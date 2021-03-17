# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from plone.dexterity.content import Container
from zope.interface import implementer


class ISectionText(ISection):
    """Marker interface and Dexterity Python Schema for SectionText"""


@implementer(ISectionText)
class SectionText(Container):
    """SectionText class"""
