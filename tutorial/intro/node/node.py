#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

# The tree() method prints the structure of the application. Each row
# corresponds to an AST node, which is associated to a unique id (an integer) and an entity name
# denoting its class. 'Module' is the top-level entity that corresponds the entire source-file.
ast.tree()

# To access a specific node, we can use its ID.
node = ast[4] #    ├─ 4:FunctionDecl(main.cpp:4:5)

# The entity property returns the node entity name. The entity classifies the type of construct.
print("node entity: ", node.entity)

# The 'id' property returns the node identifier (integer)
print("node id: ", node.id)

# The 'tag' property returns a human readable node identifier
print("node tag: ", node.tag)

# The "depth" property returns the level of node in the AST.
print("node depth: ", node.depth)

# The "location" property provides the coordinates of the construct
# Since a node can consist of several tokens, the node location may not
# always correspond to the first token
print(f"node location: {node.location.srcname}:{node.location.line}:{node.location.column}")

# The "range" property provides the extent of the construct. The returning object has
# 5 fields: srcname, line_start, column_start, line_end, column_end
print(f"node range: {node.range}")

# The "module" property returns the module which the node belongs to.
print("module source name: ", node.module.srcname)

# The 'parent' property returns the immediate ancestor of a node.
print("node parent ID: ", node.parent.id)

# The 'children' property returns the immediate children of the node
print("node children IDs: ", [ child.id for child in node.children])

# The 'descendants' property returns all children of the node
print("node descendant IDs: ", [ child.id for child in node.descendants])

# An entity itself is a subclass of other entities. The 'ancestry' property
# exposes all the entities a node belongs to.
print("node ancestry: ", node.ancestry)

# The 'isentity' property returns whether a node belongs to a specific entity
print("node is a declaration: ", node.isentity('decl'))

