# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from zope.interface import implementer


class ISectionFiles(ISection):
    """Marker interface and Dexterity Python Schema for SectionFiles"""


@implementer(ISectionFiles)
class SectionFiles(Section):
    """SectionText class"""
