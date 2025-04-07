# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import (
    CampaignView,
    DirectoryView,
    EventsView,
    NewsView,
)
from plone.app.contentmenu.menu import ActionsSubMenuItem as BaseActionsSubMenuItem
from plone.app.contentmenu.menu import DisplaySubMenuItem as BaseDisplaySubMenuItem
from plone.app.layout.viewlets.common import (
    ContentViewsViewlet as BaseContentViewsViewlet,
)
from plone.memoize.instance import memoize


class ContentViewsViewlet(BaseContentViewsViewlet):
    """Add preview action to primary actions to ensure ordering"""

    primary = ["folderContents", "edit", "view", "preview"]


class ExcludeSubMenuForCertainTypesMixin:
    """Mixin pour exclure certaines vues des sous-menus."""

    excluded_views = (CampaignView, DirectoryView, EventsView, NewsView)

    @memoize
    def available(self):
        return super().available() and not isinstance(self.context, self.excluded_views)


class ActionsSubMenuItem(ExcludeSubMenuForCertainTypesMixin, BaseActionsSubMenuItem):
    """Don't show actions sub-menu for authentic sources views."""


class DisplaySubMenuItem(ExcludeSubMenuForCertainTypesMixin, BaseDisplaySubMenuItem):
    """Don't show display sub-menu for authentic sources views."""
