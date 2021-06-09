# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_leadimage_filename
from imio.smartweb.core.tests.utils import get_sections_types
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.textfield.value import RichTextValue
from plone.uuid.interfaces import IUUID
from plone.namedfile.file import NamedBlobFile
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds


class FolderIntegrationTest(ImioSmartwebTestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="My page",
        )

    def test_has_leadimage(self):
        uuid = IUUID(self.page)
        self.assertEqual(len(api.content.find(has_leadimage=True)), 0)
        brain = api.content.find(UID=uuid)[0]
        self.assertEqual(brain.has_leadimage, False)
        self.page.image = NamedBlobFile(
            "ploneLeadImage", filename=get_leadimage_filename()
        )
        self.page.reindexObject()
        self.assertEqual(len(api.content.find(has_leadimage=True)), 1)
        brain = api.content.find(UID=uuid)[0]
        self.assertEqual(brain.has_leadimage, True)

    def test_SearchableText_section(self):
        catalog = api.portal.get_tool("portal_catalog")
        section_types = get_sections_types()
        for section_type in section_types:
            if section_type == "imio.smartweb.SectionText":
                # see test_SearchableText_sectiontext
                continue
            title = "Title{}".format(section_type.split(".")[-1])
            section = api.content.create(
                container=self.page,
                type=section_type,
                title=title,
            )
            uuid = IUUID(section)
            brain = api.content.find(UID=uuid)[0]
            indexes = catalog.getIndexDataForRID(brain.getRID())
            self.assertEqual(indexes.get("SearchableText"), [title.lower()])
            section.hide_title = True
            section.reindexObject()
            brain = api.content.find(UID=uuid)[0]
            indexes = catalog.getIndexDataForRID(brain.getRID())
            self.assertEqual(indexes.get("SearchableText"), [])

    def test_SearchableText_sectiontext(self):
        catalog = api.portal.get_tool("portal_catalog")
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Textsectiontitle",
        )
        uuid = IUUID(section)
        self.assertEqual(len(api.content.find(SearchableText="Textsectiontitle")), 0)
        section.text = RichTextValue("<p>Textsectionbody</p>", "text/html", "text/html")
        section.reindexObject()
        self.assertEqual(len(api.content.find(SearchableText="Textsectionbody")), 1)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(indexes.get("SearchableText"), ["textsectionbody"])

    def test_SearchableText_pages(self):
        catalog = api.portal.get_tool("portal_catalog")
        section_types = get_sections_types()
        texts = []
        for section_type in section_types:
            title = "Title{}".format(section_type.split(".")[-1])
            section = api.content.create(
                container=self.page,
                type=section_type,
                title=title,
            )
            if section_type == "imio.smartweb.SectionText":
                section.text = RichTextValue(
                    "<p>Textsectionbody</p>", "text/html", "text/html"
                )
                section.reindexObject()
                # section text body is indexed
                texts.append("textsectionbody")
            else:
                # sections titles are indexed by default
                texts.append(title.lower())
        texts += ["my", "page", "my", "page"]  # id & title of page are indexed
        uuid = IUUID(self.page)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertCountEqual(indexes.get("SearchableText"), texts)

    def test_related_quickaccess(self):
        catalog = api.portal.get_tool("portal_catalog")
        intids = getUtility(IIntIds)
        folder = api.content.create(
            container=self.portal,
            type="imio.smartweb.Folder",
            title="Folder",
        )
        uuid_folder = IUUID(folder)
        page2 = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page 2",
        )
        folder.quick_access_items = [
            RelationValue(intids.getId(self.page)),
            RelationValue(intids.getId(page2)),
        ]
        folder.reindexObject()
        uuid_qa1 = IUUID(self.page)
        uuid_qa2 = IUUID(page2)
        brain = api.content.find(UID=uuid_folder)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertCountEqual(indexes.get("related_quickaccess"), [uuid_qa1, uuid_qa2])
        self.assertCountEqual(brain.related_quickaccess, [uuid_qa1, uuid_qa2])
