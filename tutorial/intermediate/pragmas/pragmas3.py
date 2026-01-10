#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

ast.parse_pragmas()

def fn_pragmas(pragma):
    if pragma[0] == 'artisan':
        if pragma[1] == 'loop':
            # (str) replace pragma
            return "#pragma HLS " + "".join(pragma[1:])
        elif pragma[1] == 'another':
            return False # (bool) remove pragma from code

    return True # (bool) keep pragma in code

ast.sources[0].module.instrument(Action.pragmas, fn=fn_pragmas)

print(ast.sources[0].module.unparse(changes=True, align=True))
