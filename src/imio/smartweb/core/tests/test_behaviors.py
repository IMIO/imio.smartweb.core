# -*- coding: utf-8
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING  # noqa
from imio.smartweb.core.tests.utils import get_leadimage_filename
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.namedfile.file import NamedBlobFile
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

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

    def test_leadimage_in_folder_block_view(self):
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="My folder",
        )
        page = api.content.create(
            container=folder,
            type="imio.smartweb.Page",
            title="My page",
        )
        page.image = NamedBlobFile("ploneLeadImage", filename=get_leadimage_filename())
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        view = getMultiAdapter((folder, self.request), name="block_view")
        self.assertIn("newsImage", view())
