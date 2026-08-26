# -*- coding: utf-8 -*-

from functools import lru_cache
from imio.smartweb.core import config
from plone.app.layout.viewlets import common

import json
import logging
import os


logger = logging.getLogger(__name__)

# .../imio/smartweb/core/webcomponents/build/.vite/manifest.json
_MANIFEST_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "webcomponents",
    "build",
    ".vite",
    "manifest.json",
)
_FALLBACK_ENTRY = "js/smartweb-webcomponents-compiled.js"


@lru_cache(maxsize=1)
def _entry_script_path():
    """Path (relative to the built bundle's root) of the current,
    content-hashed entry script, resolved from Vite's build manifest.

    Every lazy-loaded widget chunk imports shared symbols (React's jsx
    runtime, moment, ...) back from the entry chunk through a relative
    URL that Rollup bakes into the chunk at build time, e.g.
    "../smartweb-webcomponents-compiled-<hash>.js". The <script> tag
    that loads the entry point (webcomponents_js_header.pt) must
    therefore reference that exact same file -- using a different URL
    for the two (e.g. a fixed filename plus an ad-hoc "?v=" query
    string) makes the browser treat them as two distinct modules,
    fetching and re-running the entry's top-level code twice and
    raising "already defined as a custom element". Reading the actual
    built filename from the manifest instead of hardcoding one keeps
    both references in sync automatically, and still busts the cache on
    every content change since the hash is part of the path itself.

    Cached for the lifetime of the process: the manifest only changes
    with a new `npm run build`, which requires a restart to pick up
    anyway (the built assets are read once from disk into memory-mapped
    resource directories).
    """
    try:
        with open(_MANIFEST_PATH) as manifest_file:
            manifest = json.load(manifest_file)
        return manifest["src/index.jsx"]["file"]
    except (OSError, KeyError, ValueError):
        logger.warning(
            "Could not resolve the webcomponents entry script from %s, "
            "falling back to the fixed, non-hashed filename.",
            _MANIFEST_PATH,
        )
        return _FALLBACK_ENTRY


class WebComponentsViewlet(common.ViewletBase):
    """Loads the smartweb webcomponents bundle.

    In production, the built ES module bundle is loaded through the
    resource registry's static directory. During development, if
    VITE_DEV_URL is set, the source entry point is loaded directly from
    the Vite dev server instead, enabling real HMR.
    """

    @property
    def vite_dev_url(self):
        return config.VITE_DEV_URL

    @property
    def entry_script_path(self):
        return _entry_script_path()
