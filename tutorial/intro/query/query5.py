#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

fn = ast.query('fn{FunctionDecl}', where=lambda fn: fn.name == 'foo')[0].fn


# "fd" specifies the distance constraint between the root node (fn) and first node in the result set
#      arg formats: 
#           - dist        : exact distance dist
#           - (min, max)  : between min and max 
#                           min is None: no minimum
#                           max is None: no maximum  

#      distance 1: only its direct children
res = fn.query("f{node}", fd=1)
print(res, f"\nquery A => {len(res)} results")

#      distance 0: FunctionDecl + distance 1: direct children
res = fn.query("f{node}", fd=(0, 1))
print(res, f"\nquery B => {len(res)} results")


# "ld" specifies the distance constraint between the root node (fn) and the every node in the result set
#      - same arg format as "fd"

res = fn.query("f=>g=>h", fd=0, gd=(None, 2))
print(res, f"\nquery C => {len(res)} results")