#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

# in this example, we instrument for-loops to
# add scope { } if their bodies don't have it.
table = ast.query("forloop{ForStmt}", where=lambda forloop: not forloop.body.isentity("CompoundStmt"))

# all six loops do not have scope
print(len(table))

# unfortunately, we cannot instrument all six loops in one go, since they overlap.
# a common pattern in these cases, will be to instrument disjoint constructs in waves as follows

wave = 1
while True:
    table = ast.query("forloop{ForStmt}", where=lambda forloop: not forloop.body.isentity("CompoundStmt"))

    if len(table) == 0:
        break

    print(f"wave: {wave}")

    # filters table such that all forloops do not overlap, and thus can be safely instrumented in one go
    disjoint_table = table.apply(RSet.disjoint, target='forloop')

    for row in disjoint_table:
        print(f"  - instrumenting for-loop {row.forloop.condition.unparse()}")
        row.forloop.body.instrument(Action.before, code="{")
        # the ";" is not necessary when the body construct ends with "}". We can
        # either unparse the body code to check the last character or check the tokens.
        # See tokens example in advanced/
        row.forloop.body.instrument(Action.after, code=";\n}")
        row.forloop.body.instrument(Action.remove_semicolon, verify=False)

    ast.commit()

    wave = wave + 1

print(ast.sources[0].module.unparse())





