# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from zope.interface import implementer


class ISectionMap(ISection):
    """Marker interface and Dexterity Python Schema for SectionMap"""


@implementer(ISectionMap)
class SectionMap(Section):
    """SectionMap class"""
