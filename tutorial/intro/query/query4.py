#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

# polymorphic query: get all expressions.
table = ast.query("expression{expr}")

print(table)

# using or ("|") for more complex queries
table = ast.query("(expr{expr}|decl{decl})")

print(table)

# when using OR, some rows will contain 'None' cells
for row in table:
    if row.decl is not None:
        print("declaration node id: ", row.decl.id)
    if row.expr is not None:
        print("expression node id: ", row.expr.id)
