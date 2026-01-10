# Artisan

Artisan is a program analysis and transformation framework designed to make it easy to **parse, query, instrument, and rewrite source code** using a structured, language-aware representation.

At its core, Artisan treats textual source code as a graph of connected nodes using the `libclang` library. This enables powerful workflows such as:

- Static analysis and querying of code structure
- Source-to-source transformations
- Program instrumentation and rewriting
- Building research and production tooling on top of real-world codebases

Artisan is particularly well suited for compiler research, software engineering research, and advanced developer tooling.

---

## Key Ideas

### Code as a Graph
Artisan parses source files into a graph-based intermediate representation. Nodes correspond to syntactic and semantic entities (e.g. AST nodes, statements, expressions), and edges encode relationships such as containment, control flow, and data flow.

This representation makes it straightforward to:

- Traverse code structurally
- Match complex patterns
- Apply local or global transformations

### Query–Transform Workflow
A typical Artisan workflow looks like this:

1. **Load source code** into an Artisan project
2. **Query** the graph to find relevant code patterns
3. **Transform or instrument** the matched nodes
4. **Unparse** the modified graph back into source code

This model scales from small scripts to large multi-file projects.

---

## Features

- Language-aware parsing and unparsing
- Graph-based program representation
- Declarative and imperative querying APIs
- Source-to-source transformation support
- Instrumentation hooks
- Command-line interface for batch processing
- Designed for extensibility and research experimentation

---

## Installation

### Using Conda (recommended)

Create a conda development environment as follows:

```bash
conda env create -f environment.yml
# extra step to configure environment variables
bash conda/post-install.sh artisan 
```

To activate the environment:
```
conda activate artisan
```

---

## Quick Start

Here is a minimal example showing the typical Artisan workflow:

```python
from artisan import *

ast = Ast('hello-world.cpp')

# Query the code graph
for node in sm.query("Function"):
    print(node.name)
```

You can then apply transformations or instrumentation to the matched nodes and write the modified code back to disk.

---

## Tutorials

Artisan comes with an extensive, hands-on tutorial series located in the `tutorial/` directory:

- **intro/** – Core concepts and basic usage
- **intermediate/** – More advanced queries and transformations
- **workflow/** – End-to-end workflows and project structuring
- **runtime/** – Runtime instrumentation and execution support
- **advanced/** – Internal APIs, extensibility, and research use cases

Start here:

```bash
cd tutorial
```

and follow the `README.md` files in each section.

---

## Project Structure

```
artisan/
├── artisan/              # Core Python package
│   ├── ast.py
│   ├── cnode.py
│   ├── query.py
│   ├── instrumentation.py
│   └── ...
├── tutorial/             # Step-by-step tutorials
├── conda/                # Conda build and environment files
├── pyproject.toml
└── README.md
```

---

## Use Cases

- Static analysis and program understanding
- Automated refactoring tools
- Code instrumentation for profiling or tracing
- Research prototypes for compilers and program analysis
- Teaching and experimentation with program representations

---

## License

This project is licensed under the terms of the included LICENSE file.

---

## Contributing

Contributions are welcome. The project is structured to encourage experimentation and extension—feel free to open issues or submit pull requests for bug fixes, improvements, or new ideas.

---

## Acknowledgements

Artisan is designed as a research-friendly platform, drawing inspiration from compiler infrastructures and graph-based program analysis tools.
