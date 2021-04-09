# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from zope.interface import implementer


class ISectionLinks(ISection):
    """Marker interface and Dexterity Python Schema for SectionFiles"""


@implementer(ISectionLinks)
class SectionLinks(Section):
    """SectionLinks class"""
