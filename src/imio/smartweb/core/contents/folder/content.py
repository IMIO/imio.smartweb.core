# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IFolder(model.Schema):
    """Marker interface and Dexterity Python Schema for Folder"""


@implementer(IFolder)
class Folder(Container):
    """Folder class"""
