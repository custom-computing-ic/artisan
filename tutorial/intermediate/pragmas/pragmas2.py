#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

# in the previous example, all pragmas are captured inside the corresponding module.
# we can override this behavior, and associate pragmas to specific constructs.

# In this example, we wish to associate "artisan loop" pragmas to adjacent loops, and "artisan fn"
# to adjacent function declarations.

def artisan_pragmas(pragma):
    if pragma [0] == "artisan":
        if pragma[1] == "loop":
            return "loop" # this is the entity we wish to associate to
        elif pragma[1] == "fn":
            return "FunctionDecl"
        else:
            return False # exclude pragma

    # Returning None allows other rules to handle remaining pragmas.
    # By default, all unhandled rules are captured inside module.
    return None

# we pass the 'artisan_pragmas' function to parse_pragmas
ast.parse_pragmas(rules=[artisan_pragmas])

table = ast.query("node{node}", where=lambda node: node.pragmas is not None)

for row in table:
    print(f"{row.node.id}:{row.node.entity} => {row.node.pragmas}")
