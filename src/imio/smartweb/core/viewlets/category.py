# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import get_category
from plone.app.layout.viewlets import common


class CategoryViewlet(common.ViewletBase):
    def available(self):
        return self.get_category() is not None

    def get_category(self):
        return get_category(self.context)
