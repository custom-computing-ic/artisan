#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

ast.tree()

print("\Types in declarations and expressions\n============")

nodes_with_types=ast.query("node", where=lambda node: any([ node.isentity(x) for x in ['decl', 'expr']]) )

for match in nodes_with_types:
    node = match.node

    # type is defined in clang.cindex.Type
    # reference: https://github.com/llvm-mirror/clang/blob/aa231e4be75ac4759c236b755c57876f76e3cf05/bindings/python/clang/cindex.py#L2030
    type = node.type

    print(f"{node.location}: {node.entity} ---- {type.kind}: {type.spelling}")

