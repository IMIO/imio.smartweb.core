# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.api import portal as portal_api
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.textfield.value import RichTextValue
from plone.protect.authenticator import createToken
from plone.testing.zope import Browser
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides

import json
import mock
import re
import transaction


class TestSections(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        self.section_text = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionText",
            title="Section Text",
            id="section-text",
        )
        self.section_text.text = RichTextValue(
            "<p>My rich text</p>", "text/html", "text/html"
        )
        # SectionText omits the "alignment" option (aligning a text section
        # with the text sections container makes no sense, it already is
        # one) — use a different section type to test that feature.
        self.section_html = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionHTML",
            title="Section HTML",
            id="section-html",
        )
        api.content.transition(self.page, "publish")

    def test_htmx_not_loaded_for_anonymous(self):
        logout()
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertNotIn("https://unpkg.com/htmx.org@1.9.10/dist/htmx.js", view())

    def test_all_html_elements_are_here(self):
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        # test if htmx well loaded
        self.assertIn("https://unpkg.com/htmx.org@1.9.10/dist/htmx.js", view())
        section_text_uid = self.section_text.UID()
        # test if elements are here and have the right id
        self.assertIn(f'id="select_{section_text_uid}"', view())
        self.assertIn(f'name="select_{section_text_uid}"', view())
        self.assertIn('class="edit-section-link edit-section-size"', view())
        self.assertIn("@@savesize", view())

    def test_options_in_select(self):
        # bootstrap_css_class defaults to "col-sm-12": no blank/no-value
        # option in that case, only the real vocabulary options.
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        section_text_view = getMultiAdapter(
            (self.section_text, self.request), name="view"
        )
        available_sizes = section_text_view.get_sizes
        match = re.search(
            r'<form class="edit-section-link edit-section-size".*?</form>',
            view(),
            re.DOTALL,
        )
        form_to_choose_size = match.group(0)
        nb_occurrences = len(re.findall(r"<option", form_to_choose_size))
        self.assertEqual(len(available_sizes), nb_occurrences)
        for size in available_sizes:
            self.assertIn(f'value="{size["key"]}"', form_to_choose_size)
            self.assertIn(f'title="{size["value"]}"', form_to_choose_size)

    def test_options_in_select_no_width_set(self):
        # The blank/no-value "Width" option only shows up when the field is
        # explicitly unset (e.g. legacy content created before the default
        # was introduced).
        self.section_text.bootstrap_css_class = None
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        section_text_view = getMultiAdapter(
            (self.section_text, self.request), name="view"
        )
        available_sizes = section_text_view.get_sizes
        match = re.search(
            r'<form class="edit-section-link edit-section-size".*?</form>',
            view(),
            re.DOTALL,
        )
        form_to_choose_size = match.group(0)
        nb_occurrences = len(re.findall(r"<option", form_to_choose_size))
        # +1 for the default "Width" option when no size is set
        self.assertEqual(len(available_sizes) + 1, nb_occurrences)

    def test_change_section_size(self):
        portal_api.get_current_language = mock.Mock(return_value="en")
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
        browser.open(f"{self.page.absolute_url()}/full_view/?language=fr")
        contents = browser.contents
        # bootstrap_css_class defaults to "col-sm-12" (full width)
        div_section_container = '<div class="sortable-section sectiontext col-sm-12" data-id="section-text" style="">'
        self.assertIn(div_section_container, contents)

        # Test save_size view directly via request
        section_text_view = getMultiAdapter(
            (self.section_text, self.request), name="view"
        )
        self.assertEqual(section_text_view.save_size, json.dumps({}))
        select_name = f"select_{self.section_text.UID()}"
        self.request.form[select_name] = "col-sm-6"
        self.request.form["_authenticator"] = createToken()
        section_text_view = getMultiAdapter(
            (self.section_text, self.request), name="view"
        )
        section_text_view.save_size
        self.assertEqual(
            section_text_view.save_size,
            json.dumps({"id": "col-sm-6", "title": "Half of width"}),
        )
        transaction.commit()

        browser.open(f"{self.page.absolute_url()}/full_view/?language=fr")
        contents = browser.contents
        div_section_container = '<div class="sortable-section sectiontext col-sm-6" data-id="section-text" style="">'
        self.assertIn(div_section_container, contents)

    def test_alignment_elements_are_here(self):
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        section_html_uid = self.section_html.UID()
        # test if elements are here and have the right id
        self.assertIn(f'id="select_alignment_{section_html_uid}"', view())
        self.assertIn(f'name="select_alignment_{section_html_uid}"', view())
        self.assertIn('class="edit-section-link edit-section-alignment"', view())
        self.assertIn("@@savealignment", view())

    def test_alignment_not_available_for_section_text(self):
        # A text section aligning itself "with the text sections container"
        # makes no sense (it already is one) — the option is omitted from
        # both the standard edit form (see ISectionText) and this front-end
        # toolbar.
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        section_text_uid = self.section_text.UID()
        self.assertNotIn(f'id="select_alignment_{section_text_uid}"', view())
        self.assertNotIn(f'name="select_alignment_{section_text_uid}"', view())

    def test_options_in_select_alignment(self):
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        section_html_view = getMultiAdapter(
            (self.section_html, self.request), name="view"
        )
        available_alignments = section_html_view.get_alignments
        match = re.search(
            r'<form class="edit-section-link edit-section-alignment".*?</form>',
            view(),
            re.DOTALL,
        )
        form_to_choose_alignment = match.group(0)
        nb_occurrences = len(re.findall(r"<option", form_to_choose_alignment))
        # no default/empty option: section_alignment is required with a default
        self.assertEqual(len(available_alignments), nb_occurrences)
        for alignment in available_alignments:
            self.assertIn(f'value="{alignment["key"]}"', form_to_choose_alignment)
            self.assertIn(f'title="{alignment["value"]}"', form_to_choose_alignment)

    def test_change_section_alignment(self):
        portal_api.get_current_language = mock.Mock(return_value="en")
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
        browser.open(f"{self.page.absolute_url()}/full_view/?language=fr")
        contents = browser.contents
        # bootstrap_css_class defaults to "col-sm-12" (full width)
        div_section_container = '<div class="sortable-section sectionhtml col-sm-12" data-id="section-html" style="">'
        self.assertIn(div_section_container, contents)

        # Test save_alignment view directly via request
        section_html_view = getMultiAdapter(
            (self.section_html, self.request), name="view"
        )
        self.assertEqual(section_html_view.save_alignment, json.dumps({}))
        select_name = f"select_alignment_{self.section_html.UID()}"
        self.request.form[select_name] = "text"
        self.request.form["_authenticator"] = createToken()
        section_html_view = getMultiAdapter(
            (self.section_html, self.request), name="view"
        )
        section_html_view.save_alignment
        self.assertEqual(
            section_html_view.save_alignment,
            json.dumps(
                {
                    "id": "text",
                    "title": "Align with text sections container (760px)",
                }
            ),
        )
        transaction.commit()

        browser.open(f"{self.page.absolute_url()}/full_view/?language=fr")
        contents = browser.contents
        div_section_container = '<div class="sortable-section sectionhtml col-sm-12 container-se-text" data-id="section-html" style="">'
        self.assertIn(div_section_container, contents)

    def test_change_section_alignment_restricts_width(self):
        # A section with a non full/half width, switched to "text" alignment,
        # must automatically fall back to full width (col-sm-12).
        self.section_html.bootstrap_css_class = "col-sm-3"
        select_name = f"select_alignment_{self.section_html.UID()}"
        self.request.form[select_name] = "text"
        self.request.form["_authenticator"] = createToken()
        section_html_view = getMultiAdapter(
            (self.section_html, self.request), name="view"
        )
        result = json.loads(section_html_view.save_alignment)
        self.assertEqual(result["id"], "text")
        self.assertEqual(result["size_id"], "col-sm-12")
        self.assertEqual(self.section_html.bootstrap_css_class, "col-sm-12")

        # get_sizes still returns all 6 options: the size <select> must always
        # contain every option in the markup so the toolbar's JS can restore
        # them when switching back to "main" alignment (only their
        # hidden/disabled state is toggled client-side, not the option list
        # itself).
        available_sizes = {size["key"] for size in section_html_view.get_sizes}
        self.assertEqual(len(available_sizes), 6)
