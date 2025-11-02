# MkDocs Pagetree Plugin

MkDocs plugin that allows you to display the page tree. Like `sitemap.xml`, but for humans. This plugin replaces the `pagetree` marker with an actual pagetree.

- [Repository](https://github.com/tombreit/mkdocs-pagetree-plugin)
- [Issues](https://github.com/tombreit/mkdocs-pagetree-plugin/issues)
- [PyPI package](https://pypi.org/project/mkdocs-pagetree-plugin/)

## Setup

Install the plugin ([PyPI package](https://pypi.org/project/mkdocs-pagetree-plugin/)) with `pip`:

```bash
pip install mkdocs-pagetree-plugin
```

Configure via `mkdocs.yml`:

```yaml
plugins:
  - pagetree
```

## Options

The following tree options for the pagetree marker exists (see the [demo section](#demo) for integration):

- <strong><code>&#123;&#123; pagetree(all) &#125;&#125;</code></strong>

    Render the whole pagetree. This is the default tree option, the `(all)` parameter can also be omitted.

- <strong><code>&#123;&#123; pagetree(children) &#125;&#125;</code></strong>

    Render only direct children of the current page

- <strong><code>&#123;&#123; pagetree(siblings) &#125;&#125;</code></strong>

    Render only direct siblings of the current page, excluding the current page

- <strong><code>&#123;&#123; pagetree(subtree) &#125;&#125;</code></strong>

    Render the subtree which contains the current page

## Notes

- The plugin or marker can be used on several pages.
- Only the first occurrence of the marker <code>&#123;&#123; pagetree &#125;&#125;</code> on a page is replaced.
- If any page `status` is used ([Ref](https://squidfunk.github.io/mkdocs-material/reference/#setting-the-page-status)), allow filtering the pagetree for these statuses.
- If no page with the `status` attribute exists, the filter will not be rendered.
- Don't want the buttons? Hide them with some CSS:

    ```
    .pagetree-functions { display: none; }
    ```

- This plugin may not be compatible with the following MkDocs plugins:
    - [mkdocs-macros-plugin](https://github.com/fralau/mkdocs-macros-plugin)
    - [mkdocs-section-index](https://github.com/oprypin/mkdocs-section-index)

## Demo

### Code

<pre><code># docs_dir/file.md

&#123;&#123; pagetree &#125;&#125;
</code></pre>

### Rendered

{{ pagetree }}
