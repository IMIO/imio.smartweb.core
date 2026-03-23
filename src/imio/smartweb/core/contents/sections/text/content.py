# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from zope import schema
from zope.interface import implementer


class ISectionText(ISection):
    """Marker interface and Dexterity Python Schema for SectionText"""

    # directives.widget(title=SuggestedIATitlesFieldWidget)
    # title = schema.TextLine(title=_("Title"), required=True)

    # We only want title from behavior (imio.smartweb.common ia)
    directives.omitted("title")

    directives.order_before(alignment="IVersionable.changeNote")
    alignment = schema.Choice(
        title=_("Image alignment"),
        description=_("Select where you want to display the image"),
        source="imio.smartweb.vocabulary.Alignment",
        default="left",
        required=True,
    )
    directives.order_after(image_scale="alignment")
    image_scale = schema.Choice(
        title=_("Image scale"),
        description=_("Select the image resolution to use"),
        source="imio.smartweb.vocabulary.SectionTextScale",
        default="section_text",
        required=True,
    )


@implementer(ISectionText)
class SectionText(Section):
    """SectionText class"""

    can_toggle_title_visibility = False
