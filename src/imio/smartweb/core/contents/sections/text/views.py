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
    def can_edit(self):
        return api.user.has_permission(
            "Modify portal content", obj=aq_inner(self.context)
        )

    def tinymce_options(self):
        """Same pat-tinymce config as the standard Plone edit form, but
        chromeless: no toolbar/menu/status bar, just a text cursor. A small
        "quickbars" toolbar (bold, italic, link) pops up above the selection
        when some text is selected, instead of a permanently visible one.
        """
        options = get_tinymce_options(
            aq_inner(self.context), IRichTextBehavior["text"], self.request
        )
        options["inline"] = True
        tiny = options.setdefault("tiny", {})
        tiny["plugins"] = tiny.get("plugins", []) + ["quickbars"]
        tiny["toolbar"] = False
        tiny["menubar"] = False
        tiny["statusbar"] = False
        tiny["quickbars_insert_toolbar"] = False
        tiny["quickbars_selection_toolbar"] = "bold italic | plonelink unlink"
        # `content_css` (theme stylesheets) is meant to be loaded inside the
        # boxed editor's iframe so the WYSIWYG matches the front-end. Inline
        # mode has no iframe: TinyMCE would inject those stylesheets straight
        # into the page's <head>, duplicating the theme CSS site-wide. We
        # want the editable element to inherit the page's real CSS through
        # the normal cascade instead, so disable it entirely.
        tiny["content_css"] = False
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
