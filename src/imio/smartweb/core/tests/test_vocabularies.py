# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import json
import requests
import requests_mock

GUICHET_URL = "https://demo.guichet-citoyen.be/api/formdefs/"


def get_vocabulary(voc_name):
    factory = getUtility(IVocabularyFactory, voc_name)
    vocabulary = factory(api.portal.get())
    return vocabulary


class TestVocabularies(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.json_procedures_raw_mock = get_json(
            "resources/json_procedures_raw_mock.json"
        )
        self.json_contacts_raw_mock = get_json("resources/json_contacts_raw_mock.json")
        self.json_empty_contacts_raw_mock = get_json(
            "resources/json_no_contact_raw_mock.json"
        )
        self.contact_search_url = "http://localhost:8080/Plone/@search?portal_type=imio.directory.Contact&metadata_fields=UID"

    @requests_mock.Mocker()
    def test_procedure_keys(self, m):
        m.get(GUICHET_URL, text=json.dumps(self.json_procedures_raw_mock))
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 3)
        vocabulary = get_vocabulary("imio.smartweb.vocabulary.PublikProcedures")
        self.assertEqual(
            vocabulary.getTerm(
                "https://demo-formulaires.guichet-citoyen.be/acte-de-deces/"
            ).title,
            "Acte de d\\u00e9c\\u00e8s",
        )
        self.assertEqual(
            vocabulary.getTerm(
                "https://demo-formulaires.guichet-citoyen.be/acte-de-divorce/"
            ).title,
            "Acte de divorce",
        )
        self.assertEqual(
            vocabulary.getTerm(
                "https://demo-formulaires.guichet-citoyen.be/acte-de-mariage/"
            ).title,
            "Acte de mariage",
        )
        api.portal.set_registry_record(
            "smartweb.url_formdefs_api",
            "https://demo.guichet-citoyen.be/api/formdefs/?query=kamoulox",
        )
        m.get(
            "https://demo.guichet-citoyen.be/api/formdefs/?query=kamoulox",
            text=json.dumps(self.json_procedures_raw_mock),
        )
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 3)

    @requests_mock.Mocker()
    def test_procedure_error_values(self, m):
        m.get(GUICHET_URL, exc=requests.exceptions.ConnectTimeout)
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 0)

        m.get(GUICHET_URL, status_code=404)
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 0)

        api.portal.set_registry_record("smartweb.url_formdefs_api", "")
        m.get(GUICHET_URL, text=json.dumps(self.json_procedures_raw_mock))
        self.assertVocabularyLen("imio.smartweb.vocabulary.PublikProcedures", 0)

    def test_bootstrap_css(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.BootstrapCSS", 4)

    def test_subsite_display_mode(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.SubsiteDisplayMode", 3)

    def test_contact_blocks(self):
        self.assertVocabularyLen("imio.smartweb.vocabulary.ContactBlocks", 5)

    @requests_mock.Mocker()
    def test_remote_contacts(self, m):
        m.get(
            self.contact_search_url,
            text=json.dumps(self.json_contacts_raw_mock),
        )
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteContacts", 2)
        vocabulary = get_vocabulary("imio.smartweb.vocabulary.RemoteContacts")
        self.assertEqual(
            vocabulary.getTerm("af7bd1f547034b24a2e0da16c0ba0358").title,
            "Contact1 title",
        )
        self.assertEqual(
            vocabulary.getTerm("2dc381f0fb584381b8e4a19c84f53b35").title,
            "Contact2 title",
        )

    @requests_mock.Mocker()
    def test_remote_contacts_error_values(self, m):
        m.get(self.contact_search_url, exc=requests.exceptions.ConnectTimeout)
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteContacts", 0)
        m.get(self.contact_search_url, status_code=404)
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteContacts", 0)

    @requests_mock.Mocker()
    def test_empty_remote_contacts(self, m):
        m.get(
            self.contact_search_url, text=json.dumps(self.json_empty_contacts_raw_mock)
        )
        self.assertVocabularyLen("imio.smartweb.vocabulary.RemoteContacts", 0)
