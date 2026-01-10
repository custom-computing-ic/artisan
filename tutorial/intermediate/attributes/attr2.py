#!/usr/bin/env artisan

from artisan import *
ast = Ast('main.cpp', parse=False).clone()

ast.parse_attributes()

def fn(attribute):
    # return False: remove attribute
    # return True: keep as-is
    return "[[ artisan::loop ]]" # replace

table = ast.query("loop{WhileStmt}")
if table:
    loop = table[0].loop
    loop.instrument(Action.attributes, fn=fn)

print(ast.sources[0].module.unparse(changes=True, align=True))
