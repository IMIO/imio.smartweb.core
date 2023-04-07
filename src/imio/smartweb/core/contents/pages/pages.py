# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from zExceptions import BadRequest
from zope.interface import Interface
from zope.interface import implementer


class IPages(Interface):
    """Shared interface and schema for Pages"""


class IDefaultPages(Interface):
    """Marker interface for default Pages (used in Element view)"""


@implementer(IPages)
class Pages(Container):
    """Shared base class for Pages"""

    def checkValidId(self, id, allow_dup=0):
        if hasattr(self, id) and id not in self.contentIds():
            raise BadRequest()

    def canSetDefaultPage(self):
        return False
