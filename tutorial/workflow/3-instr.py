from artisan import *

# optimisation over 2-instr.py:
#    => original code is not parsed
#    => clone can be analysised and instrumented
ast = Ast("main.cpp", parse=False).clone()

ast.sources[0].module.instrument(action=Action.before, code="// begin\n")
ast.sources[0].module.instrument(action=Action.after, code="\n// end")

ast.commit()  # commit change, ast will be changed