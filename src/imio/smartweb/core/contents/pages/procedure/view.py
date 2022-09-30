# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.pages.views import PagesView
from imio.smartweb.locales import SmartwebMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ProcedureView(PagesView):
    index = ViewPageTemplateFile("../view.pt")

    @property
    def no_items_message(self):
        return _("There is no section on this procedure.")
