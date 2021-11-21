# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.directives import write_permission
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class ISection(model.Schema):
    """Shared base marker interface and schema for Sections"""

    title = schema.TextLine(title=_(u"Title"), required=True)

    model.fieldset(
        "layout",
        label=_(u"Layout"),
        fields=[
            "hide_title",
            "collapsible_section",
            "background_image",
            "bootstrap_css_class",
            "css_class",
        ],
    )

    hide_title = schema.Bool(
        title=_(u"Hide title"),
        description=_(
            u"Hide title for anonymous user. Title stays visible for the editor."
        ),
        required=False,
        default=False,
    )

    collapsible_section = schema.Bool(
        title=_(
            u"Hide the content of the section that will be displayed by clicking on the title"
        ),
        description=_(
            u"The title will always be displayed if this behavior is enabled."
        ),
        required=False,
        default=False,
    )

    write_permission(background_image="cmf.ManagePortal")
    background_image = NamedBlobImage(
        title=_(u"Background image"),
        required=False,
    )

    bootstrap_css_class = schema.Choice(
        title=_(u"Section width"),
        required=False,
        vocabulary="imio.smartweb.vocabulary.BootstrapCSS",
    )

    write_permission(css_class="cmf.ManagePortal")
    css_class = schema.TextLine(title=_(u"CSS class"), required=False)


@implementer(ISection)
class Section(Container):
    """Shared base class for Sections"""

    manage_content = False
    manage_display = False
    can_toggle_title_visibility = True

    def canSetLayout(self):
        return False

    def canSetDefaultPage(self):
        return False
