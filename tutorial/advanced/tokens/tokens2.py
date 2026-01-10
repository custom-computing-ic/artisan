#!/usr/bin/env artisan

from artisan import *
import clang.cindex as ci

ast = Ast('main.cpp', parse=False).clone()

# in this example, we instrument for-loops to
# add scope { } if their bodies don't have it.
table = ast.query("forloop{ForStmt}", where=lambda forloop: not forloop.body.isentity("CompoundStmt"))

wave = 1
while True:
    table = ast.query("forloop{ForStmt}", where=lambda forloop: not forloop.body.isentity("CompoundStmt"))

    if len(table) == 0:
        break

    print(f"wave: {wave}")

    # filters table such that all forloops do not overlap, and thus can be safely instrumented in one go
    disjoint_table = table.apply(RSet.disjoint, target='forloop')

    for row in disjoint_table:
        print(f"  - instrumenting for-loop {row.forloop.condition.unparse()}")
        row.forloop.body.instrument(Action.before, code="{")

        last_body_token = [t for t in row.forloop.body.tokens] [-1]

        if last_body_token.kind == ci.TokenKind.PUNCTUATION and last_body_token.spelling == "}":
            sep = "" # does not add ";" if the body ends with "}"
        else:
            sep = ";"

        row.forloop.body.instrument(Action.after, code="%s\n}" % sep)


        row.forloop.body.instrument(Action.remove_semicolon, verify=False)

    ast.commit()

    wave = wave + 1

print(ast.sources[0].module.unparse())

ast.discard()



