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

## Pagetree demo

### Code

<pre><code># docs_dir/file.md

&#123;&#123; pagetree &#125;&#125;
</code></pre>

### Rendered

{{ pagetree }}
