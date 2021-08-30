# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IEventsView(model.Schema):
    """ """


@implementer(IEventsView)
class EventsView(Container):
    """EventsView class"""
