# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.rest.directory.endpoint import DirectoryEndpoint
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.publisher.browser import TestRequest

import json
import requests_mock


class SectionsFunctionalTest(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.json_rest_directory = get_json("resources/json_rest_directory.json")

    def test_get_extra_params(self):
        request = TestRequest(
            form={"taxonomy_contact_category": '("token")', "topics": "education"}
        )
        endpoint = DirectoryEndpoint(self.portal, request)
        params = endpoint.get_extra_params([])
        self.assertEqual(
            params, ['taxonomy_contact_category=("token")', "topics=education"]
        )

        request = TestRequest(
            form={"topics": "education", "metadata_fields": ["topics", "category"]}
        )
        endpoint = DirectoryEndpoint(self.portal, request)
        params = endpoint.get_extra_params([])
        self.assertEqual(
            params,
            ["topics=education", "metadata_fields=topics", "metadata_fields=category"],
        )

    @requests_mock.Mocker()
    def test_call(self, m):
        rest_directory = api.content.create(
            container=self.portal,
            type="imio.smartweb.DirectoryView",
            title="My directory view",
        )
        request = TestRequest(
            form={"taxonomy_contact_category": '("token")', "topics": "education"}
        )
        endpoint = DirectoryEndpoint(rest_directory, request)
        url = endpoint.query_url
        self.assertEqual(
            url,
            "http://localhost:8080/Plone/@search?"
            "selected_entities=396907b3b1b04a97896b12cc792c77f8&"
            "portal_type=imio.directory.Contact&"
            "metadata_fields=facilities&"
            "metadata_fields=taxonomy_contact_category&"
            "metadata_fields=topics&"
            "metadata_fields=has_leadimage&"
            "sort_on=sortable_title&"
            'taxonomy_contact_category=("token")&'
            "topics=education",
        )
        m.get(url, text=json.dumps([]))
        call = endpoint()
        self.assertEqual(call, [])
