"""
MkDocs Pagetree Plugin
"""

from jinja2 import PackageLoader
from mkdocs.plugins import BasePlugin, get_plugin_logger


log = get_plugin_logger(__name__)


class PagetreePlugin(BasePlugin):

    def render_pagetree(self, pagetree, config):
        env = config.theme.get_env()
        env.loader = PackageLoader("mkdocs_pagetree_plugin")
        template = env.get_template("pagetree.html.j2")
        return template.render(pagetree=pagetree)

    def on_nav(self, nav, config, files):
        self.pagetree = nav

    def on_post_page(self, output, page, config):
        marker = "{{ pagetree }}"
        if marker in output:
            log.debug(f"Found pagetree marker in {page.file.src_uri}")
            pagetree_rendered = self.render_pagetree(self.pagetree, config)
            return output.replace(marker, pagetree_rendered)

