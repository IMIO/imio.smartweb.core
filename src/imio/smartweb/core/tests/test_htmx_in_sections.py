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
import lxml.html
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
        self.assertIn(f'id="select_{section_text_uid}"', view())
        self.assertIn(f'name="select_{section_text_uid}"', view())
        self.assertIn('class="edit-section-link edit-section-size"', view())
        self.assertIn("@@savesize", view())

    def test_options_in_select(self):
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
        # +1 for the default "Size" option when no size is selected
        self.assertEqual(len(available_sizes) + 1, nb_occurrences)
        for size in available_sizes:
            self.assertIn(f'value="{size["key"]}"', form_to_choose_size)
            self.assertIn(f'title="{size["value"]}"', form_to_choose_size)

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
        div_section_container = (
            '<div class="sortable-section sectiontext" data-id="section-text" style="">'
        )
        self.assertIn(div_section_container, contents)

        # Test save_size view directly via request
        section_text_view = getMultiAdapter(
            (self.section_text, self.request), name="view"
        )
        self.assertEqual(section_text_view.save_size, json.dumps({}))
        select_name = f"select_{self.section_text.UID()}"
        self.request.form[select_name] = "col-sm-12"
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
        div_section_container = '<div class="sortable-section sectiontext col-sm-12" data-id="section-text" style="">'
        self.assertIn(div_section_container, contents)

    def test_delete_section_modal_markup(self):
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        rendered = view()
        uid = self.section_text.UID()
        url = self.section_text.absolute_url()
        # le lien pilote l'ouverture de la modale et le chargement de son contenu
        self.assertIn(f'data-bs-target="#delete-modal-{uid}"', rendered)
        self.assertIn(f'hx-get="{url}/delete_confirmation"', rendered)
        self.assertIn(f'hx-target="#delete-modal-body-{uid}"', rendered)
        # le sélecteur ignore le #content-core imbriqué que rend
        # plone.app.linkintegrity dans delete_confirmation_info
        self.assertIn(
            'hx-select=".documentFirstHeading, #content-core:not(#content-core *)"',
            rendered,
        )
        # href conservé comme repli sans htmx
        self.assertIn(f'href="{url}/delete_confirmation"', rendered)
        # la coquille de modale est rendue avec la section
        self.assertIn(f'id="delete-modal-{uid}"', rendered)
        self.assertIn(f'id="delete-modal-body-{uid}"', rendered)
        self.assertIn('hx-boost="true"', rendered)
        self.assertIn('hx-target="closest .sortable-section"', rendered)
        self.assertIn('hx-swap="delete"', rendered)
        # la soumission boostée ne doit pas pousser d'entrée d'historique
        self.assertIn('hx-push-url="false"', rendered)
        # nom accessible de la boîte de dialogue
        self.assertIn(f'id="delete-modal-title-{uid}"', rendered)
        self.assertIn(f'aria-labelledby="delete-modal-title-{uid}"', rendered)

    def test_delete_confirmation_markup_matches_hx_select(self):
        # le hx-select du lien de suppression repose sur la forme de la page
        # delete_confirmation de plone.app.content : un h1.documentFirstHeading,
        # et un #content-core externe qui contient lui-même le #content-core
        # imbriqué de plone.app.linkintegrity.
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
        browser.open(f"{self.section_text.absolute_url()}/delete_confirmation")
        tree = lxml.html.fromstring(browser.contents)
        self.assertTrue(tree.xpath('//h1[contains(@class, "documentFirstHeading")]'))
        outer = tree.xpath(
            '//*[@id="content-core"][not(ancestor::*[@id="content-core"])]'
        )
        self.assertEqual(1, len(outer))
        # le #content-core imbriqué est bien là : c'est lui que le sélecteur
        # doit laisser en place au lieu de l'extraire
        self.assertTrue(outer[0].xpath('.//*[@id="content-core"]'))
        # et le formulaire de confirmation est dans le conteneur externe
        form = outer[0].xpath(".//form")
        self.assertTrue(form)
        self.assertEqual("post", form[0].get("method"))
        # la garde shouldSwap de htmx_js_header.pt n'autorise le swap que pour un
        # POST portant ce nom de bouton exact : le pinner ici évite qu'un
        # renommage côté Plone bloque silencieusement toute suppression
        self.assertTrue(form[0].xpath('.//*[@name="form.buttons.Delete"]'))
        self.assertTrue(form[0].xpath('.//*[@name="form.buttons.Cancel"]'))

    def test_delete_section_modal_not_rendered_for_anonymous(self):
        logout()
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertNotIn("delete-section-modal", view())

    def test_delete_section_modal_close_script_is_served(self):
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        rendered = view()
        self.assertIn("htmx:beforeSwap", rendered)
        # l'écouteur travaille sur l'émetteur de la requête (requestConfig.elt),
        # pas sur la cible du swap qu'expose event.detail.elt
        self.assertIn("event.detail.requestConfig", rendered)
        # et seule une vraie soumission Delete a le droit de swapper
        self.assertIn("form.buttons.Delete", rendered)
        self.assertIn("shouldSwap", rendered)

    def test_htmx_loaded_on_footer_and_herobanner(self):
        htmx_script = "https://unpkg.com/htmx.org@1.9.10/dist/htmx.js"

        settings = getMultiAdapter((self.portal, self.request), name="footer_settings")
        settings.add_footer()
        footer = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.Footer"}
        )[0]
        footer_view = queryMultiAdapter((footer, self.request), name="full_view")
        self.assertIn(htmx_script, footer_view())

        settings = getMultiAdapter(
            (self.portal, self.request), name="herobanner_settings"
        )
        settings.add_herobanner()
        herobanner = self.portal.listFolderContents(
            contentFilter={"portal_type": "imio.smartweb.HeroBanner"}
        )[0]
        herobanner_view = queryMultiAdapter(
            (herobanner, self.request), name="full_view"
        )
        self.assertIn(htmx_script, herobanner_view())
