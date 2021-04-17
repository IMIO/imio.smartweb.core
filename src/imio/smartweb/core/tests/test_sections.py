# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.tests.utils import get_sections_types
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.namedfile.file import NamedBlobFile
from plone.protect.authenticator import createToken
from time import sleep
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
import unittest


class SectionsIntegrationTest(unittest.TestCase):

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
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
            id="section-text",
        )
        getMultiAdapter((section, self.request), name="view")()
        self.assertEqual(
            self.request.response.headers["location"],
            "http://nohost/plone/page#section-text",
        )

    def test_get_last_mofication_date(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        self.assertEqual(section.get_last_mofication_date, section.ModificationDate())
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionGallery",
            title="Section Gallery",
        )
        self.assertEqual(section.get_last_mofication_date, section.ModificationDate())
        first_modification = section.get_last_mofication_date
        sleep(1)
        # adding an image to a section causes a reindex of the section, thus
        # changes its last modification date
        api.content.create(
            container=section,
            type="Image",
            title="Image",
        )
        next_modification = section.get_last_mofication_date
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
        file_obj.file = NamedBlobFile(data="file data", filename=u"file.txt")
        view = queryMultiAdapter((section, self.request), name="view")
        self.assertEqual(
            view.get_mime_type_icon(file_obj), "++resource++mimetype.icons/txt.png"
        )
        self.assertEqual(view.human_readable_size(file_obj), "1 KB")
        self.assertEqual(view.get_thumb_scale(), "thumb")
        api.portal.set_registry_record("plone.thumb_scale_listing", "preview")
        self.assertEqual(view.get_thumb_scale(), "preview")
        api.portal.set_registry_record("plone.no_thumbs_lists", True)
        self.assertIsNone(view.get_thumb_scale())

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
        section_types = get_sections_types()
        for section_type in section_types:
            api.content.create(
                container=page,
                type=section_type,
                title="Title of my {}".format(section_type),
            )
        video_section = getattr(page, "title-of-my-imio-smartweb-sectionvideo")
        video_section.video_url = "https://www.youtube.com/watch?v=_dOAthafoGQ"
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(view.count("Title of my "), 2)
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
        file_obj.file = NamedBlobFile(data="file data", filename=u"file.txt")
        links_section = getattr(page, "title-of-my-imio-smartweb-sectionlinks")
        api.content.create(
            container=links_section,
            type="Link",
            title="My link",
        )
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(view.count("Title of my "), len(section_types))

    def test_sections_titles(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
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
        file_obj.file = NamedBlobFile(data="file data", filename=u"file.txt")
        links_section = getattr(page, "title-of-my-imio-smartweb-sectionlinks")
        api.content.create(
            container=links_section,
            type="Link",
            title="My link",
        )
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(view.count("Title of my "), len(section_types))
        for section_id in page.objectIds():
            section = getattr(page, section_id)
            section.hide_title = True
        view = queryMultiAdapter((page, self.request), name="full_view")()
        self.assertEqual(view.count("Title of my "), 0)

    def test_background_style(self):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section text",
        )
        view = queryMultiAdapter((section, self.request), name="view")
        self.assertEqual(view.background_style(), "")
        section.background_image = NamedBlobFile(data="file data", filename=u"file.png")
        self.assertIn(
            "background-image:url('http://nohost/plone/page/section-text/@@images/background_image/large')",
            view.background_style(),
        )
