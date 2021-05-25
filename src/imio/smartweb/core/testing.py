# -*- coding: utf-8 -*-
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
from zope.schema.interfaces import IVocabularyFactory

import imio.smartweb.core
import unittest


class ImioSmartwebCoreLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=imio.smartweb.core)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "imio.smartweb.core:testing")
        api.user.create(email="test@imio.be", username="test")
        api.user.grant_roles(username="test", roles=["Site Administrator"])


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
