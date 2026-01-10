from artisan import *

# instrumentation cannot be performed on the original code:
# we must first clone it.

ast = Ast("main.cpp")

ast0 = ast.clone()

# instrument
ast0.sources[0].module.instrument(action=Action.before, code="// begin\n")
ast0.sources[0].module.instrument(action=Action.after, code="\n// end")

#print(ast0.unparse(changes = True))  # we can check the changes without commiting

ast0.commit()  # commit change, ast will be changed

ast0.discard() # we can discard when not needed










