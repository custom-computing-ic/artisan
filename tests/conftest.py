from pathlib import Path
import shutil

import pytest


TUTORIAL = Path(__file__).resolve().parents[1] / "tutorial"


@pytest.fixture
def tutorial_project(tmp_path, monkeypatch):
    """Copy a tutorial project before parsing or transforming its sources."""
    def prepare(relative):
        project = tmp_path / "project"
        shutil.copytree(TUTORIAL / relative, project)
        monkeypatch.chdir(project)
        return project
    return prepare
