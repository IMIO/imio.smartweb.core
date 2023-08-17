# -*- coding: utf-8 -*-

from zope.browsermenu.interfaces import IBrowserMenu
from zope.browsermenu.interfaces import IBrowserSubMenuItem


class IAuthenticSourcesMenu(IBrowserMenu):
    """The authentic sources menu."""


class ISmartwebHelpMenu(IBrowserMenu):
    """The smartweb help menu."""


class IAuthenticSourcesSubMenuItem(IBrowserSubMenuItem):
    """The authentic sources submenu item."""


class ISmartwebHelpSubMenuItem(IBrowserSubMenuItem):
    """The smartweb help submenu item."""
