# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from html import escape
from html import unescape
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.contents.sections.views import SectionView
from plone.app.textfield.value import RichTextValue
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class TextView(SectionView):
    """Gallery Section view"""

    def get_scale_url(self, item):
        request = self.request
        scale = self.context.image_size
        return get_scale_url(item, request, "image", scale, "paysage")


class InlineEditView(TextView):
    def get_text(self):
        context = aq_inner(self.context)
        editable_text = context.text.output
        return escape(editable_text).strip()

    def save_text(self):
        context = aq_inner(self.context)
        new_text = context.REQUEST.form.get("newText", "")
        context.text = RichTextValue(unescape(new_text), "text/html", "text/html")
        context.reindexObject()
        return context.text.output
