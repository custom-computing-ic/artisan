#!/usr/bin/env artisan

from artisan import *

ast = Ast('fib.cpp', parse=False).clone()

# The 'instrument' method is available on every node, and allows arbitrary
# code to be injected in a relative position to the node. There are 5 positions:
#
#  *before*
#  <NODE
#   { *begin*   |
#               |
#               | *around*
#     *end*     |
#   }           |
#      CODE>    |
#  *after*
#


table = ast.query("fn{FunctionDecl}", where=lambda fn:fn.name == 'fib')

if table:
    fn = table[0].fn
    fn.instrument(Action.before, code=f"// before {fn.name}\n")
    fn.instrument(Action.after, code=f"\n// after {fn.name}")
    fn.instrument(Action.begin, code=f"// begin {fn.name}")
    fn.instrument(Action.end, code=f"// end {fn.name}\n") 

    # once the code is instrumented, we can check the instrumented code
    # by unparsing with changes=True
    print(fn.unparse(changes=False))
    print(fn.unparse(changes=True))



