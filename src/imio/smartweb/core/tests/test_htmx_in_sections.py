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
        self.assertIn(f"sizesForm_{section_text_uid}", view())
        self.assertIn(f'hx-boost="{section_text_uid}"', view())
        self.assertIn(f'id="selected_size_{section_text_uid}"', view())
        self.assertIn(f'hx-target="#selected_size_{section_text_uid}"', view())

    def test_options_in_select(self):
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        section_text_view = getMultiAdapter(
            (self.section_text, self.request), name="view"
        )
        available_sizes = section_text_view.get_sizes
        match = re.search(
            r'<form class="form_section_size".*?</form>', view(), re.DOTALL
        )
        form_to_choose_size = match.group(0)
        nb_occurrences = len(re.findall(r"<option", form_to_choose_size))
        self.assertEqual(len(available_sizes), nb_occurrences)
        for size in available_sizes:
            self.assertIn(
                f'<option title="{size["value"]}" value="{size["key"]}" class="icon_{size["key"]}" >',
                form_to_choose_size,
            )
            # self.assertIn(
            #     f'<option value="{size["key"]}">{size["value"]}</option>',
            #     form_to_choose_size,
            # )

    def test_change_section_size(self):
        portal_api.get_current_language = mock.Mock(return_value="en")
        transaction.commit()
        section_text_uid = self.section_text.UID()
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
        div_section_container = (
            '<div class="sortable-section sectiontext" data-id="section-text" style="">'
        )
        self.assertIn(div_section_container, contents)

        select = browser.getControl(name=f"select_{section_text_uid}")
        select.value = "col-sm-12"
        browser.getForm(name=f"sizesForm_{section_text_uid}").submit()
        section_text_view = getMultiAdapter(
            (self.section_text, self.request), name="view"
        )
        self.assertEqual(section_text_view.save_size, json.dumps({}))
        select_name = f"select_{self.section_text.UID()}"
        self.request.form[select_name] = select.value[0]
        self.request.form["_authenticator"] = createToken()
        section_text_view = getMultiAdapter(
            (self.section_text, self.request), name="view"
        )
        section_text_view.save_size
        self.assertEqual(
            section_text_view.save_size,
            json.dumps({"id": "col-sm-12", "title": "Full width"}),
        )
        transaction.commit()

        browser.open(f"{self.page.absolute_url()}/full_view/?language=fr")
        contents = browser.contents
        div_section_container = f'<div class="sortable-section sectiontext {select.value[0]}" data-id="section-text" style="">'
        self.assertIn(div_section_container, contents)
