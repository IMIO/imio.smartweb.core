# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import ISectionContainer
from plone.dexterity.content import Container
from zope.interface import implementer


class IProcedure(ISectionContainer):
    """Marker interface and Dexterity Python Schema for Procedure"""


@implementer(IProcedure)
class Procedure(Container):
    """Procedure class"""
