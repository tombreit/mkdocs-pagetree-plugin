# mkdocs-pagetree-plugin

MkDocs plugin that allows you to display the page tree. Like `sitemap.xml`, but for humans.

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

## Demo

https://tombreit.github.io/mkdocs-pagetree-plugin/

## Usage

Use `{{ pagetree }}` in your Markdown page(s) where the page tree should be rendered.
