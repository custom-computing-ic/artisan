#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

# Let's first look at the structure of our example application
ast.tree()

# perfect two nested for-loops (note that we assume loops define a scope).
# In this example, we use a condition (where), which receives a function where the parameters
# are the query identifiers
print("perfect two-nested loops")
table = ast.query("loop1{ForStmt}={1}>body{CompoundStmt}={1}>loop2{ForStmt}",
                  where=lambda body: len(body.children) == 1)


print(table)