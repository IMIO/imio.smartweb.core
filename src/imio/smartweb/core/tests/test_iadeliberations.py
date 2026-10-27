# -*- coding: utf-8 -*-
from imio.smartweb.core.contents import IPublication
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.tests.utils import get_json
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.indexing import processQueue
from unittest.mock import patch
from zope.component import createObject
from zope.component import queryUtility
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import requests_mock

INSTITUTION = "https://conseil.staging.imio.be/liege"
UID_CATS = "8ea91c2b830b486fb4f78b6a91cee882"
UID_EXAMPLE = "5c642de5dddb4bcbae56163d4cc89079"


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

    def test_attached_file_link_text(self):
        # WEB-4340 : accessible text/title for the downloadable PDF link
        # (title + file type + human readable size + "opens in new tab")
        view = SectionView(self.files_section, self.request)
        item = {
            "title": self.json_publication_raw_mock.get("title"),
            "publication_attached_file": self.json_publication_raw_mock.get("file"),
        }
        self.assertEqual(
            view.attached_file_link_text(item),
            "Ordonnance concernant des mesures spécifiques en cas de grand froid. "
            "(PDF – 117.2 KB – New tab)",
        )
        self.assertEqual(view.attached_file_link_text({"title": "No file"}), "")

    def _set_iadeliberations_institution(self, m):
        """Select the institution in the control panel. The registry validates
        the value with the institutions that iA.Delib gives."""
        m.get(
            "https://www.deliberations.be/@search",
            json=get_json("resources/json_iadeliberations_institutions.json"),
        )
        api.portal.set_registry_record(
            "smartweb.iadeliberations_institution", INSTITUTION
        )

    @requests_mock.Mocker()
    def test_store_timestamped_publications_titles(self, m):
        self._set_iadeliberations_institution(m)
        m.get(
            f"{INSTITUTION}/@search",
            json=get_json("resources/json_iadeliberations_publications.json"),
        )
        api.content.create(
            container=self.page,
            type="imio.smartweb.SectionTimestampedPublications",
            title="Publications",
            hide_title=True,
            related_timestamped_publications=[UID_CATS],
        )
        brains = api.content.find(
            SearchableText="chats", portal_type="imio.smartweb.Page"
        )
        self.assertEqual([b.UID for b in brains], [self.page.UID()])
        self.assertEqual(len(api.content.find(SearchableText="Exemple")), 0)

    @requests_mock.Mocker()
    def test_modified_section_timestamped_publications(self, m):
        self._set_iadeliberations_institution(m)
        m.get(
            f"{INSTITUTION}/@search",
            json=get_json("resources/json_iadeliberations_publications.json"),
        )
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionTimestampedPublications",
            title="Publications",
            related_timestamped_publications=[UID_CATS],
        )
        # the user creates and modifies the section in two different requests
        processQueue()
        section.related_timestamped_publications = [UID_EXAMPLE]
        notify(ObjectModifiedEvent(section))
        self.assertEqual(len(api.content.find(SearchableText="chats")), 0)
        brains = api.content.find(
            SearchableText="Exemple", portal_type="imio.smartweb.Page"
        )
        self.assertEqual([b.UID for b in brains], [self.page.UID()])

        # iA.Delib does not reply : we keep the titles that we stored before
        m.get(f"{INSTITUTION}/@search", status_code=500)
        section.related_timestamped_publications = [UID_CATS]
        notify(ObjectModifiedEvent(section))
        self.assertEqual(len(api.content.find(SearchableText="chats")), 0)
        self.assertEqual(
            len(
                api.content.find(
                    SearchableText="Exemple", portal_type="imio.smartweb.Page"
                )
            ),
            1,
        )

        # no publication is selected
        section.related_timestamped_publications = []
        notify(ObjectModifiedEvent(section))
        self.assertEqual(len(api.content.find(SearchableText="Exemple")), 0)

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
