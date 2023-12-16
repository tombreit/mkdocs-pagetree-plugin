<!--
SPDX-FileCopyrightText: 2023 Thomas Breitner

SPDX-License-Identifier: MIT
-->

# mkdocs-pagetree-plugin

[MkDocs](https://www.mkdocs.org/) plugin that allows you to display the page tree. Like `sitemap.xml`, but for humans.

[![PyPI - Version](https://img.shields.io/pypi/v/mkdocs-pagetree-plugin?color=rgb(17%2C%20148%2C%20223)&link=https%3A%2F%2Fpypi.org%2Fproject%2Fmkdocs-pagetree-plugin%2F)](https://pypi.org/project/mkdocs-pagetree-plugin/)
[![REUSE status](https://api.reuse.software/badge/github.com/tombreit/mkdocs-pagetree-plugin)](https://api.reuse.software/info/github.com/tombreit/mkdocs-pagetree-plugin)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![pre-commit enabled](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

## Demo & Docs

https://tombreit.github.io/mkdocs-pagetree-plugin/

## Setup

Install the plugin [PyPI package](https://pypi.org/project/mkdocs-pagetree-plugin/):

```bash
pip install mkdocs-pagetree-plugin
```

Configure `mkdocs.yml`:

```yaml
plugins:
  - pagetree
```

## Usage

Use `{{ pagetree }}` in your Markdown page(s) where the page tree should be rendered.
