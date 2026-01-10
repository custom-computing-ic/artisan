#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

# Let's first look at the structure of our example application
ast.tree()

# find all permutations of two nested for-loops
# The => operator represents the relationship "is ancestor of"
table = ast.query("loop1{ForStmt}=>loop2{ForStmt}")

# print the result-set
print(table)

# iterate the resulting table
print("all permutations of two nested for-loops:")
for row in table:
    for1 = row.loop1
    for2 = row.loop2
    print(f"{for1.id} => {for2.id}")

# The distance between two nodes can be constrained
# in a query. This distance can be specified as follows:
#     ={5}> (exactly 5)
#     ={1,2}> (between 1 and 2)
#     ={min:2> (at least 2)
#     ={max:5}> (at most 5)

table = ast.query("loop1{ForStmt}={2}>loop2{ForStmt}")

print("two nested for-loops:")
for row in table:
    for1 = row.loop1
    for2 = row.loop2
    print(f"{for1.id} => {for2.id}")
