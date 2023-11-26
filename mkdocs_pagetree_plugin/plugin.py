"""
MkDocs Pagetree Plugin
"""

import shutil
from pathlib import Path
from jinja2 import PackageLoader
from mkdocs.plugins import BasePlugin, get_plugin_logger


log = get_plugin_logger(__name__)


class PagetreePlugin(BasePlugin):

    def render_pagetree(self, pagetree, config):
        env = config.theme.get_env()
        env.loader = PackageLoader("mkdocs_pagetree_plugin")
        template = env.get_template("pagetree.html.j2")
        return template.render(pagetree=pagetree)

    def on_config(self, config, **kwargs):
        config["extra_javascript"] = ["js/mkdocs_pagetree_plugin.js"] + config[
            "extra_javascript"
        ]

        return config

    def on_nav(self, nav, config, files):
        self.pagetree = nav

    def on_post_page(self, output, page, config):
        marker = "{{ pagetree }}"
        if marker in output:
            log.debug(f"Found pagetree marker in {page.file.src_uri}")
            pagetree_rendered = self.render_pagetree(self.pagetree, config)
            return output.replace(marker, pagetree_rendered)

    def on_post_build(self, config):
        """
        Copy our javascript file
        """
        # Using this weird js filename to avoid a clash with js files
        # named identically from other plugins/themes.
        module_name = "mkdocs_pagetree_plugin"
        file = f"js/{module_name}.js"
        src_file_path = Path(Path.cwd() / module_name / file)
        dest_file_path = Path(config["site_dir"], file)
        shutil.copy(src_file_path, dest_file_path)
