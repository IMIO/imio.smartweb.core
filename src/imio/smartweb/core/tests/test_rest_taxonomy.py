# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import clear_ram_cache
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import transaction


class TestSmartwebTaxonomyPatch(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.api_session = RelativeSession(self.portal.absolute_url())
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="My page",
            language="fr",
        )
        self.page.taxonomy_page_category = ["emploi"]
        self.page.reindexObject()
        transaction.commit()

    def tearDown(self):
        self.api_session.close()
        clear_ram_cache()

    def test_reply(self):
        """Patching the taxonomy gives the new label to the objects"""
        response = self.api_session.patch(
            "@taxonomy/collective.taxonomy.page_category",
            json={
                "taxonomy": "collective.taxonomy.page_category",
                "languages": ["fr"],
                "tree": [
                    {
                        "key": "emploi",
                        "title": "Recrutement",
                        "translations": {"fr": "Recrutement"},
                    }
                ],
            },
        )
        self.assertEqual(response.status_code, 204, response.text)
        transaction.begin()
        found = [b.getObject() for b in api.content.find(SearchableText="Recrutement")]
        self.assertEqual(found, [self.page])
