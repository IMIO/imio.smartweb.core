# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_sections_types
from plone import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.textfield.value import RichTextValue
from plone.uuid.interfaces import IUUID
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds


class TestIndexes(ImioSmartwebTestCase):
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

    def test_SearchableText_section(self):
        catalog = api.portal.get_tool("portal_catalog")
        section_types = get_sections_types()
        for section_type in section_types:
            if section_type == "imio.smartweb.SectionText":
                # see test_SearchableText_sectiontext
                continue
            elif section_type == "imio.smartweb.SectionPostit":
                # see test_SearchableText_sectionpostit
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

    def test_SearchableText_section_with_description(self):
        catalog = api.portal.get_tool("portal_catalog")
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionLinks",
            title="Links",
        )
        section.description = "Description **bold**"
        section.reindexObject()
        uuid = IUUID(section)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(
            indexes.get("SearchableText"),
            ["links", "description", "bold"],
        )

        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionVideo",
            title="Video",
        )
        section.description = "Description **bold**"
        section.video_url = "https://www.youtube.com/embed/_dOAthafoGQ?feature=oembed"
        section.reindexObject()
        uuid = IUUID(section)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(
            indexes.get("SearchableText"),
            ["video", "description", "bold"],
        )

        self.page.reindexObject()
        uuid = IUUID(self.page)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertCountEqual(
            indexes.get("SearchableText"),
            [
                "my",
                "page",
                "my",
                "page",
                "links",
                "description",
                "bold",
                "video",
                "description",
                "bold",
            ],
        )

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
        self.page.reindexObject()
        self.assertEqual(len(api.content.find(SearchableText="Textsectionbody")), 2)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(indexes.get("SearchableText"), ["textsectionbody"])

    def test_SearchableText_sectionpostit(self):
        catalog = api.portal.get_tool("portal_catalog")
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionPostit",
            title="Postitsectiontitle",
        )
        uuid = IUUID(section)
        postit1 = {
            "title": "title1",
            "subtitle": "subtitle1",
            "description": "description1 with **bold**",
        }
        postit2 = {
            "title": "title2",
            "subtitle": "subtitle2",
            "description": "description2",
        }
        section.postits = [postit1, postit2]
        section.reindexObject()
        self.assertEqual(len(api.content.find(SearchableText="Postitsectiontitle")), 2)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertEqual(
            indexes.get("SearchableText"),
            [
                "title1",
                "subtitle1",
                "description1",
                "with",
                "bold",
                "title2",
                "subtitle2",
                "description2",
                "postitsectiontitle",
            ],
        )

    def test_SearchableText_pages(self):
        catalog = api.portal.get_tool("portal_catalog")
        section_types = get_sections_types()
        texts = []
        texts_page = ["my", "page", "my", "page"]  # id & title of page are indexed
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
        texts += texts_page
        uuid = IUUID(self.page)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertCountEqual(indexes.get("SearchableText"), texts)
        for obj in self.page.listFolderContents():
            api.content.delete(obj)
        brain = api.content.find(UID=uuid)[0]
        indexes = catalog.getIndexDataForRID(brain.getRID())
        self.assertCountEqual(indexes.get("SearchableText"), texts_page)

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

    def test_category_topics_2_topics(self):
        api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="vocabulary test page",
            page_category="emploi",
            topics=["culture", "health"],
        )

        portal_catalog = api.portal.get_tool("portal_catalog")
        result = portal_catalog._catalog.indexes["category_and_topics"]
        indexes = [x for x in result.uniqueValues()]
        self.assertEqual(sorted(indexes), ["emploi-culture", "emploi-health"])

        brains1 = api.content.find(
            category_and_topics="emploi-culture", context=self.portal
        )
        self.assertEqual(brains1[0].Title, "vocabulary test page")

        brains2 = api.content.find(
            category_and_topics="emploi-health", context=self.portal
        )
        self.assertEqual(brains2[0].Title, "vocabulary test page")

    def test_category_topics_1_topics(self):
        api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="vocabulary test page",
            page_category="emploi",
            topics=["mobility"],
        )

        portal_catalog = api.portal.get_tool("portal_catalog")
        result = portal_catalog._catalog.indexes["category_and_topics"]
        indexes = [x for x in result.uniqueValues()]

        self.assertEqual(sorted(indexes), ["emploi-mobility"])

        brains1 = api.content.find(
            category_and_topics="emploi-mobility", context=self.portal
        )
        self.assertEqual(brains1[0].Title, "vocabulary test page")

    def test_category_topics_no_topics(self):
        api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="vocabulary test page",
            page_category="emploi",
        )

        portal_catalog = api.portal.get_tool("portal_catalog")
        result = portal_catalog._catalog.indexes["category_and_topics"]
        indexes = [x for x in result.uniqueValues()]

        self.assertEqual(sorted(indexes), ["emploi"])

        brains1 = api.content.find(category_and_topics="emploi", context=self.portal)
        self.assertEqual(brains1[0].Title, "vocabulary test page")
