# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class INewsView(model.Schema):
    """ """


@implementer(INewsView)
class NewsView(Container):
    """NewsView class"""
