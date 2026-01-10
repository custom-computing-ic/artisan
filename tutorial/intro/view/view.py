#!/usr/bin/env artisan

from artisan import *

ast = Ast('fib.cpp gcd.cpp')

# The tree property prints the structure of an ast or a specific node.
print("view the AST structure")
# By default, each row printed corresponds to a node.
# Each node appears with its ID number (red) and its entity name (blue), along
# with its source location (grey)
ast.tree()

print("tree structure, root node 86")
ast[86].tree()

print("tree structure, root node 86, max depth = 2")
ast[86].tree(depth=2)

# print out custom information about node (debugging)
print("tree structure, root node 86, print the spelling of each node")
ast[86].tree(info=lambda node: f"{node.spelling}")

# view AST using a web browser, root node=ID86
ast[86].view()

# view the entire AST
#ast.view()

