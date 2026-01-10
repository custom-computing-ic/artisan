#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

ast.tree()

print("\nReferences\n==========")
references = ast.query("node", where=lambda node: node.entity in ['DeclRefExpr', 'MemberRefExpr', 'ArraySubscriptExpr'] )

for ref in references:
    node = ref.node
    print(f"{node.location}: {node.entity}: {node.unparse()}")



