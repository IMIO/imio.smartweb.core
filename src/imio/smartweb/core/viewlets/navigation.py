# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.viewlets.common import escape
from plone.app.layout.viewlets.common import GlobalSectionsViewlet
from plone.memoize.view import memoize
from Products.CMFPlone.utils import safe_unicode
from zope.i18n import translate

import Missing


class ImprovedGlobalSectionsViewlet(GlobalSectionsViewlet):
    _close_menu_markup = (
        '<a aria-label="{back}" class="prev-nav"><span>{back}</span></a>'
        '<a aria-label="{close}" class="close-nav"><span class="close-nav-icon"></span></a>'
    )
    _prev_menu_markup = (
        '<a aria-label="{back}" class="prev-nav"><span>{back}</span></a>'
    )
    _subtree_markup_wrapper = "<ul>{out}{qa_out}</ul>"
    _submenu_markup_wrapper = '<div class="has_subtree dropdown">{menu_action}<span class="nav-title"><a href="{url}">{title}</span></a>{sub}</div>'
    _quickaccesses_markup_wrapper = '<li class="quick-access"><span class="quick-access-title">{title}</span><ul>{out}</ul></li>'
    _item_markup_template = (
        '<li class="nav_{id}{has_sub_class} nav-item">'
        '<a href="{url}" class="state-{review_state} nav-link"{aria_haspopup}>{title}</a>{opener}'  # noqa: E 501
        "{sub_wrapper}"
        "</li>"
    )

    @property
    @memoize
    def root_depth(self):
        return len(self.nav_root.getPhysicalPath())

    @property
    @memoize
    def nav_root(self):
        return api.portal.get_navigation_root(self.context)

    @property
    @memoize
    def current_lang(self):
        current_lang = api.portal.get_current_language()[:2]
        return current_lang

    def render_quickaccess(self, item):
        return self._item_markup_template.format(**item)

    def render_item(self, item, path):
        sub = self.build_tree(item["path"], first_run=False)
        if sub:
            item.update(
                {
                    "sub": sub,
                    "sub_wrapper": "",
                    "menu_action": "",
                    "opener": self._opener_markup_template.format(**item),
                    "aria_haspopup": ' aria-haspopup="true"',
                    "has_sub_class": " has_subtree",
                }
            )
        else:
            item.update(
                {
                    "sub": sub,
                    "sub_wrapper": "",
                    "menu_action": "",
                    "opener": "",
                    "aria_haspopup": "",
                    "has_sub_class": "",
                }
            )

        if not sub:
            return self._item_markup_template.format(**item)

        level = len(item["path"].split("/")) - self.root_depth
        back_str = translate(_("Back"), target_language=self.current_lang)
        if level == 1:
            # We add "Back" & "Close" buttons on the first dropdown menu level
            close_str = translate(_("Close"), target_language=self.current_lang)
            item["menu_action"] = self._close_menu_markup.format(
                back=back_str, close=close_str
            )
        elif level > 1:
            # We add a "Back" button on the next dropdown menu levels
            item["menu_action"] = self._prev_menu_markup.format(back=back_str)
        item["sub_wrapper"] = self._submenu_markup_wrapper.format(**item)
        return self._item_markup_template.format(**item)

    def build_quickaccess(self, path):
        path_brains = api.content.find(
            path={"query": path, "depth": 0},
        )
        quick_access_uids = path_brains[0].related_quickaccess
        if quick_access_uids == Missing.Value:
            return ""
        quick_access_brains = api.content.find(UID=path_brains[0].related_quickaccess)
        out = ""
        for brain in quick_access_brains:
            entry = {
                "id": brain.getId,
                "path": brain.getPath(),
                "uid": brain.UID,
                "url": brain.getURL(),
                "title": escape(safe_unicode(brain.Title)),
                "review_state": brain.review_state,
                "sub": "",
                "sub_wrapper": "",
                "menu_action": "",
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
        brains = api.content.find(context=self.nav_root, object_provides=iface)
        paths = [b.getPath() for b in brains]
        if self.navtree_path in paths:
            # we never need to remove the root of the menu (ex: subsite menu)
            paths.remove(self.navtree_path)
        to_delete = set()
        for path in paths:
            if path in self.navtree:
                # Item representing the submenu of the matched element
                to_delete.add(path)
            for key in self.navtree.keys():
                if key.startswith("{}/".format(path)):
                    # Item representing a (grand)children of the matched element
                    to_delete.add(key)
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
        if not IImioSmartwebMinisite.providedBy(self.nav_root):
            self.remove_items(IImioSmartwebMinisite, remove_self=True)

    def remove_subsites_children(self):
        """We need to remove subsites children from navigation"""
        self.remove_items(IImioSmartwebSubsite)

    def build_tree(self, path, first_run=True):
        """We add quick access contents to the standard Plone navigation"""
        out = ""
        for item in self.navtree.get(path, []):
            out += self.render_item(item, path)

        if not first_run and out:
            # Quick accesses are displayed on every levels of the menu
            qa_menu = self.build_quickaccess(path)
            qa_out = ""
            if qa_menu:
                qa_out = self._quickaccesses_markup_wrapper.format(
                    title=translate(
                        _("Quick access"), target_language=self.current_lang
                    ),
                    out=qa_menu,
                )
            out = self._subtree_markup_wrapper.format(out=out, qa_out=qa_out)
        return out

    def render_globalnav(self):
        self.remove_minisites()
        self.remove_subsites_children()
        return self.build_tree(self.navtree_path)
