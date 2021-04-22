# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.supermodel import model
from zope.interface import implementer
from zope import schema


class ISectionLinks(ISection):
    """Marker interface and Dexterity Python Schema for SectionFiles"""

    model.fieldset("layout", fields=["image_scale"])
    image_scale = schema.Choice(
        title=_(u"Image scale"),
        default=u"tile",
        vocabulary="plone.app.vocabularies.ImagesScales",
        required=True,
    )


@implementer(ISectionLinks)
class SectionLinks(Section):
    """SectionLinks class"""

    manage_content = True
    manage_display = True
