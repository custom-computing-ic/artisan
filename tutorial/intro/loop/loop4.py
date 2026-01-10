#!/usr/bin/env artisan

from artisan import *

ast = Ast("main.cpp")

table = ast.query("loop{loop}")

print("loops found")
print("===========")

#### all loops have two properties: condition and body
# 'for' loops have two extra properties: init and increment
# 

for row in table:
    loop = row.loop
    print(f"loop: {loop.entity} - {loop.location}")

    is_for = loop.isentity("ForStmt")

    if is_for:
        print(f"   - init: {loop.init.entity} - {loop.init.location}")

    print(f"   - condition: {loop.condition.entity} - {loop.condition.location}")

    if is_for:
        print(f"   - incr: {loop.increment.entity} - {loop.increment.location}")

    print(f"   - body: {loop.body.entity} - {loop.body.location}")

