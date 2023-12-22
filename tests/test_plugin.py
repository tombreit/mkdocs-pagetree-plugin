# SPDX-FileCopyrightText: 2023 Thomas Breitner
#
# SPDX-License-Identifier: MIT

import re
import subprocess
from pathlib import Path
import pytest
from distutils.dir_util import copy_tree


@pytest.fixture
def mkdocs_build(tmp_path: Path):
    """Fixture that builds MkDocs based on the top level plugin docs"""
    fixture_dir: str = str(Path(__file__).parent.parent)
    mkdocs_config_filename = "mkdocs.yml"
    temp_dir: str = str(tmp_path)
    copy_tree(fixture_dir, temp_dir)
    return subprocess.check_call(
        [
            "mkdocs",
            "build",
            "--strict",
            "--config-file",
            Path(temp_dir) / mkdocs_config_filename,
        ],
    )


def test_build(mkdocs_build: int, tmp_path: Path) -> None:
    index_file = tmp_path / "site" / "index.html"
    assert index_file.exists(), "%s does not exist" % index_file

    contents = index_file.read_text()
    assert re.search('<div class="pagetree-container">', contents)
