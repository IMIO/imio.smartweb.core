# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.contents.sections.views import SectionView
from plone.app.contenttypes.behaviors.richtext import IRichTextBehavior
from plone.app.textfield.value import RichTextValue
from plone.app.z3cform.widgets.richtext import get_tinymce_options
from plone import api

import json


class TextView(SectionView):
    """Gallery Section view"""

    def get_scale_url(self, item):
        scale = getattr(item, "image_scale", "section_text")
        return get_scale_url(item, self.request, "image", scale)


class InlineEditView(TextView):
    #: height (px) of the TinyMCE editing area
    editor_height = 500

    def can_edit(self):
        return api.user.has_permission(
            "Modify portal content", obj=aq_inner(self.context)
        )

    def tinymce_options(self):
        """Same pat-tinymce config as the standard Plone edit form."""
        options = get_tinymce_options(
            aq_inner(self.context), IRichTextBehavior["text"], self.request
        )
        # force the classic boxed editor (toolbar + fixed height) instead of
        # the "inline" mode which has no chrome and no height
        options["inline"] = False
        options.setdefault("tiny", {})["height"] = self.editor_height
        return json.dumps(options)

    def get_text(self):
        context = aq_inner(self.context)
        return context.text.raw if context.text else ""

    def save_text(self):
        context = aq_inner(self.context)
        new_text = self.request.form.get("newText", "")
        context.text = RichTextValue(new_text, "text/html", "text/html")
        context.reindexObject()
        return context.text.output
