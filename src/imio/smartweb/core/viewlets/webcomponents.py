# -*- coding: utf-8 -*-

from imio.smartweb.core import config
from plone.app.layout.viewlets import common

import pkg_resources


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
    def bundle_version(self):
        """Cache-busting token for the production entry script's URL.

        Unlike bundles served through Plone's resource registry, this ES
        module is loaded via a hand-written <script> tag pointing at a
        fixed, unhashed filename (see webcomponents_js_header.pt), so it
        never gets the registry's automatic ++unique++ cache-busting
        prefix. Appending the package version as a query string forces
        browsers, Varnish and CDNs to fetch a fresh copy on every release
        instead of serving a stale entry point that references
        already-deleted, content-hashed chunk files from a previous build.
        """
        return pkg_resources.get_distribution("imio.smartweb.core").version
