# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from imio.smartweb.core.contents import IPages
from zope.component import getMultiAdapter


class UtilsView(BrowserView):
    """ """

    def is_previewable_content(self):
        if not IPages.providedBy(self.context):
            return False

        context_state = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        )
        return context_state.is_view_template()
