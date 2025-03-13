# -*- coding: utf-8 -*-
from imio.smartweb.core.contents.rest.base import BaseEndpoint
from imio.smartweb.core.contents.rest.campaign.endpoint import CampaignEndpoint
from imio.smartweb.core.contents import ICampaignView
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
from zope.publisher.browser import TestRequest

import json
import requests_mock


class TestIdeabox(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="A Folder",
        )
        self.json_campaigns_raw_mock = get_json("resources/json_ideabox_campaigns.json")
        self.json_campaign_raw_mock = get_json("resources/json_ideabox_campaign.json")

    def test_ct_publication_schema(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CampaignView")
        schema = fti.lookupSchema()
        self.assertEqual(ICampaignView, schema)

    def test_ct_publication_fti(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CampaignView")
        self.assertTrue(fti)

    def test_ct_publication_factory(self):
        fti = queryUtility(IDexterityFTI, name="imio.smartweb.CampaignView")
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(
            ICampaignView.providedBy(obj),
            "ICampaignView not provided by {0}!".format(
                obj,
            ),
        )

    @patch("imio.smartweb.core.subscribers.get_basic_auth_json")
    @patch("imio.smartweb.core.subscribers.get_value_from_registry")
    @patch("imio.smartweb.core.contents.rest.campaign.content.get_basic_auth_json")
    @patch("imio.smartweb.core.contents.rest.campaign.content.get_value_from_registry")
    def test_get_campaign(
        self,
        m_get_value_from_registry_namechooser,
        m_get_basic_auth_json_namechooser,
        m_get_value_from_registry,
        m_get_basic_auth_json,
    ):
        m_get_value_from_registry.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json.return_value = self.json_campaign_raw_mock

        m_get_value_from_registry_namechooser.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json_namechooser.return_value = self.json_campaign_raw_mock
        campaign_view = api.content.create(
            title="kamoulox",
            container=self.folder,
            type="imio.smartweb.CampaignView",
            linked_campaign="2",
        )
        self.assertEqual(campaign_view.title, "Sprint iMio Fall 2024")
        self.assertEqual(campaign_view.id, "sprint-imio-fall-2024")

    # CampaignNameChooser : Give th Title to our object thanks to e-guichet object Title.
    @patch("imio.smartweb.core.subscribers.get_basic_auth_json")
    @patch("imio.smartweb.core.subscribers.get_value_from_registry")
    @patch("imio.smartweb.core.contents.rest.campaign.content.get_basic_auth_json")
    @patch("imio.smartweb.core.contents.rest.campaign.content.get_value_from_registry")
    def test_campaign_name_chooser(
        self,
        m_get_value_from_registry_namechooser,
        m_get_basic_auth_json_namechooser,
        m_get_value_from_registry,
        m_get_basic_auth_json,
    ):
        from imio.smartweb.core.contents.rest.campaign.content import CampaignView
        from zope.component import queryAdapter
        from zope.container.interfaces import INameChooser

        m_get_value_from_registry.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json.return_value = self.json_campaign_raw_mock

        m_get_value_from_registry_namechooser.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json_namechooser.return_value = self.json_campaign_raw_mock
        campaign_view = CampaignView(id="test-campaign", title=None)
        campaign_view.linked_campaign = "2"
        name_chooser = queryAdapter(self.folder, INameChooser)
        generated_id = name_chooser.chooseName(None, campaign_view)
        self.assertEqual(campaign_view.title, "Sprint iMio Fall 2024")
        self.assertEqual(generated_id, "sprint-imio-fall-2024")

    @requests_mock.Mocker()
    @patch("imio.smartweb.core.subscribers.get_basic_auth_json")
    @patch("imio.smartweb.core.subscribers.get_value_from_registry")
    def test_get_projects(self, m_get_value_from_registry, m_get_basic_auth_json, m):
        m_get_value_from_registry.return_value = (
            "https://staging3-formulaires.guichet-citoyen.be/api"
        )
        m_get_basic_auth_json.return_value = self.json_campaign_raw_mock
        campaign_view = api.content.create(
            id="kamoulox",
            container=self.folder,
            type="imio.smartweb.CampaignView",
            linked_campaign="2",
        )
        # react additionnal fields request.
        # form={
        #         "taxonomy_contact_category_for_filtering": ("token"),
        #         "topics": "education",
        #     }

        request = TestRequest()
        endpoint = CampaignEndpoint(campaign_view, request)
        url = endpoint.query_url
        self.assertEqual(
            url,
            "https://demo-formulaires.guichet-citoyen.be/api/cards/imio-ideabox-projet/list?filter-campagne=2&full=on&filter-statut=Vote|Enregistr%C3%A9e&filter-statut-operator=in&",
        )

        m.get(url, text=json.dumps({}))
        call = endpoint()
        self.assertEqual(call, {})

        # to be continued
