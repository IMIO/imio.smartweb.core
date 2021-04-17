# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from plone import api
from plone.app.layout.viewlets.common import escape
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from Products.CMFPlone.utils import safe_unicode


class GlobalSectionsWithQuickAccessViewlet(GlobalSectionsViewlet):
    _quickaccesses_markup_wrapper = u'<ul class="quick-access">{out}</ul>'

    def render_quickaccess(self, item):
        if item["title"]:
            item["title"] = escape(item["title"])
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

    def remove_subsites_children(self):
        """We need to remove subsites children from navigation"""
        subsites_brains = api.content.find(object_provides=IImioSmartwebSubsite)
        subsites_paths = [b.getPath() for b in subsites_brains]
        to_delete = []
        for path in subsites_paths:
            if path in self.navtree:
                # Item representing the subsite submenu
                to_delete.append(path)
            for key in self.navtree.keys():
                if key.startswith("{}/".format(path)):
                    # Item representing a (grand)children of a subsite
                    to_delete.append(key)
        for key in to_delete:
            del self.navtree[key]

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

    def render_globalnav(self):
        self.remove_subsites_children()
        return self.build_tree(self.navtree_path)
