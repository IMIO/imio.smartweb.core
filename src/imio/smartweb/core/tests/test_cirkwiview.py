# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import ICirkwiView
from imio.smartweb.core.tests.utils import get_html
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryMultiAdapter
from zope.component import queryUtility


import requests_mock

CIRKWI_API_GOOD_WIDGET_URL = "https://www.modulesbox.com/fr/api/module/12345"
CIRKWI_API_BAD_WIDGET_URL = "https://www.modulesbox.com/fr/api/module/123"


class TestCirkwiView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def _changeUser(self, loginName):
        logout()
        login(self.portal, loginName)
        self.member = api.user.get_current()
        self.request["AUTHENTICATED_USER"] = self.member

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            "imio.smartweb.Folder",
            self.portal,
            "parent_container",
            title="Parent container",
        )
        self.parent = self.portal[parent_id]
        self._changeUser("test")
        self.cirkwi_bad_widget_html = get_html("resources/cirkwi_bad_widget_mock.html")
        self.cirkwi_good_widget_html = get_html(
            "resources/cirkwi_good_widget_mock.html"
        )

    def test_ct_cirkwi_schema(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CirkwiView")
        schema = fti.lookupSchema()
        self.assertEqual(ICirkwiView, schema)

    def test_ct_cirkwi_fti(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CirkwiView")
        self.assertTrue(fti)

    def test_ct_cirkwi_factory(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CirkwiView")
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ICirkwiView.providedBy(obj),
            "ICirkwiView not provided by {0}!".format(
                obj,
            ),
        )

    def test_ct_cirkwi_adding(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        obj = api.content.create(
            container=self.parent,
            type="imio.smartweb.CirkwiView",
            id="cirkwiview",
        )

        self.assertTrue(
            ICirkwiView.providedBy(obj),
            "ICirkwiView not provided by {0}!".format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn("cirkwiview", parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("cirkwiview", parent.objectIds())

    def test_ct_cirkwi_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CirkwiView")
        self.assertTrue(fti.global_allow, "{0} is globally addable!".format(fti.id))

    @requests_mock.Mocker()
    def test_cirkwi_view(self, m):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )
        cirkwiview = api.content.create(
            container=folder,
            type="imio.smartweb.CirkwiView",
            id="cirkwiview",
        )
        m.get(CIRKWI_API_BAD_WIDGET_URL, status_code=404)
        cirkwiview.cirkwi_widget_id = "123"
        view = queryMultiAdapter((cirkwiview, self.request), name="view")
        self.assertIn('class="cirkwi_richtext"', view())
        self.assertIn('<div class="cirkwi_contents">404</div>', view())
        self.assertNotIn(
            "https://www.modulesbox.com/template/4/css/cirkwi/main.css", view()
        )

        m.get(CIRKWI_API_GOOD_WIDGET_URL, text=self.cirkwi_good_widget_html)
        cirkwiview.cirkwi_widget_id = "12345"
        view = queryMultiAdapter((cirkwiview, self.request), name="view")
        self.assertIn('class="cirkwi_richtext"', view())
        self.assertIn(
            "https://www.modulesbox.com/template/4/css/cirkwi/main.css", view()
        )
        self.assertNotIn("<p>My rich text</p>", view())

        cirkwiview.text = RichTextValue("<p>My rich text</p>", "text/html", "text/html")
        view = queryMultiAdapter((cirkwiview, self.request), name="view")
        self.assertIn("<p>My rich text</p>", view())
