# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope import schema
from zope.interface import implementer


class ISectionHTML(ISection):
    """Marker interface and Dexterity Python Schema for SectionHTML"""

    html = schema.SourceText(
        title=_(u"HTML"),
        description=_(u"Structure your content directly with html."),
        required=True,
    )


@implementer(ISectionHTML)
class SectionHTML(Section):
    """SectionHTML class"""
