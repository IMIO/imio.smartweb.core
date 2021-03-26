# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.content import Container
from zope import schema
from zope.interface import implementer


class IPage(IPages):
    """Marker interface and Dexterity Python Schema for Page"""

    category = schema.Choice(title=_(u"Category"), source="collective.taxonomy.page")


@implementer(IPage)
class Page(Container):
    """Page class"""
