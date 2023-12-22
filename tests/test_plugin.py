# SPDX-FileCopyrightText: 2023 Thomas Breitner
#
# SPDX-License-Identifier: MIT

import re
import subprocess
from pathlib import Path
from distutils.dir_util import copy_tree
import pytest


@pytest.fixture
def mkdocs_build(tmp_path: Path):
    """Fixture that builds MkDocs based on the top level plugin docs"""
    fixture_dir: str = str(Path(__file__).parent.parent)
    temp_dir: str = str(tmp_path)
    copy_tree(fixture_dir, temp_dir)
    return subprocess.check_call(
        [
            "mkdocs",
            "build",
            "--strict",
            "--config-file",
            Path(temp_dir) / "mkdocs.yml",
        ],
    )


def test_build(mkdocs_build: int, tmp_path: Path) -> None:
    index_file_html = tmp_path / "site" / "index.html"
    index_file_md = tmp_path / "docs" / "index.md"

    contents_md = index_file_md.read_text()
    assert re.search("{{ pagetree }}", contents_md)

    assert index_file_html.exists(), "%s does not exist" % index_file_html
    contents_html = index_file_html.read_text()
    assert re.search('<div class="pagetree-container">', contents_html)
    assert not re.search("{{ pagetree }}", contents_html)
