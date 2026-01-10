#!/usr/bin/env artisan

from artisan import *
ast = Ast('main.cpp')

# Every node has a set of tokens
table = ast.query("fn{FunctionDecl}")

fn = table[0].fn

# we can access the tokens associated with the 'token' property
tokens = fn.tokens

# the 'kind' property returns the type of token
# the 'spelling' property returns the token code
for t in tokens:
    print(f"{t.kind} - {t.spelling}")



