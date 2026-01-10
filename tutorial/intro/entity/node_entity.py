#!/usr/bin/env artisan

from artisan import *

ast = Ast('hello.cpp')

# Every node in the ast is associated to an entity. Let's look at node id 4.

node = ast[4] #    ├─ 4:FunctionDecl(main.cpp:4:5)

print(f"entity: {node.entity}")

# low-level entities identify the type of construct of each node, and start with a capital letter.
# In this case, our node is a function declaration.

# Every entity in turn, is part of an hierarchy. The entity hierarchy can be viewed using
# the entities tool, or using the ancestry property of the node.

print(f"ancestry: {node.ancestry}")

# Hence, node 4 is a function declaration, and also a declaration (decl) and
# an AST node (node). We check whether a node is a specific entity as follows:
print("Is node a declaration?: ", node.isentity("decl"))

# High-level entities group different types of constructs, and are identified by
# a lower case name. The main high-level entities are:
# => decl: a declaration
# => stmt: a statement
# => expr: an expression
# => loop: a loop
# => node: an AST node
