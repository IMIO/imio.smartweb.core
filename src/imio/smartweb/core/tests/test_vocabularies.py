# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.tests.utils import get_procedure_json
from plone import api
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import json
import requests
import requests_mock
import unittest


def get_procedures_vocabulary():
    name = "imio.smartweb.vocabulary.PublikProcedures"
    factory = getUtility(IVocabularyFactory, name)
    vocabulary = factory(api.portal.get())
    return vocabulary


class TestVocabularies(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.json_procedures_raw_mock = get_procedure_json()

    @requests_mock.Mocker()
    def test_procedure_keys(self, m):
        m.get(
            "https://demo.guichet-citoyen.be/api/formdefs/",
            text=json.dumps(self.json_procedures_raw_mock),
        )
        vocabulary = get_procedures_vocabulary()
        keys = vocabulary.by_value.keys()
        self.assertEqual(len(keys), 3)
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
        vocabulary = get_procedures_vocabulary()
        keys = vocabulary.by_value.keys()
        self.assertEqual(len(keys), 3)

    @requests_mock.Mocker()
    def test_procedure_error_values(self, m):
        m.get(
            "https://demo.guichet-citoyen.be/api/formdefs/",
            exc=requests.exceptions.ConnectTimeout,
        )
        vocabulary = get_procedures_vocabulary()
        keys = vocabulary.by_value.keys()
        self.assertEqual(len(keys), 0)

        m.get(
            "https://demo.guichet-citoyen.be/api/formdefs/",
            text=json.dumps(self.json_procedures_raw_mock),
            status_code=404,
        )
        vocabulary = get_procedures_vocabulary()
        keys = vocabulary.by_value.keys()
        self.assertEqual(len(keys), 0)

        api.portal.set_registry_record("smartweb.url_formdefs_api", "")
        m.get(
            "https://demo.guichet-citoyen.be/api/formdefs/",
            text=json.dumps(self.json_procedures_raw_mock),
        )
        vocabulary = get_procedures_vocabulary()
        keys = vocabulary.by_value.keys()
        self.assertEqual(len(keys), 0)

    def test_bootstrap_css(self):
        factory = getUtility(
            IVocabularyFactory, "imio.smartweb.vocabulary.BootstrapCSS"
        )
        vocabulary = factory()
        self.assertEqual(len(vocabulary), 3)

    def test_subsite_display_mode(self):
        factory = getUtility(
            IVocabularyFactory, "imio.smartweb.vocabulary.SubsiteDisplayMode"
        )
        vocabulary = factory()
        self.assertEqual(len(vocabulary), 3)
