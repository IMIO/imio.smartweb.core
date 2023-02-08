# -*- coding: utf-8 -*-

from imio.smartweb.core import config
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing.zope import WSGI_SERVER_FIXTURE
from zope.component import getUtility
from zope.globalrequest import setRequest
from zope.schema.interfaces import IVocabularyFactory

import imio.smartweb.core
import imio.smartweb.core.contents.pages.footer.content as footer_content
import imio.smartweb.core.contents.pages.herobanner.content as herobanner_content
import mock
import json
import requests_mock
import unittest


class ImioSmartwebCoreLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=imio.smartweb.core, name="testing.zcml")

    @requests_mock.Mocker()
    def setUpPloneSite(self, portal, m):
        request = portal.REQUEST
        setRequest(request)
        json_directory_entities_raw_mock = get_json(
            "resources/json_directory_entities_raw_mock.json"
        )
        m.get(
            f"{config.DIRECTORY_URL}/@search?portal_type=imio.directory.Entity&sort_on=sortable_title&b_size=1000000&metadata_fields=UID",
            text=json.dumps(json_directory_entities_raw_mock),
        )
        json_events_entities_raw_mock = get_json(
            "resources/json_events_entities_raw_mock.json"
        )
        m.get(
            f"{config.EVENTS_URL}/@search?portal_type=imio.events.Entity&sort_on=sortable_title&b_size=1000000&metadata_fields=UID",
            text=json.dumps(json_events_entities_raw_mock),
        )
        json_news_entities_raw_mock = get_json(
            "resources/json_news_entities_raw_mock.json"
        )
        m.get(
            f"{config.NEWS_URL}/@search?portal_type=imio.news.Entity&sort_on=sortable_title&b_size=1000000&metadata_fields=UID",
            text=json.dumps(json_news_entities_raw_mock),
        )
        applyProfile(portal, "imio.smartweb.core:testing")
        api.user.create(email="test@imio.be", username="test")
        api.user.grant_roles(username="test", roles=["Site Administrator"])
        footer_content.ban_physicalpath = mock.Mock(return_value=None)
        herobanner_content.ban_physicalpath = mock.Mock(return_value=None)


IMIO_SMARTWEB_CORE_FIXTURE = ImioSmartwebCoreLayer()


IMIO_SMARTWEB_CORE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IMIO_SMARTWEB_CORE_FIXTURE,),
    name="ImioSmartwebCoreLayer:IntegrationTesting",
)


IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IMIO_SMARTWEB_CORE_FIXTURE,),
    name="ImioSmartwebCoreLayer:FunctionalTesting",
)


IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IMIO_SMARTWEB_CORE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="ImioSmartwebCoreLayer:AcceptanceTesting",
)


class ImioSmartwebTestCase(unittest.TestCase):
    def assertVocabularyLen(self, vocname, voc_len):
        factory = getUtility(IVocabularyFactory, vocname)
        vocabulary = factory()
        self.assertEqual(len(vocabulary), voc_len)
