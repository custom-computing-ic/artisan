#!/usr/bin/env artisan

from artisan import *

ast = Ast('fib.cpp')

# The 'unparse' method which is available on every node, returns a string corresponding to the code

table = ast.query("fn{FunctionDecl}", where=lambda fn:fn.name == 'fib')

if table:
    fn = table[0].fn
    code = fn.unparse()
    print(code)

# unparse has two parameters:
#     changes (default: False): unparses taking into account instrumented code
#     align (default: False): unparses with code indentation (pretty print)


