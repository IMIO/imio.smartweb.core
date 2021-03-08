# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IPage(model.Schema):
    """Marker interface and Dexterity Python Schema for Page"""


@implementer(IPage)
class Page(Container):
    """Page class"""
