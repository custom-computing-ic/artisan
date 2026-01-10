from artisan import *

ast = Ast("main.cpp")

ast0 = ast.clone()

# instrument
ast0.sources[0].module.instrument(action=Action.before, code="// begin\n")
ast0.sources[0].module.instrument(action=Action.after, code="// end\n")

# when executing, we must sync ast with storage. Changes were made, 
# so we must commit first.
ast0.commit()

ast1 = ast0.clone() # keep this version

# instrument
ast0.sources[0].module.instrument(action=Action.before, code="\n// another begin")
ast0.sources[0].module.instrument(action=Action.after, code="\n// another end")

ast0.commit()

print(ast0.unparse())

ast0 = ast1 # backtrack

print(ast0.unparse())
