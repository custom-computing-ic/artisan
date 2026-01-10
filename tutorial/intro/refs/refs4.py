#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

table = ast.query("ref{DeclRefExpr}")

for row in table:
    ref = row.ref
    print(f"{ref.name} ({ref.location})")

    # shape => (element type)
    shape = ref.shape
    # shape.dim is a list of dimensions if array, or None if scalar
    if shape.dim is None:
        print(f"  - SHAPE: {shape.base_type.spelling} <scalar>")
    else:
        print(f"  - SHAPE: {shape.base_type.spelling} {shape.dim}")

    # read/write
    access = ref.access
    print(f"  - ACCESS: READ: {access.is_used}, WRITE: {access.is_def}")

    # read/write
    decl = ref.decl # variable declaration
    if decl is not None:
        print(f"  - VAR DECL: {decl.unparse()}, local: {decl.is_local}")

