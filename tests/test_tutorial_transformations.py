"""Tests derived from the intermediate and advanced tutorials."""
from artisan import Action, Ast


def test_unparse_function(tutorial_project):
    tutorial_project("intermediate/unparse")
    ast = Ast("fib.cpp")
    fn = ast.query("fn{FunctionDecl}", where=lambda fn: fn.name == "fib")[0].fn
    code = fn.unparse()
    assert "fib" in code and "return" in code


def test_instrumentation_pending_changes(tutorial_project, tmp_path):
    tutorial_project("intermediate/instrumentation")
    ast = Ast("fib.cpp", parse=False).clone(name=str(tmp_path / "clone"))
    fn = ast.query("fn{FunctionDecl}", where=lambda fn: fn.name == "fib")[0].fn
    fn.instrument(Action.before, code="// before fib\n")
    fn.instrument(Action.begin, code="// begin fib\n")
    original = fn.unparse(changes=False)
    changed = fn.unparse(changes=True)
    assert "// before fib" not in original
    assert "// before fib" in changed and "// begin fib" in changed


def test_property_maps_survive_copy(tutorial_project):
    tutorial_project("intermediate/pmaps")
    ast = Ast("fib.cpp")
    ast.pmap = {"x": 2, "y": 3}
    fn = ast.query("fn{FunctionDecl}", where=lambda fn: fn.name == "fib")[0].fn
    ast.pmap[fn.id]["name"] = fn.name
    child = next(iter(fn.children))
    ast.pmap[(fn.id, child.id)]["parent"] = fn.id
    copy = ast.copy()
    assert copy.pmap["x"] == 2
    assert copy.pmap[fn.id]["name"] == "fib"
    assert copy.pmap[(fn.id, child.id)]["parent"] == fn.id


def test_pragmas_parse_and_replace(tutorial_project):
    tutorial_project("intermediate/pragmas")
    ast = Ast("main.cpp")
    ast.parse_pragmas()
    module = ast.sources[0].module
    assert len(module.pragmas) == 4
    def rewrite(pragma):
        if pragma[0:2] == ["artisan", "loop"]:
            return "#pragma HLS loop"
        if pragma[0:2] == ["artisan", "another"]:
            return False
        return True
    module.instrument(Action.pragmas, fn=rewrite)
    changed = module.unparse(changes=True)
    assert "#pragma HLS loop" in changed
    assert "#pragma artisan another" not in changed


def test_attributes_parse_and_replace(tutorial_project, tmp_path):
    tutorial_project("intermediate/attributes")
    ast = Ast("main.cpp", parse=False).clone(name=str(tmp_path / "clone"))
    ast.parse_attributes()
    loop = ast.query("loop{WhileStmt}")[0].loop
    assert loop.attributes
    loop.instrument(Action.attributes, fn=lambda attribute: "[[ artisan::loop ]]")
    assert "[[ artisan::loop ]]" in ast.sources[0].module.unparse(changes=True)


def test_function_tokens(tutorial_project):
    tutorial_project("advanced/tokens")
    ast = Ast("main.cpp")
    fn = ast.query("fn{FunctionDecl}")[0].fn
    spellings = [token.spelling for token in fn.tokens]
    assert "foo" in spellings
    assert "for" in spellings
    assert "return" in spellings


def test_track_nodes_across_commit(tutorial_project, tmp_path):
    tutorial_project("advanced/tracking")
    ast = Ast("main.cpp", parse=False).clone(name=str(tmp_path / "clone"))
    rows = ast.query("fn{FunctionDecl} => loop{ForStmt} ={1}> body{CompoundStmt}",
                     where=lambda loop: loop.is_outermost())
    assert rows
    loops = [row.loop for row in rows]
    for row in rows:
        row.body.instrument(Action.replace, code="{ /* removed */ }")
    tracked = ast.commit(track=loops)
    assert len(tracked) == len(loops)
    assert all(node.entity == "ForStmt" for node in tracked)
    assert "removed" in ast.unparse()
