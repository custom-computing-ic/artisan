#!/usr/bin/env artisan
from artisan import *

ast = Ast('fib.cpp')

# '.pmap' is used to load and store properties associated to the graph, nodes and edges

# graph pmap
ast.pmap = {'x': 2, 'y': 3}
ast.pmap['z'] = 15

fn_node = ast.query("fn{FunctionDecl}", where=lambda fn: fn.name == 'fib')[0].fn

# vertex pmap
ast.pmap[fn_node.id]['name'] = fn_node.name

for child in fn_node.children:
    # edge pmap
    ast.pmap[(fn_node.id, child.id)]['parent'] = fn_node.id


def print_pmaps(ast):
    # graph attributes
    print('graph pmap=', ast.pmap)

    # vertex attributes
    for vx in ast.vertices:
        if len(ast.pmap[vx]):
            print(f"vertex {vx} pmap => {ast.pmap[vx]}")

    # edge attributes
    for eg in ast.edges:
        if len(ast.pmap[eg]):
            print(f"edge {eg} pmap => {ast.pmap[eg]}")

print("===========[ast]==")
print_pmaps(ast)

print("===========[copy]==")
copy_ast = ast.copy()
print_pmaps(copy_ast)








