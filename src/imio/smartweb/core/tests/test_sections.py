# -*- coding: utf-8 -*-

from AccessControl.unauthorized import Unauthorized
from bs4 import BeautifulSoup
from collective.geolocationbehavior.geolocation import IGeolocatable
from functools import reduce
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import clear_cache
from imio.smartweb.core.tests.utils import make_named_image
from imio.smartweb.core.tests.utils import get_sections_types
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.formwidget.geolocation.geolocation import Geolocation
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from plone.protect.authenticator import createToken
from time import sleep
from z3c.relationfield import RelationValue
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import modified


class TestSections(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        # Number of sections where there is a title if section is empty.
        # sectionHTML,...
        self.NUMBER_OF_EMPTY_SECTIONS = len(get_sections_types("empty_section"))

        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )

    def test_redirection(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
            id="text",
        )
        getMultiAdapter((section, self.request), name="view")()
        self.assertEqual(
            self.request.response.headers["location"],
            "http://nohost/plone/page#section-text",
        )

    def test_modification_date(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionGallery",
            title="Section Gallery",
        )
        first_modification = section.ModificationDate()
        sleep(1)
        # adding an image to a section causes a reindex of the section, thus
        # changes its last modification date
        api.content.create(
            container=section,
            type="Image",
            title="Image",
        )
        next_modification = section.ModificationDate()
        self.assertNotEqual(first_modification, next_modification)

    def test_files_informations(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionFiles",
            title="Section files",
        )
        file_obj = api.content.create(
            container=section,
            type="File",
            title="My file",
        )
        file_obj.file = NamedBlobFile(data="file data", filename="file.txt")
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn("1 KB", view())

    def test_video_section(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionVideo",
            title="Section video",
        )
        section.video_url = "https://www.youtube.com/watch?v=_dOAthafoGQ"
        view = queryMultiAdapter((section, self.request), name="view")
        embedded_video = view.get_embed_video()
        self.assertIn("iframe", embedded_video)
        self.assertIn(
            "https://www.youtube.com/embed/_dOAthafoGQ?feature=oembed", embedded_video
        )

    def test_external_content_section(self):
        setRoles(self.portal, TEST_USER_ID, ["Contributor"])
        with self.assertRaises(Unauthorized):
            api.content.create(
                container=self.page,
                type="imio.smartweb.SectionExternalContent",
                title="Section External Content",
            )
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionExternalContent",
            title="Section External Content",
        )
        # section.external_content_url = (
        #     "https://app.eaglebe.com/fr-be/map/la%20louvi%C3%A8re"
        # )
        # view = queryMultiAdapter((section, self.request), name="view")
        # embedded_content = view.get_embed_external_content()
        # self.assertIn("iframe", embedded_content)
        # self.assertIn('class="eaglebe"', embedded_content)
        # self.assertIn('scrolling="no"', embedded_content)
        # self.assertIn(
        #     "https://app.eaglebe.com/fr-be/map/la%20louvi%C3%A8re", embedded_content
        # )

        section.external_content_url = "http://www.perdu.com"
        view = queryMultiAdapter((section, self.request), name="view")
        embedded_content = view.get_embed_external_content()
        self.assertNotIn("iframe", embedded_content)
        self.assertNotIn("class='eaglebe'", embedded_content)
        self.assertIn('<p class="unknow_service">Unknow service</p>', embedded_content)

    def test_map_section(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionMap",
            title="Section map",
        )
        IGeolocatable(section).geolocation = Geolocation(latitude="4.5", longitude="45")
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn("Section map", view())
        self.assertIn('class="pat-leaflet map"', view())

    def test_selections_section(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionSelections",
            title="Section selections",
        )
        page2 = api.content.create(
            container=self.portal, type="imio.smartweb.Page", title="Page 2"
        )
        intids = getUtility(IIntIds)
        section.selected_items = [
            RelationValue(intids.getId(page2)),
        ]
        view = queryMultiAdapter((section, self.request), name="table_view")
        self.assertIn("Page 2", [item[0]["title"] for item in view.items()])
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn("Page 2", view())

    def test_collection_section(self):
        portal_page = api.content.create(
            container=self.portal,
            type="imio.smartweb.PortalPage",
            title="Portal page",
        )
        section_gallery = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionGallery",
            title="Section gallery",
        )
        for i in range(0, 10):
            api.content.create(
                container=section_gallery,
                type="Image",
                title=f"Image{i}",
            )
        query = [
            {
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.any",
                "v": ["Image"],
            }
        ]
        collection = api.content.create(
            container=self.portal,
            type="Collection",
            title="My collection",
        )
        collection.setQuery(query)
        self.assertEqual(len(collection.results()), 10)
        section_collection = api.content.create(
            container=portal_page,
            type="imio.smartweb.SectionCollection",
            title="Section collection",
        )
        intids = getUtility(IIntIds)
        section_collection.collection = RelationValue(intids.getId(collection))
        section_collection.max_nb_batches = 2
        section_collection.nb_results_by_batch = 3
        view = queryMultiAdapter((section_collection, self.request), name="table_view")
        items = view.items()
        self.assertEqual(len(items), 2)
        self.assertEqual(len(items[0]), 3)
        self.assertEqual(reduce(lambda count, r: count + len(r), items, 0), 6)
        section_collection.nb_results_by_batch = 1
        section_collection.max_nb_batches = 4
        view = queryMultiAdapter((section_collection, self.request), name="table_view")
        self.assertEqual(len(view.items()), 4)

    def test_sections_ordering(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        api.content.create(
            container=page,
            type="imio.smartweb.SectionGallery",
            title="Section 1",
            id="section1",
        )
        api.content.create(
            container=page,
            type="imio.smartweb.SectionText",
            title="Section 2",
            id="section2",
        )
        self.assertListEqual(page.objectIds(), ["section1", "section2"])
        self.request.form["_authenticator"] = createToken()
        self.request.form["id"] = "section2"
        self.request.form["delta"] = "-1"
        self.request.form["orderedSectionsIds"] = '["section1", "section2"]'
        self.request.environ["REQUEST_METHOD"] = "POST"
        getMultiAdapter((page, self.request), name="reorder-section")()
        self.assertListEqual(page.objectIds(), ["section2", "section1"])

        self.request.form["id"] = "section1"
        self.request.form["delta"] = "-1"
        # wrong ordered sections ids
        self.request.form["orderedSectionsIds"] = '["section1", "section2"]'
        getMultiAdapter((page, self.request), name="reorder-section")()
        # nothing changes
        self.assertListEqual(page.objectIds(), ["section2", "section1"])

    def test_empty_sections(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        api.content.transition(page, "publish")
        section_types = get_sections_types()
        for section_type in section_types:
            api.content.create(
                container=page,
                type=section_type,
                title="Title of my {}".format(section_type),
            )
        video_section = getattr(page, "title-of-my-imio-smartweb-sectionvideo")
        video_section.video_url = "https://www.youtube.com/watch?v=_dOAthafoGQ"
        selections_section = getattr(
            page, "title-of-my-imio-smartweb-sectionselections"
        )
        intids = getUtility(IIntIds)
        selections_section.selected_items = [
            RelationValue(intids.getId(self.page)),
        ]
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(
            view.count('<h2 class="section-title">Title of my '), len(section_types)
        )
        logout()
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(view.count('<h2 class="section-title">Title of my '), 5)
        login(self.portal, "test")
        gallery_section = getattr(page, "title-of-my-imio-smartweb-sectiongallery")
        api.content.create(
            container=gallery_section,
            type="Image",
            title="Image",
        )
        files_section = getattr(page, "title-of-my-imio-smartweb-sectionfiles")
        file_obj = api.content.create(
            container=files_section,
            type="File",
            title="My file",
        )
        file_obj.file = NamedBlobFile(data="file data", filename="file.txt")
        links_section = getattr(page, "title-of-my-imio-smartweb-sectionlinks")
        api.content.create(
            container=links_section,
            type="imio.smartweb.BlockLink",
            title="My link",
        )
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(
            view.count('<h2 class="section-title">Title of my '), len(section_types)
        )

    def test_sections_titles(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        api.content.transition(page, "publish")
        section_types = get_sections_types()
        for section_type in section_types:
            api.content.create(
                container=page,
                type=section_type,
                title="Title of my {}".format(section_type),
            )
        video_section = getattr(page, "title-of-my-imio-smartweb-sectionvideo")
        video_section.video_url = "https://www.youtube.com/watch?v=_dOAthafoGQ"
        gallery_section = getattr(page, "title-of-my-imio-smartweb-sectiongallery")
        api.content.create(
            container=gallery_section,
            type="Image",
            title="Image",
        )
        files_section = getattr(page, "title-of-my-imio-smartweb-sectionfiles")
        file_obj = api.content.create(
            container=files_section,
            type="File",
            title="My file",
        )
        file_obj.file = NamedBlobFile(data="file data", filename="file.txt")
        links_section = getattr(page, "title-of-my-imio-smartweb-sectionlinks")
        api.content.create(
            container=links_section,
            type="imio.smartweb.BlockLink",
            title="My link",
        )
        selections_section = getattr(
            page, "title-of-my-imio-smartweb-sectionselections"
        )
        intids = getUtility(IIntIds)
        selections_section.selected_items = [
            RelationValue(intids.getId(self.page)),
        ]

        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(
            view.count('<h2 class="section-title">Title of my '), len(section_types)
        )
        # test hide_title
        for section_id in page.objectIds():
            section = getattr(page, section_id)
            section.hide_title = True
        # hide_title in login mode (add some specific css class)
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(
            view.count('<h2 class="hidden-section-title hide-in-preview">Title of my '),
            self.NUMBER_OF_EMPTY_SECTIONS,
        )
        # hide_title in logout mode (no more <h2> / title)
        logout()
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(view.count("</h2>"), 0)

    def test_sections_titles_display_switch(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        api.content.transition(page, "publish")
        # We can't edit title visibility of Contact & Text sections.
        # And visibility of these sections titles is False.
        for section_type in [
            "imio.smartweb.SectionContact",
            "imio.smartweb.SectionText",
        ]:
            section = api.content.create(
                container=page,
                type=section_type,
                title="Title of my {}".format(section_type),
            )
            section.hide_title = True
            view = queryMultiAdapter((section, self.request), name="hide_section_title")
            view.hide_section_title()
            self.assertTrue(section.hide_title)
            view = queryMultiAdapter((section, self.request), name="show_section_title")
            view.show_section_title()
            self.assertTrue(section.hide_title)
            view = queryMultiAdapter((page, self.request), name="full_view")
            self.assertNotIn("Show title", view())

        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionGallery",
            title="Title of my galery",
        )
        view = queryMultiAdapter((section, self.request), name="hide_section_title")
        view.hide_section_title()
        self.assertTrue(section.hide_title)
        view = queryMultiAdapter((section, self.request), name="show_section_title")
        view.show_section_title()
        self.assertFalse(section.hide_title)

    def test_sections_collapsible(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        api.content.transition(page, "publish")
        section_types = get_sections_types()
        for section_type in section_types:
            api.content.create(
                container=page,
                type=section_type,
                title="Title of my {}".format(section_type),
            )
        video_section = getattr(page, "title-of-my-imio-smartweb-sectionvideo")
        video_section.video_url = "https://www.youtube.com/watch?v=_dOAthafoGQ"
        gallery_section = getattr(page, "title-of-my-imio-smartweb-sectiongallery")
        api.content.create(
            container=gallery_section,
            type="Image",
            title="Image",
        )
        files_section = getattr(page, "title-of-my-imio-smartweb-sectionfiles")
        file_obj = api.content.create(
            container=files_section,
            type="File",
            title="My file",
        )
        file_obj.file = NamedBlobFile(data="file data", filename="file.txt")
        links_section = getattr(page, "title-of-my-imio-smartweb-sectionlinks")
        api.content.create(
            container=links_section,
            type="imio.smartweb.BlockLink",
            title="My link",
        )
        postit_section = getattr(page, "title-of-my-imio-smartweb-sectionpostit")
        postits = [{"title": "postit1", "subtitle": "", "description": ""}]
        postit_section.postits = postits

        selections_section = getattr(
            page, "title-of-my-imio-smartweb-sectionselections"
        )
        intids = getUtility(IIntIds)
        selections_section.selected_items = [
            RelationValue(intids.getId(self.page)),
        ]

        for section_id in page.objectIds():
            section = getattr(page, section_id)
            section.collapsible_section = True
            modified(section)
            self.assertFalse(section.hide_title)
        view = queryMultiAdapter((page, self.request), name="full_view")()
        soup = BeautifulSoup(view)
        collapsables = soup.select("div.body-section.collapse")
        self.assertEqual(len(collapsables), len(section_types))

    def test_sections_collapsible_hide_title(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionHTML",
            title="Section HTML",
        )
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertIn("Hide title", view)
        section.collapsible_section = True
        modified(section)
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertNotIn("Hide title", view)
        self.assertFalse(section.hide_title)
        view = queryMultiAdapter((section, self.request), name="hide_section_title")
        view.hide_section_title()
        self.assertFalse(section.hide_title)

    def test_sections_worflows(self):
        wf_tool = api.portal.get_tool("portal_workflow")
        section_types = get_sections_types()
        for section_type in section_types:
            obj = api.content.create(
                container=self.page,
                type=section_type,
                title="Title of my {}".format(section_type),
            )
            chain = wf_tool.getChainFor(obj)
            self.assertEqual(chain, ())

    def test_section_html(self):
        section_html = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionHTML",
            title="Section html",
            id="section-html",
            html="",
        )
        section_html.html = (
            '<div><h1>Perdu.com</h1><embed src="http://www.perdu.com"></embed></div>'
        )
        modified(section_html)
        page_html = getMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn("Perdu.com", page_html)
        self.assertNotIn("iframe", page_html)

    def test_link_section(self):
        links_section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionLinks",
            title="Section links",
        )
        api.content.transition(self.page, "publish")
        link = api.content.create(
            container=links_section,
            type="imio.smartweb.BlockLink",
            title="My link",
        )
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn(
            '<a class="table_image no-image" href="http://nohost/plone/page/section-links/my-link" target="">',
            view(),
        )
        link.image = NamedBlobImage(**make_named_image())
        self.assertIn(
            '<a class="table_image" href="http://nohost/plone/page/section-links/my-link" target="">',
            view(),
        )
        link.open_in_new_tab = True
        self.assertNotIn(
            '<a class="table_image" href="http://nohost/plone/page/section-links/my-link" target="_blank">',
            view(),
        )
        logout()
        clear_cache(self.request)
        view = getMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn(
            '<a class="table_image" href="http://nohost/plone/page/section-links/my-link" target="_blank">',
            view(),
        )

    def test_background_style(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertEqual(view.background_style(section), "")
        section.background_image = NamedBlobImage(**make_named_image())
        self.assertIn(
            "background-image:url(http://nohost/plone/page/section-text/@@images/background_image-750",
            view.background_style(section),
        )

    def test_get_class(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertEqual(view.get_class(section), "sectiontext")
        section.css_class = "my-css"
        self.assertEqual(view.get_class(section), "sectiontext my-css")
        section.bootstrap_css_class = "col-sm-3"
        self.assertEqual(view.get_class(section), "sectiontext my-css col-sm-3")
        section.background_image = NamedBlobImage(**make_named_image())
        self.assertEqual(
            view.get_class(section), "sectiontext my-css col-sm-3 with-background"
        )
