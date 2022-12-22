# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from collective.messagesviewlet.message import add_timezone
from collective.messagesviewlet.utils import add_message
from datetime import datetime
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.viewlets.logo import LogoViewlet
from imio.smartweb.core.viewlets.messages import MessagesViewlet
from imio.smartweb.core.viewlets.minisite import MinisitePortalLinkViewlet
from imio.smartweb.core.viewlets.navigation import ImprovedGlobalSectionsViewlet
from imio.smartweb.core.tests.utils import make_named_image
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import setRoles
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from plone.testing.zope import Browser
from plone.namedfile.file import NamedBlobImage
from unittest import mock
from unittest.mock import patch
from z3c.relationfield import RelationValue
from zope.annotation import IAnnotations
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

import transaction


class TestMinisite(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        self.message_config_folder = self.portal["messages-config"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
            id="folder",
        )
        # avoid cached empty value for instance behaviors
        delattr(self.request, ASSIGNABLE_CACHE_KEY)

    def _clean_cache(self):
        # utils.get_messages_to_show is cached, remove infos in request annotation
        cache_keys = [
            k
            for k in IAnnotations(self.request)
            if k.startswith("messagesviewlet-utils-get_messages_to_show-")
        ]
        for cache_key in cache_keys:
            del IAnnotations(self.request)[cache_key]

    def test_activation(self):
        view = getMultiAdapter((self.portal, self.request), name="minisite_settings")
        self.assertFalse(view.available())

        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        self.assertTrue(view.available())
        self.assertFalse(view.enabled())

        view.enable()
        self.assertTrue(IImioSmartwebMinisite.providedBy(self.folder))
        self.assertTrue(INavigationRoot.providedBy(self.folder))

        self.assertFalse(view.available())
        self.assertTrue(view.enabled())

        view.disable()
        self.assertFalse(IImioSmartwebMinisite.providedBy(self.folder))
        self.assertFalse(INavigationRoot.providedBy(self.folder))
        self.assertTrue(view.available())
        self.assertFalse(view.enabled())

        subsite_view = getMultiAdapter(
            (self.folder, self.request), name="subsite_settings"
        )
        subsite_view.enable()
        self.assertFalse(view.available())

        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
            id="subfolder",
        )
        view = getMultiAdapter((subfolder, self.request), name="minisite_settings")
        self.assertFalse(view.available())
        view.enable()
        self.assertFalse(view.enabled())

    def test_minisite_exclude_from_nav(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        self.assertTrue(IImioSmartwebMinisite.providedBy(self.folder))
        self.assertTrue(self.folder.exclude_from_nav)

        transaction.commit()
        browser = Browser(self.layer["app"])
        browser.addHeader(
            "Authorization",
            "Basic %s:%s"
            % (
                TEST_USER_NAME,
                TEST_USER_PASSWORD,
            ),
        )
        browser.open("{}/edit".format(self.folder.absolute_url()))
        content = browser.contents
        soup = BeautifulSoup(content)
        exclude_from_nav_widget = soup.find(
            id="form-widgets-IExcludeFromNavigation-exclude_from_nav"
        )
        self.assertIsNone(exclude_from_nav_widget.find("input"))
        children = [
            c for c in exclude_from_nav_widget if not isinstance(c, str) or c.strip()
        ]
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0].text, "yes")

    def test_minisite_navigation(self):
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
            id="subfolder",
        )
        api.content.create(
            container=subfolder,
            type="imio.smartweb.Page",
            title="Subpage",
            id="subpage",
        )
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        viewlet = ImprovedGlobalSectionsViewlet(self.folder, self.request, None, None)
        viewlet.update()
        viewlet.remove_minisites()
        self.assertEqual(len(viewlet.navtree), 2)
        self.assertEqual(len(viewlet.navtree["/plone/folder"]), 2)
        self.assertIn("subfolder", viewlet.render_globalnav())
        self.assertIn("subpage", viewlet.render_globalnav())

    def test_quick_accesses(self):
        api.portal.set_registry_record("plone.navigation_depth", 5)
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder level 2",
        )
        api.content.create(
            container=subfolder,
            type="imio.smartweb.Folder",
            title="Subfolder level 3 (to display submenu)",
        )
        page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Quick Page everywhere",
        )
        page_sub = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Quick Page Sub",
        )
        viewlet = ImprovedGlobalSectionsViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertNotIn('<li class="quick-access">', viewlet.render_globalnav())

        # Quick access on minisite folder
        intids = getUtility(IIntIds)
        self.folder.quick_access_items = [
            RelationValue(intids.getId(page)),
        ]
        self.folder.reindexObject()
        html = viewlet.render_globalnav()
        self.assertNotIn('<li class="quick-access">', viewlet.render_globalnav())

        # Quick access on second level folder
        intids = getUtility(IIntIds)
        subfolder.quick_access_items = [
            RelationValue(intids.getId(page)),
            RelationValue(intids.getId(page_sub)),
        ]
        subfolder.reindexObject()
        html = viewlet.render_globalnav()
        self.assertIn('<li class="quick-access">', viewlet.render_globalnav())

        soup = BeautifulSoup(html)
        qa = soup.find("li", {"class": "nav_subfolder-level-2"}).find(
            "li", {"class": "quick-access"}
        )

        self.assertEqual(len(qa.find_all("li")), 2)
        self.assertIsNotNone(qa.find("li", {"class": "nav_quick-page-sub"}))

    def test_delete_minisite(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        api.content.delete(self.folder)

    def test_move_minisite_in_folder(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        folder2 = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder2",
            id="folder2",
        )
        moved_folder = api.content.move(self.folder, folder2)
        view = getMultiAdapter((moved_folder, self.request), name="minisite_settings")
        self.assertFalse(view.available())
        self.assertFalse(view.enabled())
        self.assertFalse(IImioSmartwebMinisite.providedBy(moved_folder))

    def test_copy_minisite_in_folder(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        folder2 = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder2",
            id="folder2",
        )
        copied_folder = api.content.copy(self.folder, folder2)
        view = getMultiAdapter((copied_folder, self.request), name="minisite_settings")
        self.assertFalse(view.available())
        self.assertFalse(view.enabled())
        self.assertFalse(IImioSmartwebMinisite.providedBy(copied_folder))

    def test_minisite_in_minisite(self):
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        self.assertTrue(IImioSmartwebMinisite.providedBy(self.folder))

        minisite2 = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="minisite2",
            id="minisite2",
        )
        view = getMultiAdapter((minisite2, self.request), name="minisite_settings")
        self.assertFalse(view.available())

    def test_cannot_enable_minisite_on_subsite(self):
        subsite_view = getMultiAdapter(
            (self.folder, self.request), name="subsite_settings"
        )
        subsite_view.enable()
        minisite_view = getMultiAdapter(
            (self.folder, self.request), name="minisite_settings"
        )
        self.assertFalse(minisite_view.available())
        self.assertFalse(minisite_view.enabled())
        minisite_view.enable()
        self.assertFalse(minisite_view.enabled())

    def test_minisite_viewlet_logo(self):
        viewlet = LogoViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.show_title)
        self.assertTrue(viewlet.show_logo)
        self.assertFalse(viewlet.is_svg)
        self.assertEqual(viewlet.navigation_root_url, "http://nohost/plone")
        html = viewlet.render()
        soup = BeautifulSoup(html)
        img = soup.find("img")
        self.assertEqual(
            img.get("src"), "http://nohost/plone/++resource++plone-logo.svg"
        )
        annotations = IAnnotations(self.request)
        del annotations["plone.memoize"]
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        viewlet = LogoViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.navigation_root_url, "http://nohost/plone/folder")
        self.assertTrue(viewlet.show_title)
        self.assertFalse(viewlet.show_logo)
        self.folder.logo_display_mode = "logo"
        viewlet.update()
        self.assertFalse(viewlet.show_title)
        self.assertFalse(viewlet.show_logo)
        self.folder.logo_display_mode = "logo_title"
        viewlet.update()
        self.assertTrue(viewlet.show_title)
        self.assertFalse(viewlet.show_logo)
        self.folder.logo = NamedBlobImage(**make_named_image("plone.svg"))
        viewlet.update()
        self.assertTrue(viewlet.show_logo)
        self.assertTrue(viewlet.is_svg)
        self.assertIn(b"<svg", viewlet.svg_data)
        self.folder.logo = NamedBlobImage(**make_named_image("plone.png"))
        viewlet = LogoViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.show_logo)
        self.assertFalse(viewlet.is_svg)
        self.folder.logo_display_mode = "logo"
        viewlet.update()
        self.assertTrue(viewlet.show_logo)
        html = viewlet.render()
        soup = BeautifulSoup(html)
        img = soup.find("img")
        self.assertIn("http://nohost/plone/folder/@@images/", img.get("src"))

        # Title should remain the same on sub-contents
        subfolder = api.content.create(
            container=self.folder,
            type="imio.smartweb.Folder",
            title="Subfolder",
        )
        viewlet = LogoViewlet(subfolder, self.request, None, None)
        viewlet.update()
        self.assertEqual(viewlet.navigation_root_url, "http://nohost/plone/folder")

    def test_minisite_body_class(self):
        page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            title="Subpage",
            id="subpage",
        )
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        template = self.folder.restrictedTraverse("view")
        layout_view = page.restrictedTraverse("@@plone_layout")
        body_class = layout_view.bodyClass(template, view)
        self.assertIn("is-in-minisite", body_class)

        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.disable()
        layout_view = page.restrictedTraverse("@@plone_layout")
        body_class = layout_view.bodyClass(template, view)
        self.assertNotIn("is-in-minisite", body_class)

    def test_portal_link_viewlet(self):
        viewlet = MinisitePortalLinkViewlet(self.folder, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available())
        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        view.enable()
        self.assertTrue(viewlet.available())
        attr = {"absolute_url.return_value": "http://www.test.be/folder/minisite"}
        with patch("plone.api.portal.get", return_value=mock.Mock(**attr)):
            self.assertEqual(viewlet.get_hostname(), "test.be")
        attr = {"absolute_url.return_value": "http://test.be/folder/minisite"}
        with patch("plone.api.portal.get", return_value=mock.Mock(**attr)):
            self.assertEqual(viewlet.get_hostname(), "test.be")
        attr = {"absolute_url.return_value": "http://sub.test.be/folder/minisite"}
        with patch("plone.api.portal.get", return_value=mock.Mock(**attr)):
            self.assertEqual(viewlet.get_hostname(), "sub.test.be")

    def test_messagesviewlet_in_minisite(self):
        message = add_message(
            "msg",
            "My message title",
            "My message text",
            start=add_timezone(datetime(2019, 10, 26, 12, 0)),
        )
        viewlet = MessagesViewlet(self.folder, self.portal.REQUEST, None, None)
        viewlet.update()
        # no message in viewlet because the message is in "inactive" state
        self.assertEqual(len(viewlet.getAllMessages()), 0)
        api.content.transition(message, "activate")
        message.reindexObject()
        self._clean_cache()
        self.assertEqual(len(viewlet.getAllMessages()), 1)

        view = getMultiAdapter((self.folder, self.request), name="minisite_settings")
        self.assertTrue(view.available())
        self.assertFalse(view.enabled())
        view.enable()
        self.assertTrue(view.enabled())
        self.assertEqual(len(viewlet.getAllMessages()), 0)
