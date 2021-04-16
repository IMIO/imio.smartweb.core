# -*- coding: utf-8 -*-

from plone import api
from plone.app.layout.viewlets.common import escape
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from Products.CMFPlone.utils import safe_unicode


class GlobalSectionsWithQuickAccessViewlet(GlobalSectionsViewlet):
    _quickaccesses_markup_wrapper = u'<ul class="quick-access">{out}</ul>'

    def render_quickaccess(self, item):
        if "title" in item and item["title"]:
            item["title"] = escape(item["title"])
        if "name" in item and item["name"]:
            item["name"] = escape(item["name"])
        return self._item_markup_template.format(**item)

    def build_quickaccess(self, path):
        quick_access_brains = api.content.find(
            path=path,
            include_in_quick_access=True,
            sort_on="sortable_title",
        )
        out = u""
        for brain in quick_access_brains:
            entry = {
                "id": brain.getId,
                "path": brain.getPath(),
                "uid": brain.UID,
                "url": brain.getURL(),
                "title": safe_unicode(brain.Title),
                "review_state": brain.review_state,
                "sub": "",
                "opener": "",
                "aria_haspopup": "",
                "has_sub_class": "",
            }
            out += self.render_quickaccess(entry)
        return out

    def build_tree(self, path, first_run=True):
        """We add quick access contents to the standard Plone navigation"""
        out = u""
        for item in self.navtree.get(path, []):
            out += self.render_item(item, path)

        if not first_run and out:
            out = self._subtree_markup_wrapper.format(out=out)
            item_level = path.count("/") - 1
            if item_level == self.navtree_depth - 1:
                # Only add quick accesses in the last level of the menu
                qa_out = self.build_quickaccess(path)
                if qa_out:
                    out += self._quickaccesses_markup_wrapper.format(out=qa_out)
        return out
