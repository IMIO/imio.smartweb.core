# -*- coding: utf-8 -*-

from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IProcedure(model.Schema):
    """Marker interface and Dexterity Python Schema for Procedure"""


@implementer(IProcedure)
class Procedure(Item):
    """Procedure class"""
