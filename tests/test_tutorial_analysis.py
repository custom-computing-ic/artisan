"""Behavior exercised by the introductory tutorial examples."""
from artisan import Ast, RSet


def test_multiple_sources(tutorial_project):
    tutorial_project("intro/app")
    ast = Ast("gcd.cpp fib.cpp")
    assert {source.name for source in ast.sources} == {"gcd.cpp", "fib.cpp"}
    assert all(source.module is not None for source in ast.sources)
    assert ast.sources["gcd.cpp"].name == "gcd.cpp"


def test_queries_and_distances(tutorial_project):
    tutorial_project("intro/query")
    ast = Ast("main.cpp")
    loops = ast.query("loop{ForStmt}")
    pairs = ast.query("outer{ForStmt} => inner{ForStmt}")
    assert len(loops) == 3
    assert len(pairs) == 3
    assert all(row.outer.id != row.inner.id for row in pairs)
    fn = ast.query("fn{FunctionDecl}", where=lambda fn: fn.name == "foo")[0].fn
    direct = fn.query("node{node}", fd=1)
    assert {row.node.id for row in direct} == {node.id for node in fn.children}


def test_loop_properties(tutorial_project):
    tutorial_project("intro/loop")
    ast = Ast("main.cpp")
    loops = ast.query("loop{loop}")
    assert {row.loop.entity for row in loops} >= {"ForStmt", "WhileStmt", "DoStmt"}
    for_loops = ast.query("loop{ForStmt}")
    assert len(for_loops) == 2
    assert sum(row.loop.is_outermost() for row in for_loops) == 1
    assert all(row.loop.body and row.loop.condition for row in loops)


def test_functions_and_calls(tutorial_project):
    tutorial_project("intro/functions")
    ast = Ast("main.cpp")
    functions = ast.query("fn{FunctionDecl}")
    assert {row.fn.name for row in functions} >= {"f", "g", "main"}
    calls = ast.query("call{CallExpr}")
    assert sum(row.call.name == "g" for row in calls) == 2
    g = next(row.fn for row in functions if row.fn.name == "g")
    assert len(g.signature.params) == 2
    assert "return" in g.body.unparse()


def test_conditionals(tutorial_project):
    tutorial_project("intro/conditionals")
    ast = Ast("main.cpp")
    conditions = ast.query("cond{IfStmt}")
    assert len(conditions) == 2
    assert all(row.cond.condition and row.cond.body for row in conditions)
    assert sum(row.cond.elsebody is not None for row in conditions) == 1


def test_references_and_shapes(tutorial_project):
    tutorial_project("intro/refs")
    ast = Ast("main.cpp")
    refs = ast.query("ref{DeclRefExpr}")
    assert {row.ref.name for row in refs} >= {"a", "b", "c", "s"}
    array = next(row.ref for row in refs if row.ref.name == "s")
    assert array.shape.dim == [10]
    assert array.decl is not None


def test_distinct_query_results(tutorial_project):
    tutorial_project("intro/qresults")
    ast = Ast("main.cpp")
    rows = ast.query("fn{FunctionDecl} => loop{ForStmt}")
    distinct = rows.apply(RSet.distinct, target="fn")
    assert len(rows) == 6
    assert {row.fn.name for row in distinct} == {"foo", "bar"}
    assert len(distinct) == 2
