# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope.interface import implementer
from zope import schema


class ISectionMap(ISection):
    """Marker interface and Dexterity Python Schema for SectionMap"""


@implementer(ISectionMap)
class SectionMap(Section):
    """SectionMap class"""
