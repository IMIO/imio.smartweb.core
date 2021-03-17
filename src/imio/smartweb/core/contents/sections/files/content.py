# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from plone.dexterity.content import Container
from zope.interface import implementer


class ISectionFiles(ISection):
    """Marker interface and Dexterity Python Schema for SectionFiles"""


@implementer(ISectionFiles)
class SectionFiles(Container):
    """SectionText class"""
