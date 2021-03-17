# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from zope.interface import Interface
from zope.interface import implementer


class IPage(Interface):
    """Marker interface and Dexterity Python Schema for Page"""


@implementer(IPage)
class Page(Container):
    """Page class"""
