# SPDX-FileCopyrightText: Thomas Breitner
#
# SPDX-License-Identifier: MIT

import re
import subprocess
import shutil
from pathlib import Path

from bs4 import BeautifulSoup
import pytest


@pytest.fixture
def mkdocs_project(tmp_path: Path) -> Path:
    """Set up a temporary MkDocs project with the pagetree plugin."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    docs_dir = project_dir / "docs"
    docs_dir.mkdir()

    # Create mkdocs.yml
    mkdocs_yml = project_dir / "mkdocs.yml"
    mkdocs_yml.write_text(
        """
site_name: Test Site
plugins:
  - pagetree
"""
    )

    # Create page structure
    (docs_dir / "index.md").write_text("# Home\n")
    (docs_dir / "page1.md").write_text("# Page 1\n")
    (docs_dir / "page2.md").write_text("# Page 2\n")

    section_dir = docs_dir / "section"
    section_dir.mkdir()
    (section_dir / "index.md").write_text("# Section Index\n")
    (section_dir / "subpage1.md").write_text("# Subpage 1\n")
    (section_dir / "subpage2.md").write_text("# Subpage 2\n")

    subsection_dir = docs_dir / "section" / "subsection"
    subsection_dir.mkdir()
    (subsection_dir / "index.md").write_text("# Subsection Index\n")
    (subsection_dir / "subsectionpage1.md").write_text("# Subsection page 1\n")
    (subsection_dir / "subsectionpage2.md").write_text("# Subsection page 2\n")

    # subprocess.run(["tree", project_dir], check=True)
    # ├── docs
    # │   ├── index.md
    # │   ├── page1.md
    # │   ├── page2.md
    # │   └── section
    # │       ├── index.md
    # │       ├── subpage1.md
    # │       ├── subpage2.md
    # │       └── subsection
    # │           ├── index.md
    # │           ├── subsectionpage1.md
    # │           └── subsectionpage2.md
    # └── mkdocs.yml

    return project_dir


@pytest.fixture
def build_mkdocs(mkdocs_project: Path):
    """Build the MkDocs site."""

    def _build():
        subprocess.run(
            ["mkdocs", "build", "--strict", "--clean"],
            cwd=mkdocs_project,
            check=True,
        )

    return _build


@pytest.fixture
def mkdocs_build(tmp_path: Path):
    """Fixture that builds MkDocs based on the top level plugin docs"""
    fixture_dir: str = str(Path(__file__).parent.parent)
    temp_dir: str = str(tmp_path)
    shutil.copytree(fixture_dir, temp_dir, dirs_exist_ok=True)
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
    """Basic test to ensure MkdDocs builds succeedes for the existing /docs directory"""
    index_file_html = tmp_path / "site" / "index.html"
    index_file_md = tmp_path / "docs" / "index.md"

    contents_md = index_file_md.read_text()
    assert re.search("{{ pagetree }}", contents_md)

    assert index_file_html.exists(), "%s does not exist" % index_file_html
    contents_html = index_file_html.read_text()
    assert re.search('<div class="pagetree-container">', contents_html)
    assert not re.search("{{ pagetree }}", contents_html)


def test_pagetree_all(mkdocs_project: Path, build_mkdocs):
    """Test the pagetree plugin with the 'all' option."""
    target_md = mkdocs_project / "docs" / "index.md"
    target_md.write_text("{{ pagetree(all) }}")
    build_mkdocs()

    target_html = mkdocs_project / "site" / "index.html"
    assert target_html.exists()
    content = target_html.read_text()

    soup = BeautifulSoup(content, "html.parser")
    pagetree = soup.find("ul", class_="pagetree")
    links = [a.get("href") for a in pagetree.find_all("a")]

    assert "page1/" in links
    assert "page2/" in links
    assert "section/" in links
    assert "section/subpage1/" in links
    assert "section/subpage2/" in links


def test_pagetree_children(mkdocs_project: Path, build_mkdocs):
    """Test the pagetree plugin with the 'children' option."""
    target_md = mkdocs_project / "docs" / "section" / "index.md"
    expected_content = "# Section Index\n\n{{ pagetree(children) }}"
    target_md.write_text(expected_content)

    # Verify file was written correctly
    assert target_md.exists()
    assert target_md.read_text() == expected_content

    build_mkdocs()  # Execute the build function

    target_html = mkdocs_project / "site" / "section" / "index.html"
    assert target_html.exists()
    content = target_html.read_text()

    soup = BeautifulSoup(content, "html.parser")
    pagetree = soup.find("ul", class_="pagetree")
    links = [a.get("href") for a in pagetree.find_all("a")]

    assert "page1/" not in links
    assert "page2/" not in links
    assert "subsection/" in links
    assert "subsection/subsectionpage1/" in links
    assert "subsection/subsectionpage2/" in links


def test_pagetree_siblings(mkdocs_project: Path, build_mkdocs):
    """Test the pagetree plugin with the 'siblings' option."""
    target_md = mkdocs_project / "docs" / "section" / "subpage1.md"
    target_md.write_text("# Subpage 1\n\n{{ pagetree(siblings) }}")
    build_mkdocs()

    target_html = mkdocs_project / "site" / "section" / "subpage1" / "index.html"
    assert target_html.exists()

    content = target_html.read_text()
    soup = BeautifulSoup(content, "html.parser")
    pagetree = soup.find("ul", class_="pagetree")
    links = [a.get("href") for a in pagetree.find_all("a")]

    assert "../" in links
    assert "../subpage2/" in links
    assert "../subsection/" in links
    assert "../subpage1/" not in links


def test_pagetree_subtree(mkdocs_project: Path, build_mkdocs):
    """Test the pagetree plugin with the 'subtree' option."""
    target_md = mkdocs_project / "docs" / "section" / "index.md"
    target_md.write_text("{{ pagetree(subtree) }}")
    build_mkdocs()

    target_html = mkdocs_project / "site" / "section" / "index.html"
    assert target_html.exists()

    content = target_html.read_text()
    soup = BeautifulSoup(content, "html.parser")
    pagetree = soup.find("ul", class_="pagetree")
    links = [a.get("href") for a in pagetree.find_all("a")]

    assert "./" in links
    assert "subpage1/" in links
    assert "subpage1/" in links
    assert "subsection/" in links
    assert "subsection/subsectionpage1/" in links
    assert "subsection/subsectionpage1/" in links
    assert "../" not in links


def test_plugin_compatibility_with_macros_lenient(tmp_path: Path):
    """Test that pagetree works with mkdocs-macros-plugin in lenient mode."""
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    docs_dir = project_dir / "docs"
    docs_dir.mkdir()

    # Create mkdocs.yml with both plugins - pagetree first
    mkdocs_yml = project_dir / "mkdocs.yml"
    mkdocs_yml.write_text(
        """
site_name: Test Site
plugins:
  - pagetree
  - macros
"""
    )

    # Create a page with both pagetree marker and macros variable
    (docs_dir / "index.md").write_text(
        """# Home

Site name: {{ config.site_name }}

{{ pagetree }}
"""
    )

    (docs_dir / "page1.md").write_text("# Page 1\n")

    # Build the site
    subprocess.run(
        ["mkdocs", "build", "--strict", "--clean"],
        cwd=project_dir,
        check=True,
    )

    # Verify the output contains both the macros variable and pagetree
    index_html = project_dir / "site" / "index.html"
    assert index_html.exists()
    content = index_html.read_text()

    # Check that macros variable was processed
    assert "Site name: Test Site" in content

    # Check that pagetree was rendered
    soup = BeautifulSoup(content, "html.parser")
    pagetree = soup.find("ul", class_="pagetree")
    assert pagetree is not None


def test_plugin_order_matters_documentation(tmp_path: Path):
    """Verify that the built documentation includes plugin compatibility information."""
    fixture_dir: str = str(Path(__file__).parent.parent)
    temp_dir: str = str(tmp_path)
    shutil.copytree(fixture_dir, temp_dir, dirs_exist_ok=True)

    subprocess.check_call(
        [
            "mkdocs",
            "build",
            "--strict",
            "--config-file",
            Path(temp_dir) / "mkdocs.yml",
        ],
    )

    index_html = tmp_path / "site" / "index.html"
    assert index_html.exists()
    content = index_html.read_text()

    # Verify that plugin compatibility documentation exists
    assert "Plugin Compatibility" in content
    assert "mkdocs-macros-plugin" in content
    assert "plugin order" in content.lower()

    # Check for the specific recommendations
    soup = BeautifulSoup(content, "html.parser")
    plugin_compat = soup.find("h2", id="plugin-compatibility")
    assert plugin_compat is not None, (
        "Plugin Compatibility section should exist in documentation"
    )
