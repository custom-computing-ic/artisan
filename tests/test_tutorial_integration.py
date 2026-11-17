"""End-to-end checks for the workflow and execution tutorials."""
import shutil
import subprocess

import pytest
from artisan import Action, Ast


def test_clone_commit_sync_and_execute_make(tutorial_project, tmp_path):
    if not shutil.which("make"):
        pytest.skip("make is required for Ast.exec")
    project = tutorial_project("workflow")
    original = (project / "main.cpp").read_text()
    ast = Ast("main.cpp", parse=False).clone(name=str(tmp_path / "clone"))
    ast.sources[0].module.instrument(Action.before, code="// workflow test\n")
    ast.sync(commit=True)
    assert "// workflow test" in (tmp_path / "clone" / "main.cpp").read_text()
    assert (project / "main.cpp").read_text() == original
    assert ast.exec() == 0
    ast.discard()
    assert not (tmp_path / "clone").exists()


def test_transformed_source_compiles_and_runs(tutorial_project, tmp_path):
    compiler = shutil.which("g++")
    if not compiler:
        pytest.skip("g++ is required to compile the transformed example")
    tutorial_project("intro/query")
    ast = Ast("main.cpp", parse=False).clone(name=str(tmp_path / "clone"))
    fn = ast.query("fn{FunctionDecl}", where=lambda fn: fn.name == "foo")[0].fn
    fn.instrument(Action.before, code="// transformed by test\n")
    ast.sync(commit=True)
    clone = tmp_path / "clone"
    (clone / "driver.cpp").write_text("int foo(int, int, int);\nint main() { return foo(2, 2, 2); }\n")
    binary = clone / "example"
    subprocess.run([compiler, str(clone / "main.cpp"), str(clone / "driver.cpp"),
                    "-o", str(binary)], check=True, capture_output=True, text=True)
    subprocess.run([str(binary)], check=True, capture_output=True, text=True)
