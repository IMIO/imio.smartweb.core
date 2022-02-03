# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from zope.interface import implementer


class IPage(IPages):
    """Marker interface and Dexterity Python Schema for Page"""


@implementer(IPage, IInstanceBehaviorAssignableContent)
class Page(Pages):
    """Page class"""

    category_name = "page_category"
