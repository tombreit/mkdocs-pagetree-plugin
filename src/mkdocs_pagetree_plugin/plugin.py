# SPDX-FileCopyrightText: 2023 Thomas Breitner
#
# SPDX-License-Identifier: MIT

"""
MkDocs Pagetree Plugin
"""

import re
from pathlib import Path
from jinja2 import PackageLoader

from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Section
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.utils import copy_file
from mkdocs.commands.build import get_context


log = get_plugin_logger(__name__)


SUPPORTED_TREE_OPTIONS = (
    "all",
    "children",
    "siblings",
    "subtree",
)

ASSETS = [
    "assets/mkdocs_pagetree_plugin.js",
    "assets/mkdocs_pagetree_plugin.css",
]


class PagetreePlugin(BasePlugin):
    def __init__(self):
        self.pagetree = []
        self.pagetree_all = []

    def on_nav(self, nav, config, files):
        self.pagetree_all = nav

    def _replace_marker_with_pagetree(
        self,
        output,
        page,
        config,
    ):
        marker_pattern = r"\{\{\s*pagetree(\(([a-z]*)\))?\s*\}\}"
        match = re.search(marker_pattern, output)

        if match and match.group():
            tree_option = match.group(2) if match.group(2) else "all"

            if tree_option not in SUPPORTED_TREE_OPTIONS:
                msg = f"""Page '{page}': Got unsupported pagetree option '{tree_option}'. Supported options: {', '.join(f"'{opt}'" for opt in SUPPORTED_TREE_OPTIONS)}"""
                log.warning(msg)
                raise PluginError(msg)

            log.debug(
                f"Found pagetree marker '{match.group()}' in '{page.file.src_uri}'"
            )

            if page.parent and tree_option == "subtree":
                # Sibling pages, child pages and the current page
                pagetree = page.parent.children
            elif page.parent and tree_option == "children":
                # Remove sibling pages of the current page, we are only
                # interessted in sub[sections|pages].
                pagetree = [i for i in page.parent.children if not isinstance(i, Page)]
            elif page.parent and tree_option == "siblings":
                # Remove sibling subsections of the current page, we are only
                # interessted in direct sibling pages.
                pagetree = [
                    i
                    for i in page.parent.children
                    if not any([isinstance(i, Section), i == page])
                ]
            else:
                # Without tree_option or without a parent page
                # (eg. the homepage) the default 'all' pagetree will be rendered.
                pagetree = self.pagetree_all

            env = config.theme.get_env()
            env.loader = PackageLoader("mkdocs_pagetree_plugin")
            template = env.get_template("pagetree.html.j2")
            context = get_context(None, None, config, page=page, base_url="/")

            context.update({"pagetree": pagetree})
            pagetree_rendered = template.render(context)

            output = output.replace(match.group(), pagetree_rendered)

        return output

    def on_post_page(self, output, page, config):
        return self._replace_marker_with_pagetree(output, page, config)

    def on_config(self, config):
        # Insert our assets to the corresponding config keys
        for asset in ASSETS:
            if asset.endswith(".js"):
                config["extra_javascript"] = [asset] + config["extra_javascript"]
            elif asset.endswith(".css"):
                config["extra_css"] = [asset] + config["extra_css"]

        return config

    def on_post_build(self, config):
        # Copy assets to the site directory
        current_dir = Path(__file__).parent
        for asset in ASSETS:
            src_file_path = current_dir / asset
            dest_file_path = Path(config["site_dir"], asset)
            copy_file(src_file_path, dest_file_path)
