# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
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
        path_brains = api.content.find(
            path={"query": path, "depth": 0},
        )
        quick_access_brains = api.content.find(UID=path_brains[0].related_quickaccess)
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

    def remove_items(self, iface, remove_self=False):
        """
        Remove element (based on its interface) children from navigation and
        also remove the element itself, if specified so
        """
        brains = api.content.find(object_provides=iface)
        paths = [b.getPath() for b in brains]
        to_delete = []
        for path in paths:
            if path in self.navtree:
                # Item representing the submenu of the matched element
                to_delete.append(path)
            for key in self.navtree.keys():
                if key.startswith("{}/".format(path)):
                    # Item representing a (grand)children of the matched element
                    to_delete.append(key)
            if remove_self:
                parent_path = "/".join(path.rsplit("/")[:-1])
                parent_navtree = self.navtree[parent_path]
                for i in range(len(parent_navtree)):
                    if parent_navtree[i]["path"] == path:
                        # Item representing the matched element
                        del parent_navtree[i]
                        break
        for key in to_delete:
            del self.navtree[key]

    def remove_minisites(self):
        """We need to remove minisites from navigation, only in main portal"""
        root = api.portal.get_navigation_root(self.context)
        if not IImioSmartwebMinisite.providedBy(root):
            self.remove_items(IImioSmartwebMinisite, remove_self=True)

    def remove_subsites_children(self):
        """We need to remove subsites children from navigation"""
        self.remove_items(IImioSmartwebSubsite)

    def build_tree(self, path, first_run=True):
        """We add quick access contents to the standard Plone navigation"""
        out = u""
        for item in self.navtree.get(path, []):
            out += self.render_item(item, path)

        if not first_run and out:
            out = self._subtree_markup_wrapper.format(out=out)
            # Quick accesses are displayed on every levels of the menu
            qa_out = self.build_quickaccess(path)
            if qa_out:
                out += self._quickaccesses_markup_wrapper.format(out=qa_out)
        return out

    def render_globalnav(self):
        self.remove_minisites()
        self.remove_subsites_children()
        return self.build_tree(self.navtree_path)
