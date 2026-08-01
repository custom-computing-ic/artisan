# Writing Artisan Metaprograms

Artisan is a Python framework for analysing, instrumenting, and rewriting C and
C++ source code. It uses Clang to parse source into a semantic abstract syntax
tree (AST), exposes that tree as a graph of Python objects, and provides a query
language for finding code constructs.

Artisan does **not** mutate Clang's AST in place. This is because correctly
constructing or repairing a semantic AST would require substantial compiler
knowledge and would make it easy to produce an internally inconsistent tree.
Instead, Artisan records source-level instructions on tokens, emits augmented
source code, and asks Clang to parse that code into a new AST.

The central workflow is:

```text
C/C++ source
    |
    v
parse with Clang
    |
    v
query semantic AST nodes
    |
    v
annotate tokens with before/after/replace instructions
    |
    v
emit augmented source
    |
    v
reparse with Clang
    |
    v
new semantic AST
```

This primer introduces the three ideas needed to write useful Artisan
metaprograms:

1. querying the AST;
2. instrumenting matched nodes; and
3. managing the AST lifecycle.

## 1. A first metaprogram

Given the following C++ program:

```cpp
// main.cpp
int square(int value)
{
    return value * value;
}

int main()
{
    return square(4);
}
```

the following metaprogram prints every function declaration:

```python
#!/usr/bin/env artisan

from artisan import *

ast = Ast("main.cpp")

for row in ast.query("fn{FunctionDecl}"):
    print(row.fn.name, row.fn.location)
```

The argument passed to `Ast` is a compiler-like command string. It can contain
one or more source files, include paths, definitions, and other Clang
arguments:

```python
ast = Ast(
    "src/main.cpp src/algorithm.cpp "
    "-I include -I third_party/include "
    "-DENABLE_LOGGING=1 -std=c++17"
)
```

If no command string is supplied, Artisan reads the arguments given to the
metaprogram:

```python
ast = Ast()
```

This makes a metaprogram executable as:

```console
./analyse.py main.cpp -I include -DMODE=2
```

## 2. The Artisan AST

An `Ast` represents all source files supplied in the command. Each source file
is represented by a module whose root node has the entity `Module`.

```python
ast = Ast("gcd.cpp fib.cpp")

print(len(ast.sources))

for source in ast.sources:
    print(source.name)
    print(source.module)
    print(len(source.cnodes))
```

Sources can be accessed by index or by their path relative to the AST working
directory:

```python
first = ast.sources[0]
gcd = ast.sources["gcd.cpp"]
```

### 2.1 Nodes and entities

Every parsed construct is represented by a `CNode`. A node has a concrete
entity derived from its Clang cursor kind:

```python
node.entity       # for example, "ForStmt"
node.id           # integer identifier in this AST
node.tag          # human-readable source/entity/location identifier
node.location     # source, line, and column
node.range        # complete source extent
node.depth        # depth in the containment tree
```

Entities form a hierarchy. For example, a `ForStmt` is also a `loop`, a
`stmt`, and a `node`:

```python
print(node.ancestry)

if node.isentity("loop"):
    print("This node is a loop")
```

Concrete entity names begin with a capital letter, such as:

- `FunctionDecl`
- `ParmDecl`
- `VarDecl`
- `ForStmt`
- `WhileStmt`
- `IfStmt`
- `CallExpr`
- `DeclRefExpr`
- `BinaryOperator`

Useful high-level entities include:

- `decl`: any declaration;
- `stmt`: any statement;
- `expr`: any expression;
- `loop`: a `for`, `while`, or `do` loop; and
- `node`: any AST node.

### 2.2 Tree navigation

The graph edges created by Artisan describe AST containment. Nodes provide
convenient navigation properties:

```python
node.parent
node.children
node.num_children
node.child(0)
node.ancestors
node.descendants
```

The complete tree can be printed with:

```python
ast.tree()
```

or, for one subtree:

```python
node.tree()
```

The containment graph should not be confused with a control-flow or data-flow
graph. Query paths describe syntactic ancestry in the parsed AST.

### 2.3 Construct-specific interfaces

Some entities expose properties that interpret their child structure.

Functions:

```python
function.name
function.signature
function.body       # None when there is no definition
```

Function calls:

```python
call.name
call.args
call.is_operator
```

Loops:

```python
loop.condition
loop.body

# ForStmt only
loop.init
loop.increment
```

Conditionals:

```python
if_statement.condition
if_statement.body
if_statement.elsebody
```

References:

```python
reference.name
reference.decl
reference.type
reference.shape
reference.access
```

These properties are preferable to depending directly on numeric child
positions. They are available only on the corresponding entities, and some
semantic properties, such as reference access classification, are necessarily
conservative.

### 2.4 Source and tokens

Every node can emit the source corresponding to its token range:

```python
print(node.unparse())
```

Its Clang tokens are also available:

```python
for token in node.tokens:
    print(token.kind, token.spelling, token.location)
```

Token access is useful when a transformation depends on punctuation or exact
source spelling rather than only on AST structure.

## 3. Querying

The query language finds patterns in the AST containment graph. A query returns
a table-like result set. Each identifier in the query becomes a named column
in every result row.

### 3.1 Matching one entity

Find every `for` loop:

```python
results = ast.query("loop{ForStmt}")

for row in results:
    print(row.loop.location)
```

The name before the braces is an arbitrary result identifier. These queries
are equivalent except for the result-column name:

```python
ast.query("loop{ForStmt}")
ast.query("candidate{ForStmt}")
```

If no entity is specified, `node` is assumed:

```python
ast.query("item")
ast.query("item{node}")
```

Queries can use a high-level entity:

```python
ast.query("loop{loop}")  # for, while, and do loops
ast.query("decl{decl}")  # all declarations
ast.query("expr{expr}")  # all expressions
```

### 3.2 Matching structural relationships

The `=>` operator means “is an ancestor of”:

```python
results = ast.query(
    "fn{FunctionDecl} => loop{ForStmt}"
)

for row in results:
    print(row.fn.name, row.loop.location)
```

The two matched nodes do not have to be immediate parent and child. A
`FunctionDecl` can match a loop at any depth beneath it.

Longer patterns describe longer ancestry paths:

```python
results = ast.query(
    "fn{FunctionDecl} => outer{ForStmt} => inner{ForStmt}"
)
```

This returns combinations of nested loops, not merely one result per outer
loop.

### 3.3 Constraining distance

An edge can constrain the difference in AST depth:

```python
# Exactly one level: immediate parent and child.
ast.query("fn{FunctionDecl} ={1}> body{CompoundStmt}")

# Exactly two levels.
ast.query("outer{ForStmt} ={2}> inner{ForStmt}")

# Between one and three levels, inclusive.
ast.query("ancestor{node} ={1,3}> descendant{node}")
```

Distance measures AST containment depth, not source lines or runtime execution
distance.

### 3.4 Semantic predicates with `where`

Structural matching can be refined with a Python predicate:

```python
results = ast.query(
    "fn{FunctionDecl}",
    where=lambda fn: fn.name == "compute"
)
```

Predicate parameter names are matched to query identifiers. A predicate needs
to name only the columns it uses:

```python
results = ast.query(
    "fn{FunctionDecl} => loop{loop}",
    where=lambda fn, loop:
        fn.name == "compute" and loop.is_outermost()
)
```

A predicate can inspect any node property or run another query:

```python
results = ast.query(
    "loop{ForStmt}",
    where=lambda loop:
        loop.body.isentity("CompoundStmt")
        and len(loop.body.children) == 1
)
```

### 3.5 Alternatives

The `|` operator matches alternatives:

```python
results = ast.query(
    "(expression{expr}|declaration{decl})"
)
```

Because an alternative does not populate every column, unmatched cells are
`None`:

```python
for row in results:
    if row.expression is not None:
        print("expression", row.expression.location)

    if row.declaration is not None:
        print("declaration", row.declaration.location)
```

### 3.6 Scoped queries

Calling `query` on an AST searches all its modules. Calling it on a node limits
the search to that node's subtree:

```python
function = ast.query(
    "fn{FunctionDecl}",
    where=lambda fn: fn.name == "compute"
)[0].fn

loops_in_compute = function.query("loop{loop}")
```

The optional `fd` argument constrains the distance between the query root and
the first result node:

```python
# Direct children only.
function.query("child{node}", fd=1)

# The function and its direct children.
function.query("item{node}", fd=(0, 1))
```

The optional `gd` argument constrains the distance from the query root to all
matched nodes:

```python
function.query(
    "a{node} => b{node} => c{node}",
    fd=0,
    gd=(None, 2)
)
```

### 3.7 Result-set operations

Query results behave as tables:

```python
print(results)
print(len(results))

first = results[0]

for row in results:
    print(row.fn)
```

`RSet.distinct` removes duplicate values in selected columns. For example,
find each function containing at least one loop:

```python
matches = ast.query(
    "fn{FunctionDecl} => loop{loop}"
)

functions = matches.apply(
    RSet.distinct,
    target="fn"
)
```

Multiple columns can form the distinct key:

```python
unique = matches.apply(
    RSet.distinct,
    target=["src", "fn"]
)
```

`RSet.disjoint` selects rows whose target nodes do not overlap in source
tokens:

```python
safe_wave = matches.apply(
    RSet.disjoint,
    target="loop"
)
```

This is particularly important for structural transformations of nested code.

## 4. Instrumentation

Instrumentation attaches emission instructions to tokens belonging to a node.
It does not mutate the node, its Clang cursor, or the containment graph.

Conceptually, the available positions are:

```text
before
<NODE
{
    begin

    ...original contents...

    end
}
NODE>
after
```

Replacement, sometimes described as “around” instrumentation, replaces the
node's complete token range.

### 4.1 Inserting code

```python
node.instrument(
    Action.before,
    code="// emitted before the node\n"
)

node.instrument(
    Action.after,
    code="\n// emitted after the node"
)
```

For constructs containing braces:

```python
function.instrument(
    Action.begin,
    code='printf("entering function\\n");'
)

function.instrument(
    Action.end,
    code='printf("leaving function\\n");'
)
```

`Action.begin` inserts after the first `{` token in the node.
`Action.end` inserts before the last `}` token. They therefore require a
braced construct.

### 4.2 Replacing code

Replace an entire node:

```python
statement.instrument(
    Action.replace,
    code="result = fallback();"
)
```

Internally, Artisan replaces the first token and ignores the remaining tokens
in the node's range.

### 4.3 Handling semicolons

The semicolon terminating a statement is not always included in the Clang
cursor's token range. `Action.remove_semicolon` handles the adjacent module
token:

```python
statement.instrument(
    Action.remove_semicolon,
    verify=False
)
```

This is useful when wrapping an unbraced statement:

```python
body.instrument(Action.before, code="{")
body.instrument(Action.after, code=";\n}")
body.instrument(Action.remove_semicolon, verify=False)
```

### 4.4 Previewing annotations

Annotations are initially pending:

```python
print(node.unparse())               # current parsed source
print(node.unparse(changes=True))   # source with pending annotations
print(ast.unparse(changes=True))    # preview all modules
```

Previewing does not change the AST and does not write any files.

### 4.5 Committing annotations

`commit()` materialises the annotations:

```python
ast.commit()
```

For every changed module, Artisan:

1. emits source with the pending token annotations;
2. optionally formats and preprocesses it;
3. removes that module's old nodes;
4. asks Clang to parse the emitted source;
5. builds new `CNode` objects and containment edges; and
6. clears the committed annotations.

After the commit, ordinary unparsing includes the change:

```python
print(ast.unparse())
```

### 4.6 Node references become stale

A commit replaces all nodes in each changed module. Python references obtained
before the commit refer to the old AST:

```python
loop = ast.query("loop{ForStmt}")[0].loop

loop.instrument(Action.before, code="// loop\n")
ast.commit()

# Do not continue using `loop`; query its replacement.
loop = ast.query("loop{ForStmt}")[0].loop
```

Requerying is the simplest and safest approach.

When specific identities must survive a transformation, an aligned AST can
track nodes:

```python
old_loops = [
    row.loop
    for row in ast.query("loop{loop}")
]

new_loops = ast.commit(track=old_loops)
```

Tracking maps old source locations through the emitted source and performs an
entity/location integrity check. It cannot track a node that the
transformation destroys, and it requires an aligned AST.

### 4.7 Overlapping transformations

Nested constructs often cover overlapping token ranges. Structural
transformations should therefore be performed in disjoint waves:

```python
wave_number = 1

while True:
    matches = ast.query(
        "loop{loop}",
        where=lambda loop:
            not loop.body.isentity("CompoundStmt")
    )

    if not matches:
        break

    wave = matches.apply(
        RSet.disjoint,
        target="loop"
    )

    print("wave", wave_number)

    for row in wave:
        body = row.loop.body
        body.instrument(Action.before, code="{")
        body.instrument(Action.after, code=";\n}")
        body.instrument(
            Action.remove_semicolon,
            verify=False
        )

    ast.commit()
    wave_number += 1
```

Each commit creates a new legal AST. The next query then sees the newly created
`CompoundStmt` nodes. This query-transform-commit loop is a common Artisan
pattern.

### 4.8 Pragmas and attributes

Artisan can associate preprocessor pragmas with AST constructs:

```python
def pragma_rule(pragma):
    if pragma[0:2] == ["artisan", "loop"]:
        return "loop"

    if pragma[0:2] == ["artisan", "function"]:
        return "FunctionDecl"

    return None

ast.parse_pragmas(rules=[pragma_rule])
```

`Action.pragmas` can keep, remove, or replace matched pragmas:

```python
def rewrite_pragma(pragma):
    if pragma[0:2] == ["artisan", "loop"]:
        return "#pragma HLS pipeline"

    return True

module.instrument(
    Action.pragmas,
    fn=rewrite_pragma
)
```

C++ attributes can similarly be parsed and rewritten:

```python
ast.parse_attributes()

annotated = ast.query(
    "item{node}",
    where=lambda item: item.attributes is not None
)

for row in annotated:
    print(row.item.attributes)
```

## 5. The AST lifecycle

Artisan separates four forms of state:

- source files in a working directory;
- the currently parsed AST;
- pending token annotations; and
- disposable project clones.

Understanding which operation changes which state prevents most lifecycle
errors.

### 5.1 Original and cloned ASTs

For read-only analysis, parse the original source directly:

```python
ast = Ast("main.cpp")
results = ast.query("decl{decl}")
```

For transformations, work on a clone:

```python
original = Ast("main.cpp")
working = original.clone()
```

The original AST is non-discardable. A clone is disposable and can be written,
executed, versioned, or removed without touching the original project.

If the original only exists to create a working clone, avoid parsing it:

```python
working = Ast(
    "main.cpp",
    parse=False
).clone()
```

The unparsed `Ast` locates the sources. `clone()` copies and, by default,
aligns them, then parses the clone.

### 5.2 Lifecycle operations

| Operation | Pending annotations | Parsed AST | Working files |
| --- | --- | --- | --- |
| `instrument()` | Adds annotations | Unchanged | Unchanged |
| `unparse(changes=True)` | Previews them | Unchanged | Unchanged |
| `reset()` | Clears them | Unchanged | Unchanged |
| `commit()` | Applies and clears them | Reparsed | Unchanged |
| `sync()` | Retained, or applied with `commit=True` | Unchanged, or reparsed | Updated |
| `clone(changes=...)` | Choice is explicit | Creates a new AST | Creates a new tree |
| `export_to()` | Choice is explicit | Creates no useful working AST | Creates an output tree |
| `exec()` | Normally requires none | Unchanged | Builds/runs current files |
| `discard()` | Irrelevant | Clone becomes invalid | Clone is deleted |

`commit()` updates the semantic AST but does not update the files in its
working directory. `sync()` writes the current emitted AST to those files.

### 5.3 Pending changes

The state of staged instrumentation is available as:

```python
if ast.has_changes:
    print("The AST has pending annotations")
```

Pending annotations can be discarded without reparsing:

```python
ast.reset()
```

If an AST has pending changes, cloning requires an explicit decision:

```python
# Clone the currently parsed version.
copy_without_changes = ast.clone(changes=False)

# Emit pending annotations into the clone.
copy_with_changes = ast.clone(changes=True)
```

This prevents an accidental choice between two different program versions.

### 5.4 Synchronising files

Only a disposable AST can be synchronised:

```python
working.sync()
```

If annotations are pending, state whether to commit them:

```python
working.sync(commit=True)   # commit/reparse, clear annotations, then write
working.sync(commit=False)  # emit annotations without reparsing the AST
```

With `commit=False`, the annotated source is written to disk, but the parsed
AST and its pending annotations are retained. The AST and working files
therefore represent different lifecycle states. Use this deliberately;
`commit=True` is normally the safer choice when further AST work will follow.

The usual transformation sequence is:

```python
working = Ast(
    "main.cpp",
    parse=False
).clone()

# Query and instrument.

working.commit()

# Requery if more AST work is required.

working.sync()
```

or, more compactly:

```python
# Query and instrument.
working.sync(commit=True)
```

### 5.5 Cloning and backtracking

Clones make alternative transformations inexpensive to express:

```python
base = Ast("main.cpp").clone()

# Transform and commit a first version.
version_a = base.clone()

# Continue transforming base independently.
version_b = base.clone()
```

A clone can also include pending annotations and track selected nodes:

```python
old_function = ast.query(
    "fn{FunctionDecl}",
    where=lambda fn: fn.name == "compute"
)[0].fn

new_ast, tracked = ast.clone(
    changes=True,
    track=[old_function]
)

new_function = tracked[0]
```

### 5.6 Exporting

Export emits a project tree without creating a parsed working version for
further manipulation:

```python
working.export_to(
    "generated-project",
    overwrite=False,
    changes=True
)
```

### 5.7 Executing

`exec()` invokes Make in the AST working directory:

```python
return_code = working.exec()
```

By default, it expects `artisan.make`:

```make
program: main.cpp
	g++ main.cpp ${ARTISAN_CXXFLAGS} -o program
	./program
```

A different makefile or rule can be selected:

```python
working.exec(
    rule="profile",
    makefile="artisan.make"
)
```

Artisan supplies these variables to the process:

- `AST_WORKDIR`
- `AST_SOURCES`
- `AST_ARGS`
- `AST_DEFS`

Execution normally refuses to continue while annotations are pending. Commit
and synchronise first:

```python
working.sync(commit=True)
working.exec()
```

### 5.8 Runtime reports

The bundled C++ header provides:

- `artisan::Timer` for scoped timing;
- `artisan::Report` for sending runtime data to the metaprogram; and
- `artisan::Mem` for registering and querying allocation sizes.

An Artisan makefile should compile with `${ARTISAN_CXXFLAGS}` so the runtime
header and its dependencies are available.

Python can receive a report while the generated program runs:

```python
captured = None

def receive_report(ast, data):
    global captured
    captured = data

working.exec(report=receive_report)
print(captured)
```

The generated C++ program is responsible for connecting, emitting a complete
Python-compatible value, and disconnecting:

```cpp
artisan::Report::connect();
artisan::Report::write("[");
artisan::Report::write("('measurement', %1%)", value);
artisan::Report::emit("]");
artisan::Report::disconnect();
```

### 5.9 Discarding clones

When a working version is no longer needed:

```python
working.discard()
```

`discard()` recursively removes the clone's working directory. Artisan refuses
to discard an original, non-disposable AST.

## 6. Recommended transformation pattern

The following template captures the normal lifecycle:

```python
#!/usr/bin/env artisan

from artisan import *

# Locate the original project without spending time parsing it.
ast = Ast(
    "main.cpp",
    parse=False
).clone()

try:
    # 1. Query the current AST.
    matches = ast.query(
        "fn{FunctionDecl}",
        where=lambda fn: fn.body is not None
    )

    # 2. Record token-level annotations.
    for row in matches:
        row.fn.instrument(
            Action.begin,
            code=f'printf("enter {row.fn.name}\\n");'
        )

    # 3. Preview if useful.
    print(ast.unparse(changes=True))

    # 4. Emit and reparse.
    ast.commit()

    # Nodes from `matches` are now stale. Requery before
    # performing further semantic work.
    transformed_functions = ast.query(
        "fn{FunctionDecl}"
    )

    # 5. Write the clone's source files.
    ast.sync()

    # 6. Optionally compile and execute.
    # ast.exec()

finally:
    # Omit this when the generated tree should be retained.
    ast.discard()
```

If an exception occurs before `ast` is successfully cloned, initialise it
separately or guard the cleanup as appropriate.

## 7. Worked example: locating loop hotspots

A loop hotspot profiler illustrates querying, instrumentation, execution, and
the lifecycle together.

### 7.1 Select the loops

Find every loop in every source module:

```python
loops = ast.query(
    "src{Module} => loop{loop}"
)
```

Use `ForStmt` instead of `loop` when only `for` loops are required. Use a
predicate such as `loop.is_outermost()` when nested-loop measurements are not
wanted.

### 7.2 Normalise loop bodies

Counting iterations requires inserting code at the beginning of each loop
body. First convert unbraced bodies into compound statements using the
disjoint-wave pattern from Section 4.7.

After the final commit, query the loops again. The original loop objects no
longer belong to the current AST.

### 7.3 Add runtime support

Add the runtime header once to every module containing a matched loop:

```python
loops = ast.query(
    "src{Module} => loop{loop}"
)

modules = loops.apply(
    RSet.distinct,
    target="src"
)

for row in modules:
    row.src.instrument(
        Action.before,
        code="#include <artisan>\n"
    )
```

### 7.4 Instrument loop boundaries

For each loop, create a timing scope around the complete statement and insert
an iteration counter at the beginning of its body:

```python
import re

for row in loops:
    loop = row.loop
    tag = loop.tag
    identifier = re.sub(r"\W", "_", tag)

    loop.instrument(
        Action.before,
        code=(
            "{\n"
            f"long long __iterations_{identifier} = 0;\n"
            f"artisan::Timer __timer_{identifier}("
            "[](double elapsed) {"
            f"artisan::Report::write("
            f"\"('time', '{tag}', %1%),\", elapsed"
            ");"
            "});\n"
        )
    )

    loop.instrument(
        Action.begin,
        code=f"++__iterations_{identifier};"
    )

    loop.instrument(
        Action.after,
        code=(
            f"artisan::Report::write("
            f"\"('iterations', '{tag}', %1%),\", "
            f"__iterations_{identifier}"
            ");\n"
            "}\n"
        )
    )
```

The emitted structure is equivalent to:

```cpp
{
    long long iterations = 0;

    artisan::Timer timer([](double elapsed) {
        artisan::Report::write(
            "('time', 'loop-tag', %1%),",
            elapsed
        );
    });

    for (...)
    {
        ++iterations;
        // original body
    }

    artisan::Report::write(
        "('iterations', 'loop-tag', %1%),",
        iterations
    );
}
```

When the generated scope ends, the timer destructor reports its elapsed time.

### 7.5 Instrument program reporting

The program must connect before any measured work and emit/disconnect before
it terminates. A robust transformation must account for `return` statements
inside `main`; simply inserting disconnection code at the closing brace may
place it after an earlier return.

One approach is to wrap the original body in an immediately invoked lambda,
store its return value, and disconnect before returning that value. Another is
to inject an RAII reporting guard whose destructor emits and disconnects.

### 7.6 Emit, execute, and aggregate

```python
ast.sync(commit=True)
ast.exec(report=receive_report)
```

Aggregate measurements by loop tag and report:

- total elapsed time;
- dynamic invocation count;
- mean and maximum time per invocation;
- total and mean iteration count;
- source location and loop kind; and
- percentage of measured runtime.

Nested-loop times are **inclusive**: an outer loop includes time spent in its
inner loops. Adding every loop's time therefore double-counts nested work.
Either label the measurements as inclusive or maintain a runtime nesting stack
and subtract child time to derive exclusive measurements.

## 8. Pitfalls

### Using nodes after a commit

`commit()` reparses changed modules. Requery or explicitly track nodes before
continuing.

### Treating `commit()` as a file write

`commit()` updates the semantic AST. Use `sync()` to update the clone's files.

### Expecting pending annotations in normal output

Use `unparse(changes=True)` to preview uncommitted annotations.

### Transforming the original project

Use `clone()` for transformations. The original AST is intentionally protected
from synchronisation and deletion.

### Calling `Action.begin` on an unbraced construct

`Action.begin` searches for `{`. Add a compound statement first.

### Instrumenting overlapping structures in one pass

Use `RSet.disjoint`, commit one wave, and requery.

### Confusing containment with control flow

`=>` means AST ancestry. It does not mean “executes before,” “calls,” or
“reaches.”

### Omitting compilation arguments

Clang needs the relevant language standard, include paths, definitions, and
forced includes to parse the source accurately.

### Executing with pending changes

Use `sync(commit=True)` before `exec()`.

### Assuming tags are C++ identifiers

`node.tag` is useful as a report key, but paths and filenames may contain
characters that are invalid in a C++ variable name. Sanitise it before using it
as an identifier.

## 9. Quick reference

### Common queries

```python
ast.query("fn{FunctionDecl}")
ast.query("loop{loop}")
ast.query("decl{decl}")
ast.query("expr{expr}")
ast.query("fn{FunctionDecl} => call{CallExpr}")
ast.query("outer{loop} ={2}> inner{loop}")
ast.query("item{node}", where=lambda item: ...)
node.query("descendant{node}")
```

### Common node operations

```python
node.entity
node.isentity("expr")
node.location
node.range
node.parent
node.children
node.descendants
node.tokens
node.unparse()
node.query("item{node}")
node.instrument(Action.before, code="...")
```

### Instrumentation actions

```python
Action.before
Action.after
Action.begin
Action.end
Action.replace
Action.remove_semicolon
Action.pragmas
Action.attributes
```

### Lifecycle operations

```python
Ast(...)
ast.clone(...)
ast.unparse(changes=True)
ast.commit(...)
ast.reset()
ast.sync(...)
ast.export_to(...)
ast.exec(...)
ast.discard()
```

## 10. Where to go next

The repository's `tutorial/` directory contains focused examples:

- `tutorial/intro/`: applications, nodes, entities, queries, references, loops,
  functions, and conditionals;
- `tutorial/intermediate/`: unparsing, instrumentation, pragmas, attributes,
  and property maps;
- `tutorial/advanced/`: tokens, execution/reporting, cloning, and node
  tracking;
- `tutorial/runtime/`: use of the bundled C++ runtime; and
- `tutorial/workflow/`: common analysis and transformation lifecycles.

The most productive way to develop an Artisan metaprogram is incrementally:

1. print the AST structure;
2. develop and inspect the query;
3. preview annotations with `changes=True`;
4. commit and inspect the new AST;
5. synchronise only a disposable clone; and
6. compile and test the generated program.
