# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from plone import api
from Products.Five import BrowserView


class InlineTitleView(BrowserView):
    """Renders a title, made contenteditable + htmx-aware for editors.

    Used from every template that displays a title (sections, pages, folders)
    so the inline edition logic lives in a single place.
    """

    def __call__(self):
        # inlined in <h1>/<h2>: no surrounding whitespace
        return super().__call__().strip()

    def can_edit(self):
        return api.user.has_permission(
            "Modify portal content", obj=aq_inner(self.context)
        )


class SaveTitleView(BrowserView):
    """htmx endpoint: stores the new title sent by @@inline_title"""

    def __call__(self):
        context = aq_inner(self.context)
        new_title = self.request.form.get("newTitle", "").strip()
        if new_title and new_title != context.Title():
            context.setTitle(new_title)
            context.reindexObject(idxs=["Title", "sortable_title", "SearchableText"])
        return context.Title()
