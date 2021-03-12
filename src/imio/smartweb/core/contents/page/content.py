# -*- coding: utf-8 -*-

from collective.behavior.gallery.behaviors.folderish_gallery import IFolderishGallery
from plone.dexterity.content import Container
from zope.interface import implementer


class IPage(IFolderishGallery):
    """Marker interface and Dexterity Python Schema for Page"""


@implementer(IPage)
class Page(Container):
    """Page class"""
