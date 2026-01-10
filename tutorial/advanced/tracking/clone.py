from artisan import *

ast = Ast("main.cpp", parse=False).clone()

# assume scopify
table = ast.query("fn{FunctionDecl} => loop{ForStmt} ={1}> body{CompoundStmt}", where=lambda loop: loop.is_outermost())

outerloops = []
for row in table:
    row.body.instrument(action=Action.replace, code="{\n/* removed */ \n}\n")
    outerloops.append(row.loop)

(new_ast, ret) = ast.clone(track=outerloops, changes=True)

print("OLD => NEW")
for i in range(0, len(outerloops)):
    print(f"{outerloops[i].id} => {ret[i].id}")

print("\nNew loops")
table2 = new_ast.query("fn{FunctionDecl} => loop{ForStmt}")
for row in table2:
    print(f"{row.loop.id}")

