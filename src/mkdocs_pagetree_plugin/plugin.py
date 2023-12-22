# SPDX-FileCopyrightText: 2023 Thomas Breitner
#
# SPDX-License-Identifier: MIT

"""
MkDocs Pagetree Plugin
"""

from pathlib import Path
from jinja2 import PackageLoader
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.utils import copy_file
from mkdocs.commands.build import get_context


log = get_plugin_logger(__name__)


class PagetreePlugin(BasePlugin):
    def render_pagetree(self, pagetree, config, page):
        env = config.theme.get_env()
        env.loader = PackageLoader("mkdocs_pagetree_plugin")
        template = env.get_template("pagetree.html.j2")
        context = get_context(None, None, config, page=page, base_url="/")
        context["pagetree"] = pagetree
        return template.render(context)

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
            pagetree_rendered = self.render_pagetree(self.pagetree, config, page)
            return output.replace(marker, pagetree_rendered)

    def on_post_build(self, config):
        """
        Copy our javascript file
        """
        # Using this weird js filename to avoid a clash with js files
        # named identically from other plugins/themes.
        module_name = "mkdocs_pagetree_plugin"
        file = f"js/{module_name}.js"
        current_dir = Path(__file__).parent
        src_file_path = current_dir / file
        dest_file_path = Path(config["site_dir"], file)
        copy_file(src_file_path, dest_file_path)
