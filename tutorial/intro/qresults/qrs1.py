#!/usr/bin/env artisan

from artisan import *

ast = Ast('main.cpp')

# which functions have for-loops? We can query as follows:
table = ast.query("fn{FunctionDecl} => forloop{ForStmt}")

# As we can see, our query returns all for-loop occurences
print(table)

# We can further apply operations on tables. In this example,
# we use the RSet.distinct operator to return a new table,
# filtering out all matches that contain duplicate values, as
# defined by the target column. Note that multiple
# target columns can be specified using a list,
# e.g. target=['module', 'fn']. In this case, the
# resulting table will contain rows with
# distinct (module, fn) values.

table2 = table.apply(RSet.distinct, target='fn')

fns_with_for = [ row.fn.name for row in table2 ]

print(f"Functions with for-loops: ", fns_with_for)