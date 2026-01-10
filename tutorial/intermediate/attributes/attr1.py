#!/usr/bin/env artisan

from artisan import *
import pprint

ast = Ast('main.cpp')

# attributes will be automatically
# attached to the next construct
ast.parse_attributes()


# constructs with attributes
table = ast.query("node", where=lambda node: node.attributes is not None)

pp=pprint.PrettyPrinter(indent=4)
for row in table:
    node = row.node
    print(f"{node.entity}-{node.location}")

    # Each attribute: [[attr0, attr1, attr2 ]] => ({'attr0': [args0], 'attr1': [args1]}, token_ini, token_end)
    pp.pprint(node.attributes)
