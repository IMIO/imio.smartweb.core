# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPage
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.protect.authenticator import createToken
from time import sleep
from zope.component import createObject
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides
import unittest


class SectionsIntegrationTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )

    def test_redirection(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
            id="section-text",
        )
        getMultiAdapter((section, self.request), name="view")()
        self.assertEqual(
            self.request.response.headers["location"],
            "http://nohost/plone/page#section-text",
        )

    def test_get_last_mofication_date(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        self.assertEqual(section.get_last_mofication_date, section.ModificationDate())
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionGallery",
            title="Section Gallery",
        )
        self.assertEqual(section.get_last_mofication_date, section.ModificationDate())
        sleep(1)
        img = api.content.create(
            container=section,
            type="Image",
            title="Kamoulox",
        )
        img.reindexObject()
        section.reindexObject()
        self.assertNotEqual(section.get_last_mofication_date, section.ModificationDate())
        self.assertEqual(section.get_last_mofication_date, img.ModificationDate())
