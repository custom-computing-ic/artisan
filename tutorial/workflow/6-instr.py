from artisan import *

ast = Ast("main.cpp")

ast0 = ast.clone()

row = ast0.query("fn{FunctionDecl}={1}>body{CompoundStmt}")[0]
row.body.instrument(action=Action.replace, code=f"\n {{ /* '{row.fn.name}' body */ }}")

(ast1, [new_fn]) = ast0.clone(changes=True, track=[row.fn])

print(ast1.unparse())
