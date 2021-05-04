# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.common import (
    ContentViewsViewlet as ContentViewsViewletBase,
)


class ContentViewsViewlet(ContentViewsViewletBase):
    """Add preview action to primary actions to ensure ordering"""

    primary = ["folderContents", "edit", "view", "preview"]
