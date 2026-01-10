#!/usr/bin/env artisan

from artisan import *

ast = Ast("main.cpp")

table = ast.query("cond{IfStmt}")

print("if statement found:")
for row in table:
    ifstmt = row.cond
    print(f"ID: {ifstmt.id} -- {ifstmt.location} -- {ifstmt.entity}")
    print(f"   condition: {ifstmt.condition.id} -- {ifstmt.condition.location} -- {ifstmt.condition.entity}")
    print(f"   body: {ifstmt.body.id} -- {ifstmt.body.location} -- {ifstmt.body.entity}")
    if ifstmt.elsebody:
        print(f"   else: {ifstmt.elsebody.id} -- {ifstmt.elsebody.location} -- {ifstmt.elsebody.entity}")




