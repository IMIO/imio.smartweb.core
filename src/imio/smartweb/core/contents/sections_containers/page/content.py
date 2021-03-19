# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import ISectionContainer
from plone.dexterity.content import Container
from zope.interface import implementer


class IPage(ISectionContainer):
    """Marker interface and Dexterity Python Schema for Page"""


@implementer(IPage)
class Page(Container):
    """Page class"""
