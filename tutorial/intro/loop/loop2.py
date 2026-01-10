#!/usr/bin/env artisan

from artisan import *

ast = Ast("main.cpp")

table = ast.query("l{ForStmt}")

print("for-loops found:")
for row in table:
    print(f"ID: {row.l.id} -- {row.l.location} -- {row.l.entity} -- {row.l.is_innermost()} -- outermost: {row.l.is_outermost()} ")


