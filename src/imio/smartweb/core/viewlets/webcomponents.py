# -*- coding: utf-8 -*-

from imio.smartweb.core import config
from plone.app.layout.viewlets import common


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
