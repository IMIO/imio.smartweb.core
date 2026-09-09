# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from imio.smartweb.core.utils import can_edit_content
from imio.smartweb.core.utils import release_lock
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
        return can_edit_content(aq_inner(self.context))


class SaveTitleView(BrowserView):
    """htmx endpoint: stores the new title sent by @@inline_title"""

    def __call__(self):
        context = aq_inner(self.context)
        if not can_edit_content(context):
            # Locked by another editor since the page was rendered: ignore
            # the write, return the title unchanged.
            return context.Title()
        new_title = self.request.form.get("newTitle", "").strip()
        if new_title and new_title != context.Title():
            context.setTitle(new_title)
            context.reindexObject(idxs=["Title", "sortable_title", "SearchableText"])
        release_lock(context)
        return context.Title()
