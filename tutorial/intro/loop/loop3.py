#!/usr/bin/env artisan

from artisan import *

ast = Ast("main.cpp")

# Ranking allows to check the position of one node in regards to another.
# The method "rank" is available to every node, and works by ranking its descendents.
#    context: function which receives a node object, and must return True if part of ranking

table = ast.query("fn{FunctionDecl}")

print("considering only for-loops")
for row in table:
    fn = row.fn
    print("    * function: ", fn.name)
    ret = fn.rank(context=lambda node: node.isentity("ForStmt"))
    for loop_id in ret:
        loop = ast[loop_id]
        rank = ", ".join([str(x) for x in ret[loop_id]])
        print(f"       => loop in {loop.location} => rank: ({rank})")

print("considering all types of loops")
for row in table:
    fn = row.fn
    print("   * function: ", fn.name)
    ret = fn.rank(context=lambda node: node.isentity("loop"))
    for loop_id in ret:
        loop = ast[loop_id]
        rank = ", ".join([str(x) for x in ret[loop_id]])
        print(f"       => loop in {loop.location} => rank: ({rank})")
