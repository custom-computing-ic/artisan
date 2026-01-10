#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

# to enable pragmas, we need to invoke the following Ast method:
ast.parse_pragmas()

# by default, all pragmas are associated to the corresponding module.
pragmas = ast.sources[0].module.pragmas

for pragma in pragmas:
    # Each pragma has the format: ([token list], token_start, token_end)
    print(f"{pragma[0]} => {pragma[1]}")


