# -*- coding: utf-8 -*-

from plone.app.content.browser.contents.rearrange import OrderContentsBaseAction
from plone.app.content.utils import json_loads
from plone.app.contenttypes.browser.full_view import FullViewItem as BaseFullViewItem


class PageView(BaseFullViewItem):
    """Page view"""


class PageOrderingView(OrderContentsBaseAction):
    """Page sections ordering view"""

    def __call__(self):
        self.protect()
        form = self.request.form
        id = form.get("id")
        delta = int(form.get("delta"))
        ordering = self.getOrdering()
        ordered_ids = json_loads(form.get("orderedSectionsIds", "null"))
        if ordered_ids:
            position_id = [(ordering.getObjectPosition(i), i) for i in ordered_ids]
            position_id.sort()
            if ordered_ids != [i for position, i in position_id]:
                return
        ordering.moveObjectsByDelta([id], delta, ordered_ids)
