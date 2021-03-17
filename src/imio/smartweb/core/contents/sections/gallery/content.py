# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from plone.dexterity.content import Container
from zope.interface import implementer


class ISectionGallery(ISection):
    """Marker interface and Dexterity Python Schema for SectionGallery"""


@implementer(ISectionGallery)
class SectionGallery(Container):
    """SectionGallery class"""
