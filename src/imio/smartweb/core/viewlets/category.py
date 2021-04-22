# -*- coding: utf-8 -*-

from collective.taxonomy.interfaces import ITaxonomy
from plone import api
from plone.app.layout.viewlets import common
from Products.CMFPlone.utils import base_hasattr
from zope.component import getSiteManager


class CategoryViewlet(common.ViewletBase):
    def available(self):
        if not base_hasattr(self.context, "category"):
            return False
        return self.context.category is not None

    def get_category(self):
        if not base_hasattr(self.context, "category_taxonomy"):
            return self.context.category
        term = self.context.category
        taxonomy_name = self.context.category_taxonomy
        current_lang = api.portal.get_current_language()[:2]
        sm = getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=taxonomy_name)
        value = utility.translate(
            term,
            context=self.context,
            target_language=current_lang,
        )
        return value
