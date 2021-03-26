# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from zope.interface import implementer


class ISectionGallery(ISection):
    """Marker interface and Dexterity Python Schema for SectionGallery"""


@implementer(ISectionGallery)
class SectionGallery(Section):
    """SectionGallery class"""
