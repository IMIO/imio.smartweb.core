# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from imio.smartweb.core.utils import can_edit_content
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.utils import release_lock
from imio.smartweb.core.contents.sections.views import SectionView
from plone.app.contenttypes.behaviors.richtext import IRichTextBehavior
from plone.app.textfield.value import RichTextValue
from plone.app.z3cform.widgets.richtext import get_tinymce_options

import json


class TextView(SectionView):
    """Gallery Section view"""

    def get_scale_url(self, item):
        scale = getattr(item, "image_scale", "section_text")
        return get_scale_url(item, self.request, "image", scale)


class InlineEditView(TextView):
    def can_edit(self):
        return can_edit_content(aq_inner(self.context))

    def tinymce_options(self):
        """Same pat-tinymce config as the standard Plone edit form, but
        chromeless: no toolbar/menu/status bar, just a text cursor. A small
        "quickbars" toolbar pops up above the selection when some text is
        selected, instead of a permanently visible one.
        """
        options = get_tinymce_options(
            aq_inner(self.context), IRichTextBehavior["text"], self.request
        )
        options["inline"] = True
        tiny = options.setdefault("tiny", {})
        # "lists" powers bullist/numlist below; it's normally already part of
        # Plone's default plugin list, but we add it explicitly (deduped)
        # since we can't rely on that default staying unchanged.
        plugins = tiny.get("plugins", []) + ["quickbars", "lists"]
        tiny["plugins"] = list(dict.fromkeys(plugins))
        tiny["toolbar"] = False
        tiny["menubar"] = False
        tiny["statusbar"] = False
        tiny["quickbars_insert_toolbar"] = False
        # h3/h4/h5: no h1/h2 here, the section's own title is already an
        # <h2> (see sections/macros.pt, section_title macro) - letting
        # editors pick h1/h2 in the body too would duplicate/confuse the
        # heading outline. "omnia" is iMio's AI assistant TinyMCE plugin
        # (imio.omnia.tinymce): it's installed site-wide and self-registers
        # via the standard plone.custom_plugins/custom_buttons registry
        # records, already merged into `tiny` above by get_tinymce_options().
        tiny["quickbars_selection_toolbar"] = (
            "bold italic underline | h3 h4 h5 | bullist numlist | "
            "plonelink unlink | omnia"
        )
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
        if not can_edit_content(context):
            # Section locked by another editor since the page was rendered:
            # ignore the write, return the text unchanged.
            return context.text.output if context.text else ""
        new_text = self.request.form.get("newText", "")
        context.text = RichTextValue(new_text, "text/html", "text/html")
        context.reindexObject()
        release_lock(context)
        return context.text.output
