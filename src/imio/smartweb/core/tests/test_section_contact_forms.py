# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.contact.forms import ContactCustomAddForm
from imio.smartweb.core.contents.sections.contact.forms import ContactCustomEditForm
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.zope import Browser
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import queryUtility
from zope.ramcache.interfaces.ram import IRAMCache

import json
import requests_mock
import transaction

CONTACT_UID = "2dc381f0fb584381b8e4a19c84f53b35"
OTHER_CONTACT_UID = "af7bd1f547034b24a2e0da16c0ba0358"
SEARCH_URL = "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
    CONTACT_UID
)
BOTH_SEARCH_URL = (
    "http://localhost:8080/Plone/@search?UID={}&UID={}&fullobjects=1".format(
        CONTACT_UID, OTHER_CONTACT_UID
    )
)
# RemoteContactsVocabulary feeds the related_contacts field. The edit form
# validates the submitted UID against it on save, so it has to know our UID.
VOCABULARY_URL = (
    "http://localhost:8080/Plone/@search"
    "?portal_type=imio.directory.Contact"
    "&selected_entities=396907b3b1b04a97896b12cc792c77f8"
    "&sort_on=breadcrumb&b_size=1000000"
    "&metadata_fields=UID&metadata_fields=breadcrumb"
)


class TestContactCustomEditForm(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal, type="imio.smartweb.Page", id="page"
        )
        self.section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        payload = get_json("resources/json_contact_informations_raw_mock.json")
        self.both_payload = json.loads(json.dumps(payload))
        payload["items"] = [payload["items"][0]]
        self.payload = payload

    def _make_form(self, form_data):
        self.request.form.clear()
        self.request.form.update(form_data)
        return ContactCustomEditForm(self.section, self.request)

    def _messages(self):
        """(type, text) of the status messages the editor will be shown."""
        return [
            (message.type, message.message)
            for message in IStatusMessage(self.request).show()
        ]

    def test_keeps_the_base_buttons(self):
        # A bare @buttonAndHandler in the class body would shadow the base
        # form's Buttons manager and drop Save / Cancel.
        names = [button.__name__ for button in ContactCustomEditForm.buttons.values()]
        self.assertIn("save", names)
        self.assertIn("cancel", names)
        self.assertIn("load_contact_informations", names)

    def test_keeps_the_base_handlers(self):
        # @buttonAndHandler ALSO setdefaults `handlers` in the class body. A
        # missing `handlers = <Base>.handlers.copy()` leaves the Save button
        # rendered but handler-less: pressing it silently saves nothing.
        for form_class in (ContactCustomEditForm, ContactCustomAddForm):
            handlers = form_class.handlers
            handled = [button.__name__ for button, _handler in handlers._handlers]
            self.assertIn("save", handled, form_class.__name__)
            self.assertIn("cancel", handled, form_class.__name__)
            self.assertIn("load_contact_informations", handled, form_class.__name__)
            for name in ("save", "cancel"):
                self.assertIsNotNone(
                    handlers.getHandler(form_class.buttons[name]),
                    "{} lost its {} handler".format(form_class.__name__, name),
                )

    def test_the_base_handlers_are_not_polluted(self):
        # The copy must be a copy: addHandler mutates in place, so sharing the
        # base manager would add our button's handler to every dexterity form.
        from plone.dexterity.browser.edit import DefaultEditForm

        handled = [button.__name__ for button, _h in DefaultEditForm.handlers._handlers]
        self.assertEqual(sorted(handled), ["cancel", "save"])

    @requests_mock.Mocker()
    def test_reload_writes_one_request_row_per_remote_row(self, m):
        m.get(SEARCH_URL, text=json.dumps(self.payload))
        form = self._make_form(
            {
                "form.buttons.load_contact_informations": "Load",
                "form.widgets.related_contacts": [CONTACT_UID],
            }
        )
        form._reload_display_grids()
        request_form = self.request.form
        self.assertEqual(request_form["form.widgets.phones_display.count"], "2")
        self.assertEqual(
            request_form["form.widgets.phones_display.0.widgets.number"],
            "+3287123456",
        )
        self.assertEqual(
            request_form["form.widgets.phones_display.0.widgets.contact_uid"],
            CONTACT_UID,
        )
        self.assertEqual(
            request_form["form.widgets.phones_display.0.widgets.contact_title"],
            "Administration communale",
        )
        self.assertEqual(
            request_form["form.widgets.phones_display.0.widgets.type"], "Work phone"
        )
        self.assertEqual(
            request_form["form.widgets.phones_display.0.widgets.visible_columns"],
            ["label", "type", "number"],
        )
        self.assertEqual(
            request_form[
                "form.widgets.phones_display.0.widgets.visible_columns-empty-marker"
            ],
            "1",
        )
        self.assertEqual(request_form["form.widgets.mails_display.count"], "1")
        self.assertEqual(request_form["form.widgets.urls_display.count"], "2")
        # A successful load is confirmed to the editor.
        messages = self._messages()
        self.assertEqual([type_ for type_, _text in messages], ["info"])
        self.assertIn("has been loaded", messages[0][1])

    @requests_mock.Mocker()
    def test_reload_preserves_the_checkboxes_already_submitted(self, m):
        m.get(SEARCH_URL, text=json.dumps(self.payload))
        form = self._make_form(
            {
                "form.buttons.load_contact_informations": "Load",
                "form.widgets.related_contacts": [CONTACT_UID],
                "form.widgets.phones_display.count": "1",
                "form.widgets.phones_display.0.widgets.contact_uid": CONTACT_UID,
                "form.widgets.phones_display.0.widgets.number": "+3287123456",
                "form.widgets.phones_display.0.widgets.visible_columns": ["number"],
                "form.widgets.phones_display.0.widgets.visible_columns-empty-marker": "1",  # noqa: E501
            }
        )
        form._reload_display_grids()
        self.assertEqual(
            self.request.form["form.widgets.phones_display.0.widgets.visible_columns"],
            ["number"],
        )
        # The row that was not in the request keeps the all-columns default.
        self.assertEqual(
            self.request.form["form.widgets.phones_display.1.widgets.visible_columns"],
            ["label", "type", "number"],
        )

    @requests_mock.Mocker()
    def test_reload_reads_an_all_unchecked_row_as_an_empty_list(self, m):
        # An unchecked checkbox group submits nothing but its empty-marker.
        # That must be read as "explicitly hidden" ([]), not as "no preference".
        m.get(SEARCH_URL, text=json.dumps(self.payload))
        form = self._make_form(
            {
                "form.buttons.load_contact_informations": "Load",
                "form.widgets.related_contacts": [CONTACT_UID],
                "form.widgets.phones_display.count": "1",
                "form.widgets.phones_display.0.widgets.contact_uid": CONTACT_UID,
                "form.widgets.phones_display.0.widgets.number": "+3287123456",
                "form.widgets.phones_display.0.widgets.visible_columns-empty-marker": "1",  # noqa: E501
            }
        )
        form._reload_display_grids()
        self.assertEqual(
            self.request.form["form.widgets.phones_display.0.widgets.visible_columns"],
            [],
        )

    @requests_mock.Mocker()
    def test_reload_drops_stale_rows(self, m):
        m.get(SEARCH_URL, text=json.dumps(self.payload))
        form = self._make_form(
            {
                "form.buttons.load_contact_informations": "Load",
                "form.widgets.related_contacts": [CONTACT_UID],
                "form.widgets.phones_display.count": "9",
                "form.widgets.phones_display.7.widgets.contact_uid": "gone",
                "form.widgets.phones_display.7.widgets.number": "+3200000000",
            }
        )
        form._reload_display_grids()
        self.assertNotIn(
            "form.widgets.phones_display.7.widgets.number", self.request.form
        )
        self.assertEqual(self.request.form["form.widgets.phones_display.count"], "2")

    def test_reload_without_related_contacts_empties_the_grids(self):
        form = self._make_form({"form.buttons.load_contact_informations": "Load"})
        form._reload_display_grids()
        for field_name in ("phones_display", "mails_display", "urls_display"):
            self.assertEqual(
                self.request.form["form.widgets.{}.count".format(field_name)], "0"
            )
        # No contact really means no row, but the editor must be told why the
        # grids came back empty.
        messages = self._messages()
        self.assertEqual([type_ for type_, _text in messages], ["info"])
        self.assertIn("select a contact", messages[0][1])

    @requests_mock.Mocker()
    def test_reload_keeps_the_grids_when_the_directory_is_unreachable(self, m):
        # get_remote_contacts cannot distinguish a 404 / timeout / unreachable
        # host from "no results": utils.get_json swallows everything and
        # returns None. Emptying the grids here would destroy every recorded
        # visible_columns preference as soon as the editor pressed Save.
        m.get(SEARCH_URL, status_code=404)
        form = self._make_form(
            {
                "form.buttons.load_contact_informations": "Load",
                "form.widgets.related_contacts": [CONTACT_UID],
                "form.widgets.phones_display.count": "1",
                "form.widgets.phones_display.0.widgets.contact_uid": CONTACT_UID,
                "form.widgets.phones_display.0.widgets.number": "+3287123456",
                "form.widgets.phones_display.0.widgets.visible_columns": ["number"],
                "form.widgets.phones_display.0.widgets.visible_columns-empty-marker": "1",  # noqa: E501
            }
        )
        form._reload_display_grids()
        request_form = self.request.form
        self.assertEqual(request_form["form.widgets.phones_display.count"], "1")
        self.assertEqual(
            request_form["form.widgets.phones_display.0.widgets.visible_columns"],
            ["number"],
        )
        self.assertEqual(
            request_form["form.widgets.phones_display.0.widgets.number"], "+3287123456"
        )
        messages = self._messages()
        self.assertEqual([type_ for type_, _text in messages], ["error"])
        self.assertIn("could not be reached", messages[0][1])

    @requests_mock.Mocker()
    def test_reload_accepts_a_single_uid_as_a_string(self, m):
        # A single-valued select submits a bare string, not a list.
        m.get(SEARCH_URL, text=json.dumps(self.payload))
        form = self._make_form(
            {
                "form.buttons.load_contact_informations": "Load",
                "form.widgets.related_contacts": CONTACT_UID,
            }
        )
        form._reload_display_grids()
        self.assertEqual(self.request.form["form.widgets.phones_display.count"], "2")

    @requests_mock.Mocker()
    def test_reload_splits_the_ajaxselect_joined_uids(self, m):
        # related_contacts is an AjaxSelectWidget: several selected contacts
        # arrive as ONE ";"-joined string. Taking it as a single UID would
        # query a bogus "uid1;uid2" and load nothing.
        m.get(BOTH_SEARCH_URL, text=json.dumps(self.both_payload))
        form = self._make_form(
            {
                "form.buttons.load_contact_informations": "Load",
                "form.widgets.related_contacts": "{};{}".format(
                    CONTACT_UID, OTHER_CONTACT_UID
                ),
            }
        )
        form._reload_display_grids()
        # 2 phones for the first contact, 1 for the second.
        self.assertEqual(self.request.form["form.widgets.phones_display.count"], "3")
        self.assertEqual(
            self.request.form["form.widgets.phones_display.2.widgets.contact_uid"],
            OTHER_CONTACT_UID,
        )
        self.assertEqual(
            self.request.form["form.widgets.phones_display.2.widgets.contact_title"],
            "CPAS",
        )


class TestContactInformationsGridRoundTrip(ImioSmartwebTestCase):
    """Load then Save the grids through the real edit form in a browser."""

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal, type="imio.smartweb.Page", id="page"
        )
        self.section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            id="my-contact",
            title="My contact",
        )
        self.section.related_contacts = [CONTACT_UID]
        payload = get_json("resources/json_contact_informations_raw_mock.json")
        payload["items"] = [payload["items"][0]]
        self.payload = payload
        transaction.commit()

    def _browser(self):
        browser = Browser(self.layer["app"])
        browser.addHeader(
            "Authorization",
            "Basic %s:%s"
            % (
                TEST_USER_NAME,
                TEST_USER_PASSWORD,
            ),
        )
        return browser

    def _mock_directory(self, m):
        m.get(SEARCH_URL, text=json.dumps(self.payload))
        m.get(
            VOCABULARY_URL,
            text=json.dumps(
                {
                    "items": [
                        {
                            "UID": CONTACT_UID,
                            "breadcrumb": "Administration communale",
                        }
                    ]
                }
            ),
        )
        # RemoteContactsVocabulary is @ram.cache'd on a time bucket only, so a
        # previous test may have cached an empty vocabulary for this minute.
        cache = queryUtility(IRAMCache)
        if cache is not None:
            cache.invalidateAll()

    def test_load_button_then_save_persists_the_grids(self):
        with requests_mock.Mocker() as m:
            self._mock_directory(m)
            browser = self._browser()
            browser.open("{}/edit".format(self.section.absolute_url()))
            self.assertIn("form.widgets.phones_display", browser.contents)
            browser.getControl(name="form.buttons.load_contact_informations").click()
            content = browser.contents
            # The grid is populated from the live directory payload...
            self.assertIn("+3287123456", content)
            self.assertIn("Administration communale", content)
            self.assertIn("Secretariat", content)
            # ...and the data columns render as frozen labels, i.e. a span
            # plus a hidden input, so they are still submitted on save.
            self.assertIn('<span class="dgf-frozen-label">+3287123456</span>', content)
            self.assertIn(
                'name="form.widgets.phones_display.0.widgets.number"', content
            )
            self.assertEqual(
                browser.getControl(name="form.widgets.phones_display.count").value,
                "2",
            )
            # Hide the label of the first phone, then save.
            browser.getControl(
                name="form.widgets.phones_display.0.widgets.visible_columns:list"
            ).value = ["type", "number"]
            browser.getControl(name="form.buttons.save").click()
            saved_content = browser.contents

        self.assertNotIn("Required input is missing", saved_content)
        self.assertNotIn("system could not process the given value", saved_content)
        self.assertNotIn(
            "There were some errors", saved_content, "the save form errored out"
        )

        transaction.begin()
        section = self.portal["page"]["my-contact"]
        phones = section.phones_display
        self.assertEqual(len(phones), 2, "phones_display did not persist")
        self.assertEqual(phones[0]["contact_uid"], CONTACT_UID)
        self.assertEqual(phones[0]["number"], "+3287123456")
        self.assertEqual(phones[0]["contact_title"], "Administration communale")
        self.assertEqual(phones[0]["visible_columns"], ["type", "number"])
        self.assertEqual(phones[1]["number"], "+32475010203")
        self.assertEqual(phones[1]["visible_columns"], ["label", "type", "number"])
        self.assertEqual(len(section.mails_display), 1)
        self.assertEqual(section.mails_display[0]["mail_address"], "info@example.be")
        self.assertEqual(len(section.urls_display), 2)
        self.assertEqual(section.urls_display[0]["url"], "https://example.be")

    def test_add_form_keeps_its_buttons_and_loads_the_grids(self):
        with requests_mock.Mocker() as m:
            self._mock_directory(m)
            browser = self._browser()
            browser.open(
                "{}/++add++imio.smartweb.SectionContact".format(
                    self.page.absolute_url()
                )
            )
            # Save and Cancel must survive the extra button.
            browser.getControl(name="form.buttons.save")
            browser.getControl(name="form.buttons.cancel")
            browser.getControl(name="form.widgets.related_contacts").value = CONTACT_UID
            browser.getControl(name="form.buttons.load_contact_informations").click()
            content = browser.contents
        self.assertIn("+3287123456", content)
        self.assertIn('<span class="dgf-frozen-label">+3287123456</span>', content)
        self.assertIn("info@example.be", content)
        self.assertIn("https://example.be", content)
