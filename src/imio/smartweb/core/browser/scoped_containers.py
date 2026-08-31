# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from imio.smartweb.core.utils import get_agenda_scope
from imio.smartweb.core.utils import get_newsfolder_scope
from plone import api
from Products.Five.browser import BrowserView

import json


class _ScopedContainersView(BrowserView):
    """Containers a given rest view is able to display, as JSON.

    Consumed by browser/static/src/edit.js to repopulate the container options
    when the editor picks another linking view, before anything is saved -- a
    vocabulary can only ever see the stored value.
    """

    portal_type = None
    container_field = None
    scope_getter = None

    def __call__(self):
        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )
        uid = self.request.form.get("linking_rest_view")
        if not uid:
            return json.dumps([])
        # Resolved with the editor's own permissions, exactly like
        # get_linking_rest_view() does for the vocabularies and the invariants:
        # if the two disagreed, the cascade would empty a <select> the server
        # would have accepted, or offer containers it then refuses.
        try:
            rest_view = api.content.get(UID=uid)
        except Unauthorized:
            rest_view = None
        if rest_view is None or rest_view.portal_type != self.portal_type:
            return json.dumps([])
        scope = self.scope_getter(getattr(rest_view, self.container_field, None))
        return json.dumps(
            [{"id": item_uid, "text": title} for item_uid, title in scope]
        )


class ScopedAgendasView(_ScopedContainersView):
    """Agendas a given EventsView is able to display, as JSON."""

    portal_type = "imio.smartweb.EventsView"
    container_field = "selected_agenda"
    scope_getter = staticmethod(get_agenda_scope)


class ScopedNewsFoldersView(_ScopedContainersView):
    """News folders a given NewsView is able to display, as JSON."""

    portal_type = "imio.smartweb.NewsView"
    container_field = "selected_news_folder"
    scope_getter = staticmethod(get_newsfolder_scope)
