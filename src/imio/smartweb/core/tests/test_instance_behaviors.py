# -*- coding: utf-8 -*-

from collective.taxonomy.interfaces import ITaxonomy
from imio.smartweb.core.browser.instancebehaviors.form import InstanceBehaviors
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.testing.zope import Browser
from zope.component import getMultiAdapter
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.i18n.interfaces import ITranslationDomain
from zope.schema.interfaces import IVocabularyFactory

import transaction


class TestInstanceBehaviors(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.authorized_instance_behaviors = [
            "imio.smartweb.Page",
            "imio.smartweb.Procedure",
        ]
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            id="folder",
        )
        self.page = api.content.create(
            container=self.folder,
            type="imio.smartweb.Page",
            id="page",
        )
        taxonomy = queryUtility(ITaxonomy, name="collective.taxonomy.test")
        self.assertIsNotNone(taxonomy)

    def delete_taxonomy(self, name):
        sm = self.portal.getSiteManager()
        utility = sm.queryUtility(ITaxonomy, name=name)
        utility.unregisterBehavior()
        sm.unregisterUtility(utility, ITaxonomy, name=name)
        sm.unregisterUtility(utility, IVocabularyFactory, name=name)
        sm.unregisterUtility(utility, ITranslationDomain, name=name)

    def test_action_available(self):
        for t in self.authorized_instance_behaviors:
            obj = api.content.create(
                container=self.folder,
                type=t,
                title="My {}".format(t),
            )
            is_instancebehaviors_assignable_content = getMultiAdapter(
                (obj, self.request), name="is_instancebehaviors_assignable_content"
            )
            self.assertTrue(is_instancebehaviors_assignable_content())

        is_instancebehaviors_assignable_content = getMultiAdapter(
            (self.folder, self.request), name="is_instancebehaviors_assignable_content"
        )
        self.assertFalse(is_instancebehaviors_assignable_content())

        is_instancebehaviors_assignable_content = getMultiAdapter(
            (self.page, self.request), name="is_instancebehaviors_assignable_content"
        )
        self.delete_taxonomy("collective.taxonomy.test")
        self.assertFalse(is_instancebehaviors_assignable_content())

    def test_form(self):
        transaction.commit()
        browser = Browser(self.layer["app"])
        browser.addHeader(
            "Authorization",
            "Basic %s:%s"
            % (
                TEST_USER_NAME,
                TEST_USER_PASSWORD,
            ),
        )
        browser.open("{}/edit".format(self.page.absolute_url()))
        content = browser.contents
        self.assertNotIn("form-widgets-test-taxonomy_test", content)
        request = self.request
        request.form = {
            "form.widgets.instance_behaviors": "collective.taxonomy.generated.test",
            "form.buttons.ok": "Ok",
        }
        alsoProvides(request, IPloneFormLayer)
        form = InstanceBehaviors(self.page, request)
        form.update()
        transaction.commit()
        browser.open("{}/edit".format(self.page.absolute_url()))
        content = browser.contents
        self.assertIn("form-widgets-test-taxonomy_test", content)

    def test_vocabulary(self):
        vocabulary_name = "imio.smartweb.vocabulary.AvailableInstanceBehaviors"
        self.assertVocabularyLen(vocabulary_name, 1)
        self.delete_taxonomy("collective.taxonomy.test")
        self.assertVocabularyLen(vocabulary_name, 0)
