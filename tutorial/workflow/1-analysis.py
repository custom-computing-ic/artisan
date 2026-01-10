from artisan import *

# when performing only analysis, we parse directly 
# from the source

ast = Ast("main.cpp")
table = ast.query("d{decl}")
print(f"[i] found {len(table)} declarations(s):")
for row in table:
    print(f"  => {row.d.location}: {row.d.spelling}")




