# MkDocs Pagetree Plugin

MkDocs plugin that allows you to display the page tree. Like `sitemap.xml`, but for humans.

- [Repository](https://github.com/tombreit/mkdocs-pagetree-plugin)
- [Issues](https://github.com/tombreit/mkdocs-pagetree-plugin/issues)
- [PyPI package](https://pypi.org/project/mkdocs-pagetree-plugin/)

## Options

The following tree options for the pagetree marker exists:

- <strong><code>&#123;&#123; pagetree(all) &#125;&#125;</code></strong>

    Render the whole pagetree. This is the default tree option, the `(all)` parameter can also be omitted.

- <strong><code>&#123;&#123; pagetree(children) &#125;&#125;</code></strong>

    Render only direct children of the current page

- <strong><code>&#123;&#123; pagetree(siblings) &#125;&#125;</code></strong>

    Render only direct siblings of the current page, excluding the current page

- <strong><code>&#123;&#123; pagetree(subtree) &#125;&#125;</code></strong>

    Render the subtree which contains the current page

## Plugin Compatibility

### Using with mkdocs-macros-plugin

The `pagetree` plugin uses the <code>&#123;&#123; pagetree &#125;&#125;</code> syntax which resembles Jinja2 template variables. This can cause compatibility issues with plugins like [mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/) that process Jinja2 templates.

**Important:** The plugin order in your `mkdocs.yml` matters!

#### Recommended Configuration

Place `pagetree` **before** `macros` in your plugin list:

```yaml
plugins:
  - pagetree
  - macros
```

This ensures that the <code>&#123;&#123; pagetree &#125;&#125;</code> marker is processed by the pagetree plugin during the `on_post_page` event, after macros has already processed the page content during the `page_markdown` event.

#### Why Order Matters

- **mkdocs-macros-plugin** processes Jinja2 templates during the `page_markdown` event (before HTML rendering)
- **mkdocs-pagetree-plugin** replaces the <code>&#123;&#123; pagetree &#125;&#125;</code> marker during the `on_post_page` event (after HTML rendering)

If `macros` is listed first and configured with strict undefined handling, it will fail with an error like:

```
UndefinedError: 'pagetree' is undefined
```

This happens because `macros` tries to render <code>&#123;&#123; pagetree &#125;&#125;</code> as a Jinja2 variable that doesn't exist in its context.

#### Alternative: Using Both Plugins

If you need both plugins and prefer to have `macros` listed first, you can work around this by:

1. Configuring macros to use lenient undefined handling (default behavior):

```yaml
plugins:
  - macros:
      on_undefined: lenient  # or omit this line for default behavior
  - pagetree
```

2. Or by escaping the pagetree marker in your content:

<pre><code>{% raw %}&#123;&#123; pagetree &#125;&#125;{% endraw %}</code></pre>

However, the recommended approach is to simply place `pagetree` before `macros` in your plugin list.

## Notes

- The plugin or marker can be used on several pages.
- Only the first occurrence of the marker <code>&#123;&#123; pagetree &#125;&#125;</code> on a page is replaced.
- If any page `status` is used ([Ref](https://squidfunk.github.io/mkdocs-material/reference/#setting-the-page-status)), allow filtering the pagetree for these statuses.
- If no page with the `status` attribute exists, the filter will not be rendered.

## Demo

### Code

<pre><code># docs_dir/file.md

&#123;&#123; pagetree &#125;&#125;
</code></pre>

### Rendered

{{ pagetree }}
