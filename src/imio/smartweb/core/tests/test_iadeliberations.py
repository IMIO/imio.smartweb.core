# -*- coding: utf-8 -*-
from imio.smartweb.core.contents import IPublication
from imio.smartweb.core.tests.utils import get_json
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from unittest.mock import patch
from zope.component import createObject
from zope.component import queryMultiAdapter
from zope.component import queryUtility


class TestIADeliberations(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="A Page",
        )
        self.files_section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionFiles",
            title="My files section",
        )
        self.json_publication_raw_mock = get_json(
            "resources/json_iadeliberations_publication.json"
        )

    def test_ct_publication_schema(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Publication")
        schema = fti.lookupSchema()
        self.assertEqual(IPublication, schema)

    def test_ct_publication_fti(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Publication")
        self.assertTrue(fti)

    def test_ct_publication_factory(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.Publication")
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(
            IPublication.providedBy(obj),
            "IPublication not provided by {0}!".format(
                obj,
            ),
        )

    @patch("imio.smartweb.core.subscribers.get_basic_auth_json")
    @patch("imio.smartweb.core.subscribers.get_value_from_registry")
    def test_ct_publication_adding(self, m_get_institution, m_get_publication):
        m_get_institution.return_value = "https://conseil.staging.imio.be/liege"
        m_get_publication.return_value = self.json_publication_raw_mock
        obj = api.content.create(
            container=self.files_section,
            type="imio.smartweb.Publication",
            linked_publication="ordonnance-concernant-des-mesures-specifiques-en-cas-de-grand-froid",
            id="ordonnance-concernant-des-mesures-specifiques-en-cas-de-grand-froid",
        )
        self.assertTrue(
            IPublication.providedBy(obj),
            "IPublication not provided by {0}!".format(
                obj.id,
            ),
        )
        parent = obj.__parent__
        self.assertIn(
            "ordonnance-concernant-des-mesures-specifiques-en-cas-de-grand-froid",
            parent.objectIds(),
        )
        title_resp = (
            "Ordonnance concernant des mesures spécifiques en cas de grand froid."
        )
        self.assertEqual(obj.title, title_resp)
        desc_resp = "Adopté par M. le Bourgmestre en date 12 décembre 2022"
        self.assertEqual(obj.description, desc_resp)
        url_resp = "https://conseil.staging.imio.be/liege/publications/ordonnance-concernant-des-mesures-specifiques-en-cas-de-grand-froid"
        self.assertEqual(obj.publication_url, url_resp)
        self.assertEqual(obj.publication_category, "Sécurité & Prévention")
        self.assertEqual(
            obj.publication_attached_file.get("filename"), "013400000123949.PDF"
        )

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn("publication", parent.objectIds())

    # Fix tests : timestamped publication are now a section, not an item in a file section
    #
    # @patch("imio.smartweb.core.subscribers.get_iadeliberation_json")
    # @patch("imio.smartweb.core.subscribers.get_value_from_registry")
    # def test_publication_view(self, m_get_institution, m_get_publication):
    #     m_get_institution.return_value = "https://conseil.staging.imio.be/liege"
    #     m_get_publication.return_value = self.json_publication_raw_mock
    #     obj = api.content.create(
    #         container=self.files_section,
    #         type="imio.smartweb.Publication",
    #         id="18820593",
    #     )
    #     obj.reindexObject()
    #     title_to_get = (
    #         "Ordonnance concernant des mesures spécifiques en cas de grand froid."
    #     )

    #     view = queryMultiAdapter((self.files_section, self.request), name="full_view")
    #     self.assertIn(title_to_get, view())
    #     self.assertNotIn("013400000123949.PDF", view())

    #     view = queryMultiAdapter((self.files_section, self.request), name="table_view")
    #     self.assertIn(title_to_get, [item[0]["title"] for item in view.items()])
    #     self.assertEqual(
    #         [
    #             item[0]["publication_attached_file"].get("filename")
    #             for item in view.items()
    #         ][0],
    #         "013400000123949.PDF",
    #     )
    #     self.assertEqual(
    #         [item[0]["publication_document_type"] for item in view.items()][0],
    #         "Ordonnance de police administrative",
    #     )
    #     self.assertEqual(
    #         [item[0]["publication_datetime"] for item in view.items()][0],
    #         "2024-08-14T09:14:31",
    #     )
