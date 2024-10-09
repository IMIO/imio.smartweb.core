# -*- coding: utf-8 -*-
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

    def test_get_campaigns(self):
        campaign_view = api.content.create(
            container=self.folder,
            type="imio.smartweb.CampaignView",
            linked_campaign="2",
        )
