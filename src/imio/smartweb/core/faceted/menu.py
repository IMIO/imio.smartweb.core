# -*- coding: utf-8 -*-

from plone.app.contentmenu.menu import DisplaySubMenuItem
from plone.memoize.instance import memoize


class CollectionDisplaySubMenuItem(DisplaySubMenuItem):
    @memoize
    def available(self):
        if self.disabled():
            return False
        return True
