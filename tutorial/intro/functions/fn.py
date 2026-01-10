#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

print("\nFunction Declarations\n=====================")

fndecls = ast.query("fndecl{FunctionDecl}" )

for f in fndecls:
    fndecl = f.fndecl
    '''
    function signature (sig) format:
       sig.rettype: return type
       sig.params: list of parameters,
                   each parameter is a tuple - (type, name)


    '''
    print(f"=> name: {fndecl.name}, signature: {fndecl.signature}")
    body = fndecl.body
    if body:
        print(fndecl.body.unparse())
    else:
        print("<no definition>")

print("\nFunction calls\n==============")

table = ast.query("call{CallExpr}")
for row in table:
    args = ", ".join([ arg.unparse() for arg in row.call.args])
    print(f"function: {row.call.name}, arguments: {args}")

