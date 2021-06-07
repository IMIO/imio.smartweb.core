# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_sections_types
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.vocabularies.types import BAD_TYPES
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter


class DescriptionIntegrationTest(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_description(self):
        portal_types = api.portal.get_tool("portal_types")
        bad_types = BAD_TYPES + get_sections_types() + ["Discussion Item"]
        all_types = [t for t in portal_types.listContentTypes() if t not in bad_types]
        for pt in all_types:
            if pt == "imio.smartweb.Footer":
                view = getMultiAdapter(
                    (self.portal, self.request), name="footer_settings"
                )
                view.add_footer()
                content_type = getattr(self.portal, "footer")
            else:
                content_type = api.content.create(
                    title="My {}".format(pt), container=self.portal, type=pt
                )
            content_type.description = "My bold **description** is wonderfull with *italic* and \r\n carriage return \r\n"
            view = queryMultiAdapter((content_type, self.request), name="description")
            self.assertEqual(
                view.description(),
                "My bold <strong>description</strong> is wonderfull with <em>italic</em> and <br/> carriage return <br/>",
            )

            content_type.description = "My bold **description** is *wonderfull with *italic* and \r\n carriage return \r\n"
            view = queryMultiAdapter((content_type, self.request), name="description")
            self.assertEqual(
                view.description(),
                "My bold <strong>description</strong> is <em>wonderfull with </em>italic* and <br/> carriage return <br/>",
            )
