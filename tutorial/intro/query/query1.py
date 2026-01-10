#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

# Let's first look at the structure of our example application
ast.tree()

# The "query" method is available on the ast and node objects.
# If invoked from the ast, then all nodes are queried. If invoked from a node,
# then the node and all its descendents are queried.

# For our first query, let's find all FOR statements. In this case, "loop" is an arbitrary
# identifier, and ForStmt specifies the type of nodes we wish to find. Note that entities specified
# in the query can be low-level or high-level. If no entity is specified,
# then the "node" entity is assumed (i.e. matches every node).
table = ast.query("loop{ForStmt}")

# print the resulting table
print(table)

# iterate the table. Note that the "loop" identifier used in the query
# is used to access the corresponding node in each match.
print("for-loops:")
for row in table:
    forstmt = row.loop
    print(f"id: {forstmt.id}")


