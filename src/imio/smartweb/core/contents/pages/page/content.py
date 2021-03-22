# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from plone.dexterity.content import Container
from zope.interface import implementer


class IPage(IPages):
    """Marker interface and Dexterity Python Schema for Page"""


@implementer(IPage)
class Page(Container):
    """Page class"""
