# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.cropping import SmartwebCroppingProvider
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from zope import schema
from zope.interface import implementer


class SectionTextCroppingProvider(SmartwebCroppingProvider):
    def get_scales(self, fieldname, request=None):
        if fieldname == "image":
            # scale used for lead image field
            return [self.context.image_size]
        else:
            return super(SectionTextCroppingProvider, self).get_scales(
                fieldname, request
            )


class ISectionText(ISection):
    """Marker interface and Dexterity Python Schema for SectionText"""

    directives.order_before(alignment="IVersionable.changeNote")
    alignment = schema.Choice(
        title=_("Image alignment"),
        description=_("Select where you want to display the image"),
        source="imio.smartweb.vocabulary.Alignment",
        default="left",
        required=True,
    )
    directives.order_after(image_size="alignment")
    image_size = schema.Choice(
        title=_("Image size"),
        description=_("Select image size"),
        source="imio.smartweb.vocabulary.ImageSize",
        default="preview",
        required=True,
    )


@implementer(ISectionText)
class SectionText(Section):
    """SectionText class"""

    can_toggle_title_visibility = False
