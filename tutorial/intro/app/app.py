#!/usr/bin/env python3
# the above 'shebang' allows a metaprogram to be invoked
# as a script inside the container or directly running on the host.

# recommended way to import artisan
from artisan import *

# The Ast class receives as an argument a single command string, which includes:
# 1) one or more C++ sources (src1.cpp src2.cpp ...),
# 2) optional include headers (-I ... )
# 3) optional defines (-DVAR=2).

# If no explicit command is provided to Ast, then the command is supplied via sys.argv.

ast = Ast('gcd.cpp fib.cpp')

# The property 'sources' provides direct access to each individual source file
print(f"number of sources: {len(ast.sources)}")

for src in ast.sources:
    print(f"* src={src.name}")

# we can also access the source by name (relative pathname) or by index
print("\n=>first source:", ast.sources[0].name)
print("=>second source:", ast.sources['gcd.cpp'].name)

# Each source is represented by an AST (Abstract Syntax Tree).
# The top-level node of each source can be accesed using the 'module' property,
# while the nodes can be accesed via 'cnodes' property.

print("\n*AST nodes*")
for src in ast.sources:
    print(f"src={src.name} => #nodes: {len(src.cnodes)}, module id: {src.module.id}")

