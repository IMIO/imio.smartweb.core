# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from time import sleep
from zope.component import getMultiAdapter
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
        first_modification = section.get_last_mofication_date
        sleep(1)
        # adding an image to a section causes a reindex of the section, thus
        # changes its last modification date
        api.content.create(
            container=section,
            type="Image",
            title="Kamoulox",
        )
        next_modification = section.get_last_mofication_date
        self.assertNotEqual(first_modification, next_modification)
