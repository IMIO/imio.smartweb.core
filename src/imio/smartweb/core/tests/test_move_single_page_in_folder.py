# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.protect.authenticator import createToken
from zExceptions import Forbidden
from zope.interface import alsoProvides


class TestMoveSinglePageView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )
        api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            id="page",
        )
        self.folder.setLayout("element_view")

    def call_view(self, method="GET", token=None):
        self.request.method = method
        if token is not None:
            self.request.form["_authenticator"] = token
        view = self.portal.restrictedTraverse("@@move_single_page")
        return view()

    def test_get_shows_confirmation_and_changes_nothing(self):
        html = self.call_view()
        self.assertIn("Lancer la remontée", html)
        self.assertIn('name="_authenticator"', html)
        self.assertIn("folder", self.portal)
        self.assertNotIn("page", self.portal)

    def test_post_without_token_is_refused(self):
        with self.assertRaises(Forbidden):
            self.call_view(method="POST")
        with self.assertRaises(Forbidden):
            self.call_view(method="POST", token="wrong")
        self.assertIn("folder", self.portal)
        self.assertNotIn("page", self.portal)

    def test_post_with_token_moves_the_page(self):
        html = self.call_view(method="POST", token=createToken())
        self.assertIn("Résultats", html)
        self.assertNotIn("folder", self.portal)
        self.assertIn("page", self.portal)
