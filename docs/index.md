# Home

MkDocs plugin that allows you to display the page tree. Like `sitemap.xml`, but for humans.

- [Repository](https://github.com/tombreit/mkdocs-pagetree-plugin)
- [Issues](https://github.com/tombreit/mkdocs-pagetree-plugin/issues)
- [PyPI package](https://pypi.org/project/mkdocs-pagetree-plugin/)

## Notes

- Only the first occurrence of the marker <code>&#123;&#123; pagetree &#125;&#125;</code> on a page is replaced.
- The plugin or marker can be used on several pages.
- If any page `status` is used ([Ref](https://squidfunk.github.io/mkdocs-material/reference/#setting-the-page-status)), allow filtering the pagetree for these statuses.
- If no page with the `status` attribute exists, the filter will not be rendered.
- The following tree options for the pagetree marker exists:
    - <code>&#123;&#123; pagetree(all) &#125;&#125;</code>: Render the whole pagetree. This is the default tree option, the `(all)` parameter can also be omitted.
    - <code>&#123;&#123; pagetree(children) &#125;&#125;</code>: Render only direct children of the current page
    - <code>&#123;&#123; pagetree(siblings) &#125;&#125;</code>: Render only direct siblings of the current page
    - <code>&#123;&#123; pagetree(subtree) &#125;&#125;</code>: Render the subtree which contains the current page

## Pagetree demo

### Code

<pre><code># docs_dir/file.md

&#123;&#123; pagetree &#125;&#125;
</code></pre>

### Rendered

{{ pagetree }}
