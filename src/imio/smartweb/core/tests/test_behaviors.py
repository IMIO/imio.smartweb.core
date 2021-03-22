# -*- coding: utf-8 -*-
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING  # noqa
from plone import api
from plone.app.testing import login
from plone.app.testing import logout

import unittest


class ProcedureFunctionalTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def _changeUser(self, loginName):
        logout()
        login(self.portal, loginName)
        self.member = api.user.get_current()
        self.request["AUTHENTICATED_USER"] = self.member

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self._changeUser("test")

    def test_quick_access(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Quick access page",
            include_in_quick_access=True,
        )
        brains = api.content.find(include_in_quick_access=True)
        self.assertEquals(len(brains), 1)
        self.assertEquals(page, brains[0].getObject())
        page.include_in_quick_access = False
        page.reindexObject()
        brains = api.content.find(include_in_quick_access=True)
        self.assertEquals(len(brains), 0)
