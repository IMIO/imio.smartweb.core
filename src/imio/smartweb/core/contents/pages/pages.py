# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs
from zope.interface import Interface
from zope.interface import implementer


class IPages(Interface):
    """ Shared mecanism for Pages """


# Interface pour marquer la page par défaut sur un dossier
# Grâce à IHideFromBreadcrumbs, dans le breadcrumbs, la page sera cachée.
class IDefaultPages(IHideFromBreadcrumbs):
    """"""


@implementer(IPages)
class Pages(Container):
    """ Shared mecanism for Pages """

    def canSetDefaultPage(self):
        return False
