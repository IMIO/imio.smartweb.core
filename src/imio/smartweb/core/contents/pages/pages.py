# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from zope.interface import Interface
from zope.interface import implementer


class IPages(Interface):
    """ Shared mecanism for Pages """


@implementer(IPages)
class Pages(Container):
    """ Shared mecanism for Pages """

    def canSetDefaultPage(self):
        return False
