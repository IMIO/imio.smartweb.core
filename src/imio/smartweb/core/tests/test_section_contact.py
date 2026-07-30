# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from freezegun import freeze_time
from imio.smartweb.common.contact_utils import formatted_schedule
from imio.smartweb.common.contact_utils import get_schedule_for_today
from imio.smartweb.core.contents.sections.contact.utils import build_display_rows
from imio.smartweb.core.contents.sections.contact.utils import ContactProperties
from imio.smartweb.core.contents.sections.contact.utils import get_remote_contacts
from imio.smartweb.core.contents.sections.contact.utils import row_key
from imio.smartweb.core.contents.sections.contact.utils import translated_type_label
from imio.smartweb.core.contents.sections.views import SECTION_ITEMS_HASH_KEY
from imio.smartweb.core.tests.utils import clear_cache
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
from time import sleep
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter

import itertools
import json
import re
import requests
import requests_mock
import transaction


class TestSectionContact(ImioSmartwebTestCase):
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
        self.json_contact = get_json("resources/json_contact_raw_mock.json")
        self.json_contacts = get_json("resources/json_contacts_raw_mock.json")
        self.json_no_contact = get_json("resources/json_no_contact_raw_mock.json")
        self.json_contact_images = get_json(
            "resources/json_contact_images_raw_mock.json"
        )
        self.json_no_image = get_json("resources/json_contact_no_image_raw_mock.json")

    @requests_mock.Mocker()
    def test_contact(self, m):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertIn("My contact", view())
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        self.assertEqual(contact_view.contacts(), [])

        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contacts = [authentic_contact_uid]
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        contact_images_url = "http://localhost:8080/Plone/{}/@search?portal_type=Image&path.depth=1&metadata_fields=modified".format(
            authentic_contact_uid
        )
        m.get(contact_search_url, exc=requests.exceptions.ConnectTimeout)
        self.assertEqual(contact_view.contacts(), [])
        m.get(contact_search_url, status_code=404)
        self.assertEqual(contact_view.contacts(), [])
        m.get(contact_search_url, text=json.dumps(self.json_no_contact))
        self.assertEqual(contact_view.contacts(), [])
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        self.assertIsNotNone(contact_view.contacts())
        json_contact = ContactProperties(self.json_contact.get("items")[0], contact)
        self.assertEqual(json_contact.contact_type_class, "contact-type-organization")
        self.assertNotIn("contact_titles", view())
        self.assertIn("contact_address", view())
        # The fixture's phones/mails/urls are empty and vat_number is null, so
        # the contact informations block now has no content at all and is
        # omitted (no more orphan title / empty <ul>).
        self.assertNotIn("contact_informations", view())
        self.assertIn("schedule", view())
        self.assertNotIn("contact_gallery", view())
        contact.visible_blocks = ["titles", "gallery"]
        self.assertIn("contact_titles", view())
        self.assertNotIn("contact_address", view())
        self.assertNotIn("contact_informations", view())
        self.assertNotIn("schedule", view())
        contact.visible_blocks = ["contact_informations", "address", "schedule"]
        # Was 4: the section title <h2> plus one per block (informations,
        # address, schedule). The informations block is now omitted (fixture
        # has empty phones/mails/urls and a null vat_number), so only 3 remain
        # (section title, address, schedule).
        self.assertEqual(view().count("<h2"), 3)
        contact.visible_blocks = [
            "titles",
            "contact_informations",
            "address",
            "map",
            "schedule",
        ]
        self.assertIn('class="pat-leaflet map"', view())
        # Unchanged: the informations block's title was already an <h3> here
        # (show_main_title is True), so its disappearance doesn't move this
        # count -- these two <h2> are the section title and the contact's own
        # title (contact_titles), untouched by this change.
        self.assertEqual(view().count("<h2"), 2)
        # Was 3: informations, address and schedule titles all rendered as
        # <h3> (show_main_title True). The informations block is now omitted
        # (empty fixture), leaving only address and schedule -> 2.
        self.assertEqual(view().count("<h3"), 2)

        self.assertNotIn("contact_description", view())
        contact.visible_blocks = ["description"]
        self.assertIn("contact_description", view())
        self.assertIn(
            "Description <strong>avec gras</strong> et <br/> retours à la ligne",
            view(),
        )

        contact.visible_blocks = ["titles", "gallery"]
        m.get(contact_images_url, text=json.dumps(self.json_contact_images))
        self.assertIn("contact_gallery", view())

        contact.visible_blocks = ["titles"]
        json_contact = ContactProperties(self.json_contact.get("items")[0], contact)
        images = json_contact.images(contact.image_scale, contact.nb_results_by_batch)
        self.assertNotIn("contact_gallery", view())
        self.assertIsNone(images)

        contact.visible_blocks = ["titles", "gallery"]
        json_contact = ContactProperties(self.json_contact.get("items")[0], contact)
        images = json_contact.images(contact.image_scale, contact.nb_results_by_batch)
        self.assertEqual(len(images[0]), 2)

        json_contact = ContactProperties(self.json_contact.get("items")[0], contact)
        m.get(contact_images_url, text=json.dumps(self.json_no_image))
        images = json_contact.images(contact.image_scale, contact.nb_results_by_batch)
        self.assertIsNone(images)

        m.get(contact_images_url, status_code=404)
        images = json_contact.images(contact.image_scale, contact.nb_results_by_batch)
        self.assertIsNone(images)

        m.get(contact_images_url, exc=requests.exceptions.ConnectTimeout)
        images = json_contact.images(contact.image_scale, contact.nb_results_by_batch)
        self.assertIsNone(images)

    @requests_mock.Mocker()
    def test_sorted_contacts_are_empty(self, m):
        # TODO Separate test test_sorted_contacts_is_none /
        # test_sorted_contacts 'cause of Memoize ??!!
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        self.assertEqual(contact_view.contacts(), [])

    @requests_mock.Mocker()
    def test_sorted_contacts(self, m):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        authentic_contact_uid = [
            "2dc381f0fb584381b8e4a19c84f53b35",
            "af7bd1f547034b24a2e0da16c0ba0358",
        ]
        contact.related_contacts = authentic_contact_uid
        uids = "&UID=".join(contact.related_contacts)
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(uids)
        )
        m.get(contact_search_url, text=json.dumps(self.json_contacts))
        self.assertIsNotNone(contact_view.contacts())
        # contact_view.contacts()[0][0] : first contact of first bash
        self.assertEqual(
            contact.related_contacts[0], contact_view.contacts()[0][0].get("UID")
        )

        # Change sort order
        authentic_contact_uid = [
            "af7bd1f547034b24a2e0da16c0ba0358",
            "2dc381f0fb584381b8e4a19c84f53b35",
        ]
        contact.related_contacts = authentic_contact_uid
        uids = "&UID=".join(contact.related_contacts)
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(uids)
        )
        m.get(contact_search_url, text=json.dumps(self.json_contacts))
        self.assertIsNotNone(contact_view.contacts())
        # contact_view.contacts()[0][0] : first contact of first bash
        self.assertEqual(
            contact.related_contacts[0], contact_view.contacts()[0][0].get("UID")
        )

    def test_toggle_title_visibility(self):
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            title="Page",
        )
        api.content.transition(page, "publish")
        # We can't edit title visibility of a "Contact" section.
        # And visibility of contact title is False.
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionContact",
            title="Title of my contact",
        )
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
        browser.open("{}/edit".format(section.absolute_url()))
        content = browser.contents
        soup = BeautifulSoup(content)
        hide_title_true = soup.find(id="form-widgets-hide_title-0")
        self.assertIsNotNone(hide_title_true)
        self.assertEqual(len(hide_title_true), 0)
        self.assertEqual(hide_title_true["type"], "hidden")
        self.assertEqual(hide_title_true["value"], "selected")
        hide_title_false = soup.find(id="form-widgets-hide_title-1")
        self.assertIsNone(hide_title_false)

        browser.open("{}/++add++{}".format(page.absolute_url(), section.portal_type))
        content = browser.contents
        soup = BeautifulSoup(content)
        hide_title_true = soup.find(id="form-widgets-hide_title-0")
        self.assertIsNotNone(hide_title_true)
        self.assertEqual(len(hide_title_true), 0)
        self.assertEqual(hide_title_true["type"], "hidden")
        self.assertEqual(hide_title_true["value"], "selected")
        hide_title_false = soup.find(id="form-widgets-hide_title-1")
        self.assertIsNone(hide_title_false)

    @requests_mock.Mocker()
    def test_opening_informations(self, m):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        json_contact = contact_view.get_contact_properties(
            self.json_contact.get("items")[0]
        )
        self.assertIsNotNone(json_contact.get_opening_informations())

        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow_str = (today + timedelta(days=1)).strftime("%Y-%m-%d")

        self.json_contact["items"][0]["exceptional_closure"] = [
            {"date": today_str, "title": "Exceptional closure !"}
        ]
        json_contact = contact_view.get_contact_properties(
            self.json_contact.get("items")[0]
        )
        self.assertIsNotNone(json_contact.get_opening_informations())

        today = datetime.now().strftime("%Y-%m-%d")
        self.json_contact["items"][0]["multi_schedule"][0]["dates"] = [
            {"end_date": tomorrow_str, "start_date": yesterday_str}
        ]
        json_contact = contact_view.get_contact_properties(
            self.json_contact.get("items")[0]
        )
        self.assertIsNotNone(json_contact.get_opening_informations())

        self.json_contact["items"][0]["multi_schedule"][0]["dates"] = [
            {"end_date": yesterday_str, "start_date": yesterday_str}
        ]
        json_contact = contact_view.get_contact_properties(
            self.json_contact.get("items")[0]
        )
        self.assertIsNotNone(json_contact.get_opening_informations())

    # {'afternoonend': '', 'afternoonstart': '', 'comment': 'vendredi : apéro à midi', 'morningend': '11:00', 'morningstart': '08:30'}
    def test_get_schedule_for_today(self):
        schedule = {
            "morningstart": "08:30",
            "morningend": "12:00",
            "afternoonstart": "13:00",
            "afternoonend": "17:00",
            "comment": "",
        }
        with freeze_time("2021-09-14 8:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertIn("Open at", result)
        with freeze_time("2021-09-14 10:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Open")
        with freeze_time("2021-09-14 12:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Lunch time")
        with freeze_time("2021-09-14 18:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Closed")

        schedule = {
            "morningstart": "08:30",
            "morningend": "12:00",
            "afternoonstart": "",
            "afternoonend": "",
            "comment": "",
        }
        with freeze_time("2021-09-14 7:30:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual("Open at  08:30", result)
        with freeze_time("2021-09-14 8:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertIn("Open at", result)
        with freeze_time("2021-09-14 10:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Open")
        with freeze_time("2021-09-14 12:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Closed")

        schedule = {
            "morningstart": "",
            "morningend": "",
            "afternoonstart": "13:00",
            "afternoonend": "17:00",
            "comment": "",
        }
        with freeze_time("2021-09-14 13:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertIn(result, "Open at")
        with freeze_time("2021-09-14 14:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Open")
        with freeze_time("2021-09-14 17:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Closed")

        schedule = {
            "morningstart": "8:30",
            "morningend": "",
            "afternoonstart": "",
            "afternoonend": "17:00",
            "comment": "",
        }
        with freeze_time("2021-09-14 8:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertIn("Open at", result)
        with freeze_time("2021-09-14 12:20:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Open")
        with freeze_time("2021-09-14 17:00:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Closed")

        schedule = {
            "morningstart": "8:30",
            "morningend": "",
            "afternoonstart": "",
            "afternoonend": "17:00",
            "comment": "Full day opening!",
        }
        with freeze_time("2021-09-14 12:20:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Open (Full day opening!)")

        schedule = {
            "morningstart": "",
            "morningend": "",
            "afternoonstart": "",
            "afternoonend": "",
            "comment": "",
        }
        with freeze_time("2021-09-14 12:20:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Closed")

        schedule = {
            "morningstart": "",
            "morningend": "",
            "afternoonstart": "",
            "afternoonend": "",
            "comment": "It's closed!",
        }
        with freeze_time("2021-09-14 12:20:00"):
            result = get_schedule_for_today(schedule)
            self.assertEqual(result, "Closed (It's closed!)")

    def test_formatted_schedule(self):
        schedule = {
            "morningstart": "08:30",
            "morningend": "12:00",
            "afternoonstart": "13:00",
            "afternoonend": "17:00",
            "comment": "",
        }
        self.assertEqual("08:30 - 12:00 | 13:00 - 17:00", formatted_schedule(schedule))

        schedule = {
            "morningstart": "08:30",
            "morningend": "",
            "afternoonstart": "",
            "afternoonend": "17:00",
            "comment": "",
        }
        self.assertEqual("08:30 - 17:00", formatted_schedule(schedule))

        schedule = {
            "morningstart": "08:30",
            "morningend": "12:00",
            "afternoonstart": "",
            "afternoonend": "",
            "comment": "",
        }
        self.assertEqual("08:30 - 12:00", formatted_schedule(schedule))

        schedule = {
            "morningstart": "",
            "morningend": "",
            "afternoonstart": "",
            "afternoonend": "",
            "comment": "",
        }
        self.assertEqual("Closed", formatted_schedule(schedule))

        schedule = {
            "morningstart": "",
            "morningend": "",
            "afternoonstart": "13:00",
            "afternoonend": "17:00",
            "comment": "",
        }
        self.assertEqual("13:00 - 17:00", formatted_schedule(schedule))

        schedule = {
            "morningstart": "",
            "morningend": "",
            "afternoonstart": "13:00",
            "afternoonend": "17:00",
            "comment": "Opening only on PM",
        }
        self.assertEqual(
            "13:00 - 17:00 (Opening only on PM)", formatted_schedule(schedule)
        )

    @requests_mock.Mocker()
    def test_formatted_with_multi_schedule(self, m):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contacts = [authentic_contact_uid]
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        json_contact = ContactProperties(self.json_contact.get("items")[0], contact)
        with freeze_time("2021-06-30 12:20:00"):
            schedule = json_contact.get_opening_informations()
            self.assertEqual(
                "13:00 - 17:30 (Ouverture PM)",
                json_contact.formatted_schedule(schedule),
            )
        with freeze_time("2021-07-07 12:20:00"):
            schedule = json_contact.get_opening_informations()
            self.assertEqual(
                "13:00 - 15:00 (Ouverture PM vacances)",
                json_contact.formatted_schedule(schedule),
            )
        with freeze_time("2021-09-01 12:20:00"):
            schedule = json_contact.get_opening_informations()
            self.assertEqual(
                "13:00 - 17:30 (Ouverture PM)",
                json_contact.formatted_schedule(schedule),
            )
        with freeze_time("2021-12-29 12:20:00"):
            schedule = json_contact.get_opening_informations()
            self.assertEqual(
                "13:00 - 15:00 (Ouverture PM vacances)",
                json_contact.formatted_schedule(schedule),
            )

    @requests_mock.Mocker()
    def test_empty_schedule(self, m):
        json_contact_empty_schedule = get_json(
            "resources/json_contact_empty_schedule_raw_mock.json"
        )
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        contact.visible_blocks = ["titles", "gallery", "schedule"]
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contacts = [authentic_contact_uid]
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        m.get(contact_search_url, text=json.dumps(json_contact_empty_schedule))
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        json_contact = ContactProperties(
            json_contact_empty_schedule.get("items")[0], contact
        )
        is_empty = json_contact.is_empty_schedule()
        self.assertEqual(is_empty, True)
        self.assertNotIn('class="schedule"', view())
        json_contact_empty_schedule["items"][0].get("schedule")["monday"] = {
            "morningstart": "8:00",
            "morningend": "12:00",
            "afternoonstart": "",
            "afternoonend": "",
            "comments": "",
        }
        clear_cache(self.request)
        m.get(contact_search_url, text=json.dumps(json_contact_empty_schedule))
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        json_contact = ContactProperties(
            json_contact_empty_schedule.get("items")[0], contact
        )
        is_empty = json_contact.is_empty_schedule()
        self.assertEqual(is_empty, False)
        self.assertIn('class="schedule"', view())

    @requests_mock.Mocker()
    def test_leadimage_orientation(self, m):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contacts = [authentic_contact_uid]
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        contact.visible_blocks = ["titles", "leadimage"]
        m.get(contact_search_url, text=json.dumps(self.json_contact))

        # Test default orientation (should be paysage by default)
        self.assertNotIn("contact_leadimage display-portrait", view())
        self.assertNotIn("contact_leadimage display-carre", view())
        self.assertIn("contact_leadimage display-paysage", view())

        # Test portrait orientation
        contact.orientation = "portrait"
        self.assertIn("contact_leadimage display-portrait", view())
        self.assertNotIn("contact_leadimage display-carre", view())
        self.assertNotIn("contact_leadimage display-paysage", view())

        # Test carre (square) orientation
        contact.orientation = "carre"
        self.assertIn("contact_leadimage display-carre", view())
        self.assertNotIn("contact_leadimage display-portrait", view())
        self.assertNotIn("contact_leadimage display-paysage", view())

        # Test paysage (landscape) orientation
        contact.orientation = "paysage"
        self.assertIn("contact_leadimage display-paysage", view())
        self.assertNotIn("contact_leadimage display-portrait", view())
        self.assertNotIn("contact_leadimage display-carre", view())

    @requests_mock.Mocker()
    def test_contact_modified(self, m):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contacts = [authentic_contact_uid]
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        contact_view = queryMultiAdapter((contact, self.request), name="view")

        annotations = IAnnotations(contact)
        self.assertIsNone(annotations.get(SECTION_ITEMS_HASH_KEY))
        self.assertIsNotNone(contact_view.contacts())
        hash_1 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertIsNotNone(hash_1)
        first_modification = self.page.ModificationDate()

        sleep(1)
        m.get(contact_search_url, text=json.dumps(self.json_no_contact))
        clear_cache(self.request)
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        self.assertEqual(contact_view.contacts(), [])
        # refresh_modification_date doesn't calculate when json_data is None
        # For this section, this is the case
        # For other sections, we get json_data with empty "items"
        # Refactoring needed to ensure clarity ?
        next_modification = self.page.ModificationDate()
        hash_2 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertEqual(hash_1, hash_2)
        self.assertEqual(first_modification, next_modification)

        sleep(1)
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        self.assertEqual(contact_view.contacts(), [])
        last_modification = self.page.ModificationDate()
        hash_3 = annotations.get(SECTION_ITEMS_HASH_KEY)
        self.assertEqual(hash_2, hash_3)
        self.assertEqual(next_modification, last_modification)

        # TODO we should test with various contact sections containing
        # contacts

    @requests_mock.Mocker()
    def test_contact_urls(self, m):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        contact.visible_blocks = ["contact_informations"]
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contacts = [authentic_contact_uid]
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        # contact_view = queryMultiAdapter((contact, self.request), name="view")
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertNotIn('Error in section : "My contact"', view())
        self.assertNotIn("contact_informations_social", view())

        self.json_contact.get("items")[0]["urls"] = None
        sleep(1)
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        # contact_view = queryMultiAdapter((contact, self.request), name="view")
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertNotIn('Error in section : "My contact"', view())
        self.assertNotIn("contact_informations_social", view())

        urls = [
            {"type": None, "url": None},
            {"type": None, "url": None},
            {"type": None, "url": None},
        ]
        self.json_contact.get("items")[0]["urls"] = urls
        sleep(1)
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        # contact_view = queryMultiAdapter((contact, self.request), name="view")
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertNotIn('Error in section : "My contact"', view())
        self.assertNotIn("contact_informations_social", view())

        urls = [
            {"type": None, "url": None},
            {"type": "facebook", "url": "Yolo"},
            {"type": None, "url": None},
        ]
        self.json_contact.get("items")[0]["urls"] = urls
        sleep(1)
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        # contact_view = queryMultiAdapter((contact, self.request), name="view")
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        self.assertNotIn('Error in section : "My contact"', view())
        self.assertIn("contact_informations_social", view())

    def test_display_fields_exist_and_start_empty(self):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        for field_name in ("phones_display", "mails_display", "urls_display"):
            self.assertIsNone(getattr(contact, field_name))

    def test_display_fields_accept_rows(self):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        contact.phones_display = [
            {
                "contact_uid": "uid1",
                "contact_title": "Administration communale",
                "label": "Secretariat",
                "type": "Work phone",
                "number": "+3287123456",
                "visible_columns": ["label", "number"],
            }
        ]
        self.assertEqual(
            contact.phones_display[0]["visible_columns"], ["label", "number"]
        )

    def test_display_grids_forbid_manual_row_editing(self):
        # Rows come from the directory; an editor must not add or remove any.
        from imio.smartweb.core.contents import ISectionContact
        from plone.autoform.interfaces import WIDGETS_KEY
        from plone.supermodel.utils import mergedTaggedValueDict

        widgets = mergedTaggedValueDict(ISectionContact, WIDGETS_KEY)
        for field_name in ("phones_display", "mails_display", "urls_display"):
            factory = widgets[field_name]
            self.assertFalse(factory.params["allow_insert"])
            self.assertFalse(factory.params["allow_delete"])
            self.assertFalse(factory.params["allow_reorder"])
            self.assertFalse(factory.params["auto_append"])

    @requests_mock.Mocker()
    def test_displayed_columns_drive_the_render(self, m):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        section.visible_blocks = ["contact_informations"]
        uid = "2dc381f0fb584381b8e4a19c84f53b35"
        section.related_contacts = [uid]
        url = "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(uid)
        payload = get_json("resources/json_contact_informations_raw_mock.json")
        payload["items"] = [payload["items"][0]]
        m.get(url, text=json.dumps(payload))

        view = queryMultiAdapter((self.page, self.request), name="full_view")
        rendered = view()
        self.assertIn("+3287123456", rendered)
        self.assertIn("Secretariat", rendered)
        self.assertIn("Work phone", rendered)

        # Hide the label and the type of the first phone.
        section.phones_display = [
            {
                "contact_uid": uid,
                "number": "+3287123456",
                "visible_columns": ["number"],
            }
        ]
        sleep(1)
        m.get(url, text=json.dumps(payload))
        clear_cache(self.request)
        rendered = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn("+3287123456", rendered)
        self.assertNotIn("Secretariat", rendered)
        # "Direction" is untouched, so its own label is still there.
        self.assertIn("Direction", rendered)

        # Uncheck every column: the row disappears entirely.
        section.phones_display = [
            {"contact_uid": uid, "number": "+3287123456", "visible_columns": []}
        ]
        sleep(1)
        m.get(url, text=json.dumps(payload))
        clear_cache(self.request)
        rendered = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertNotIn("+3287123456", rendered)
        self.assertIn("+32475010203", rendered)

    @requests_mock.Mocker()
    def test_no_empty_list_nor_orphan_title_when_everything_is_hidden(self, m):
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        section.visible_blocks = ["contact_informations"]
        uid = "2dc381f0fb584381b8e4a19c84f53b35"
        section.related_contacts = [uid]
        url = "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(uid)
        payload = get_json("resources/json_contact_informations_raw_mock.json")
        payload["items"] = [payload["items"][0]]
        section.phones_display = [
            {"contact_uid": uid, "number": "+3287123456", "visible_columns": []},
            {"contact_uid": uid, "number": "+32475010203", "visible_columns": []},
        ]
        section.mails_display = [
            {
                "contact_uid": uid,
                "mail_address": "info@example.be",
                "visible_columns": [],
            }
        ]
        section.urls_display = [
            {"contact_uid": uid, "url": "https://example.be", "visible_columns": []},
            {
                "contact_uid": uid,
                "url": "https://facebook.com/example",
                "visible_columns": [],
            },
        ]
        m.get(url, text=json.dumps(payload))
        rendered = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertNotIn("contact_informations_genral", rendered)
        self.assertNotIn("contact_informations_social", rendered)
        self.assertNotIn('<h2 class="informations"', rendered)

    @requests_mock.Mocker()
    def test_contact_informations_unchecked_skips_the_grids(self, m):
        # visible_blocks is the master switch: the DGFs are not even consulted.
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        section.visible_blocks = ["titles"]
        uid = "2dc381f0fb584381b8e4a19c84f53b35"
        section.related_contacts = [uid]
        url = "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(uid)
        payload = get_json("resources/json_contact_informations_raw_mock.json")
        payload["items"] = [payload["items"][0]]
        m.get(url, text=json.dumps(payload))
        rendered = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertNotIn("+3287123456", rendered)
        self.assertNotIn("contact_informations_genral", rendered)

    @requests_mock.Mocker()
    def test_url_type_only_renders_icon_without_link(self, m):
        # `type` and `url` are independently checkable for a urls row. With
        # only `type` checked, the editor asked for the icon but not the
        # link: the icon must still render, but NOT wrapped in an <a> (no
        # href to link to).
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        section.visible_blocks = ["contact_informations"]
        uid = "2dc381f0fb584381b8e4a19c84f53b35"
        section.related_contacts = [uid]
        url = "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(uid)
        payload = get_json("resources/json_contact_informations_raw_mock.json")
        payload["items"] = [payload["items"][0]]
        section.urls_display = [
            {
                "contact_uid": uid,
                "url": "https://facebook.com/example",
                "visible_columns": ["type"],
            }
        ]
        m.get(url, text=json.dumps(payload))
        rendered = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn("bi-facebook", rendered)
        self.assertNotIn('href="https://facebook.com/example"', rendered)

    @requests_mock.Mocker()
    def test_url_only_hides_icon_and_type_leak(self, m):
        # With only `url` checked, the link renders but neither the icon nor
        # the translated type label may appear anywhere -- including as a
        # `title=` attribute, which is the actual leak this guards against.
        section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        section.visible_blocks = ["contact_informations"]
        uid = "2dc381f0fb584381b8e4a19c84f53b35"
        section.related_contacts = [uid]
        url = "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(uid)
        payload = get_json("resources/json_contact_informations_raw_mock.json")
        payload["items"] = [payload["items"][0]]
        section.urls_display = [
            {
                "contact_uid": uid,
                "url": "https://facebook.com/example",
                "visible_columns": ["url"],
            }
        ]
        m.get(url, text=json.dumps(payload))
        rendered = queryMultiAdapter((self.page, self.request), name="full_view")()
        self.assertIn('href="https://facebook.com/example"', rendered)
        self.assertNotIn("bi-facebook", rendered)
        self.assertNotIn("Facebook", rendered)
        # The title expression falls back to `nothing`, not to '', so TAL drops
        # the attribute instead of emitting an empty `title=""`. Scoped to this
        # anchor: unrelated Plone chrome does emit `title=""` elsewhere.
        anchor = re.search(r"<a[^>]*https://facebook\.com/example[^>]*>", rendered)
        self.assertIsNotNone(anchor)
        self.assertNotIn("title=", anchor.group(0))


class TestContactPropertiesMethods(ImioSmartwebTestCase):
    """Direct unit tests for ContactProperties methods in contact/utils.py"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page",
        )
        self.section = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact section",
        )
        self._contact_data = {
            "@id": "http://localhost:8080/Plone/contact1",
            "title": "My Contact",
            "modified": "2021-05-19T08:04:06+00:00",
            "type": {"token": "organization", "title": "Organization"},
            "geolocation": {"latitude": 50.4, "longitude": 4.7},
            "street": "Rue de la Paix",
            "number": "1",
            "complement": None,
            "zipcode": "4000",
            "city": "Liège",
            "country": {"token": "be", "title": "Belgique"},
            "description": "Hello **world**",
            "logo": None,
            "image": None,
            "urls": [],
            "UID": "2dc381f0fb584381b8e4a19c84f53b35",
            "phones": [],
            "mails": [],
        }

    def _make_contact_properties(self, overrides=None):
        data = {**self._contact_data}
        if overrides:
            data.update(overrides)
        return ContactProperties(data, self.section)

    # --- logo ---

    def test_logo_returns_empty_when_none(self):
        cp = self._make_contact_properties({"logo": None})
        self.assertEqual(cp.logo(), "")

    def test_logo_returns_url_when_set(self):
        cp = self._make_contact_properties({"logo": {"content-type": "image/jpeg"}})
        result = cp.logo()
        self.assertIn("@@images/logo/preview", result)
        self.assertIn("cache_key=", result)

    # --- leadimage ---

    def test_leadimage_returns_empty_when_none(self):
        cp = self._make_contact_properties({"image": None})
        self.assertEqual(cp.leadimage(), "")

    def test_leadimage_default_orientation_is_paysage(self):
        cp = self._make_contact_properties({"image": {"content-type": "image/jpeg"}})
        result = cp.leadimage()
        self.assertIn("@@images/image/paysage_affiche", result)
        self.assertIn("cache_key=", result)

    def test_leadimage_uses_section_orientation(self):
        self.section.orientation = "portrait"
        cp = self._make_contact_properties({"image": {"content-type": "image/jpeg"}})
        result = cp.leadimage()
        self.assertIn("@@images/image/portrait_affiche", result)

    # --- data_geojson ---

    def test_data_geojson_returns_valid_geojson_structure(self):
        cp = self._make_contact_properties()
        result = json.loads(cp.data_geojson())
        self.assertEqual(result["type"], "Feature")
        self.assertEqual(result["geometry"]["type"], "Point")
        self.assertEqual(result["geometry"]["coordinates"], [4.7, 50.4])
        self.assertIn("popup", result["properties"])

    def test_data_geojson_popup_contains_itinerary_link(self):
        cp = self._make_contact_properties()
        result = json.loads(cp.data_geojson())
        self.assertIn("google.com", result["properties"]["popup"])

    # --- get_itinerary_link ---

    def test_get_itinerary_link_with_full_address(self):
        cp = self._make_contact_properties()
        result = cp.get_itinerary_link()
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("https://www.google.com/maps/dir/"))
        self.assertIn("Rue de la Paix", result)

    def test_get_itinerary_link_returns_none_when_no_address(self):
        cp = self._make_contact_properties(
            {
                "street": None,
                "number": None,
                "complement": None,
                "zipcode": None,
                "city": None,
                "country": None,
            }
        )
        self.assertIsNone(cp.get_itinerary_link())

    def test_get_itinerary_link_includes_country_title(self):
        cp = self._make_contact_properties()
        result = cp.get_itinerary_link()
        self.assertIn("Belgique", result)

    # --- get_translated_url_type ---

    def test_get_translated_url_type_capitalizes_label(self):
        cp = self._make_contact_properties()
        result = cp.get_translated_url_type("facebook")
        self.assertIsNotNone(result)
        self.assertTrue(result[0].isupper())

    def test_get_translated_url_type_already_capitalized(self):
        cp = self._make_contact_properties()
        result = cp.get_translated_url_type("Website")
        self.assertIsNotNone(result)

    # --- formatted_address ---

    def test_formatted_address_with_full_data(self):
        cp = self._make_contact_properties()
        result = cp.formatted_address()
        self.assertIsNotNone(result)
        self.assertIn("Rue de la Paix", result["street"])
        self.assertIn("1", result["street"])
        self.assertIn("4000", result["entity"])
        self.assertIn("Liège", result["entity"])
        self.assertNotEqual(result["country"], "")

    def test_formatted_address_returns_none_when_all_empty(self):
        cp = self._make_contact_properties(
            {
                "street": None,
                "number": None,
                "complement": None,
                "zipcode": None,
                "city": None,
                "country": None,
            }
        )
        self.assertIsNone(cp.formatted_address())

    def test_formatted_address_without_country(self):
        cp = self._make_contact_properties({"country": None})
        result = cp.formatted_address()
        self.assertIsNotNone(result)
        self.assertEqual(result["country"], "")

    def test_formatted_address_includes_complement(self):
        cp = self._make_contact_properties({"complement": "Bte 2"})
        result = cp.formatted_address()
        self.assertIn("Bte 2", result["street"])

    # --- get_urls ---

    def test_get_urls_returns_none_when_all_items_have_none_type_and_url(self):
        cp = self._make_contact_properties(
            {"urls": [{"type": None, "url": None}, {"type": None, "url": None}]}
        )
        self.assertIsNone(cp.get_urls)

    def test_get_urls_filters_out_null_items(self):
        cp = self._make_contact_properties(
            {
                "urls": [
                    {"type": None, "url": None},
                    {"type": "facebook", "url": "https://facebook.com"},
                ]
            }
        )
        result = cp.get_urls
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "facebook")

    def test_get_urls_returns_none_when_urls_is_none(self):
        cp = self._make_contact_properties({"urls": None})
        self.assertIsNone(cp.get_urls)

    def test_get_urls_returns_non_list_value_as_is(self):
        cp = self._make_contact_properties({"urls": "not-a-list"})
        self.assertEqual(cp.get_urls, "not-a-list")

    # --- description ---

    def test_description_renders_markdown_bold(self):
        cp = self._make_contact_properties({"description": "Hello **world**"})
        self.assertIn("<strong>world</strong>", cp.description)

    def test_description_renders_line_breaks(self):
        cp = self._make_contact_properties({"description": "line1\r\nline2"})
        self.assertIn("<br/>", cp.description)

    # --- __getattr__ ---

    def test_getattr_returns_value_from_contact_dict(self):
        cp = self._make_contact_properties()
        self.assertEqual(cp.title, "My Contact")

    def test_getattr_returns_none_for_missing_key(self):
        cp = self._make_contact_properties()
        self.assertIsNone(cp.nonexistent_key)

    # --- displayed_rows ---

    _PHONES = [
        {"label": "Secretariat", "type": "work", "number": "+3287123456"},
        {"label": "Direction", "type": "cell", "number": "+32475010203"},
    ]

    def test_displayed_rows_without_preference_shows_every_column(self):
        cp = self._make_contact_properties({"phones": self._PHONES})
        rows = cp.displayed_rows("phones")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["columns"], {"label", "type", "number"})
        self.assertEqual(rows[0]["data"]["number"], "+3287123456")

    def test_displayed_rows_returns_the_remote_row_by_reference(self):
        # `self.contact` is cached JSON shared across renders: `data` must be
        # the SAME dict object as the remote row, never a copy, and must
        # never gain the "columns" key. `_PHONES` entries are shared by
        # reference into `self.contact["phones"]` (only the top-level contact
        # dict is copied by `_make_contact_properties`), so `assertIs` here
        # actually exercises identity, not just equality.
        cp = self._make_contact_properties({"phones": self._PHONES})
        rows = cp.displayed_rows("phones")
        self.assertIs(rows[0]["data"], self._PHONES[0])
        self.assertNotIn("columns", rows[0]["data"])

    def test_displayed_rows_with_a_subset_returns_that_subset(self):
        self.section.phones_display = [
            {
                "contact_uid": "2dc381f0fb584381b8e4a19c84f53b35",
                "number": "+3287123456",
                "visible_columns": ["number"],
            }
        ]
        cp = self._make_contact_properties({"phones": self._PHONES})
        rows = cp.displayed_rows("phones")
        self.assertEqual(rows[0]["columns"], {"number"})
        # The unlisted row keeps the default.
        self.assertEqual(rows[1]["columns"], {"label", "type", "number"})

    def test_displayed_rows_hides_a_row_with_an_empty_preference(self):
        self.section.phones_display = [
            {
                "contact_uid": "2dc381f0fb584381b8e4a19c84f53b35",
                "number": "+3287123456",
                "visible_columns": [],
            }
        ]
        cp = self._make_contact_properties({"phones": self._PHONES})
        rows = cp.displayed_rows("phones")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["data"]["number"], "+32475010203")

    def test_displayed_rows_distinguishes_none_from_an_empty_list(self):
        # THE critical invariant. `None` means "no preference recorded" and
        # must show every column; `[]` means "explicitly hidden". Normalising
        # one into the other would either resurrect hidden rows or wipe the
        # contact informations of every existing section.
        base = {
            "contact_uid": "2dc381f0fb584381b8e4a19c84f53b35",
            "number": "+3287123456",
        }
        cp = self._make_contact_properties({"phones": self._PHONES[:1]})

        self.section.phones_display = [{**base, "visible_columns": None}]
        rows_for_none = cp.displayed_rows("phones")

        self.section.phones_display = [{**base, "visible_columns": []}]
        rows_for_empty = cp.displayed_rows("phones")

        self.assertEqual(len(rows_for_none), 1)
        self.assertEqual(rows_for_none[0]["columns"], {"label", "type", "number"})
        self.assertEqual(rows_for_empty, [])

    def test_displayed_rows_ignores_a_preference_from_another_contact(self):
        self.section.phones_display = [
            {
                "contact_uid": "another-uid",
                "number": "+3287123456",
                "visible_columns": [],
            }
        ]
        cp = self._make_contact_properties({"phones": self._PHONES})
        self.assertEqual(len(cp.displayed_rows("phones")), 2)

    def test_displayed_rows_drops_unknown_columns(self):
        # A stale preference naming a column that no longer exists must not
        # leak into the render.
        self.section.phones_display = [
            {
                "contact_uid": "2dc381f0fb584381b8e4a19c84f53b35",
                "number": "+3287123456",
                "visible_columns": ["number", "gone"],
            }
        ]
        cp = self._make_contact_properties({"phones": self._PHONES})
        self.assertEqual(cp.displayed_rows("phones")[0]["columns"], {"number"})

    def test_displayed_rows_skips_rows_without_a_key(self):
        cp = self._make_contact_properties(
            {
                "urls": [
                    {"type": None, "url": None},
                    {"type": "facebook", "url": "https://example.be"},
                ]
            }
        )
        rows = cp.displayed_rows("urls")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["data"]["url"], "https://example.be")

    def test_displayed_rows_tolerates_missing_remote_payload(self):
        cp = self._make_contact_properties({"phones": None})
        self.assertEqual(cp.displayed_rows("phones"), [])

    def test_translated_type_delegates_to_the_label_table(self):
        cp = self._make_contact_properties()
        self.assertEqual(cp.translated_type("phones", "cell"), "Mobile")
        self.assertEqual(cp.translated_type("phones", "pager"), "pager")


class TestContactInformationsUtils(ImioSmartwebTestCase):
    """Module-level helpers of contents/sections/contact/utils.py"""

    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.contacts = get_json(
            "resources/json_contact_informations_raw_mock.json"
        ).get("items")

    def test_row_key_is_the_payload_value(self):
        self.assertEqual(row_key("phones", {"number": " +3287123456 "}), "+3287123456")
        self.assertEqual(
            row_key("mails", {"mail_address": "info@example.be"}),
            "info@example.be",
        )
        self.assertEqual(
            row_key("urls", {"url": "https://example.be"}), "https://example.be"
        )

    def test_row_key_is_empty_when_the_payload_is_missing(self):
        self.assertEqual(row_key("urls", {"type": "facebook", "url": None}), "")

    def test_translated_type_label_uses_the_directory_msgids(self):
        self.assertEqual(translated_type_label("phones", "cell"), "Mobile")
        self.assertEqual(translated_type_label("mails", "work"), "Work email")
        self.assertEqual(translated_type_label("urls", "facebook"), "Facebook")

    def test_translated_type_label_falls_back_to_the_raw_token(self):
        # The directory owns these vocabularies; an added type must degrade
        # visibly rather than blow up.
        self.assertEqual(translated_type_label("phones", "pager"), "pager")
        self.assertEqual(translated_type_label("phones", None), "")

    def test_build_display_rows_flattens_every_contact(self):
        rows = build_display_rows("phones", self.contacts)
        self.assertEqual(len(rows), 3)
        self.assertEqual(
            [row["contact_title"] for row in rows],
            ["Administration communale", "Administration communale", "CPAS"],
        )
        self.assertEqual(
            [row["number"] for row in rows],
            ["+3287123456", "+32475010203", "+3287654321"],
        )

    def test_build_display_rows_translates_the_type_column(self):
        rows = build_display_rows("phones", self.contacts)
        self.assertEqual(rows[0]["type"], "Work phone")
        self.assertEqual(rows[1]["type"], "Mobile")

    def test_build_display_rows_defaults_to_every_column(self):
        rows = build_display_rows("phones", self.contacts)
        self.assertEqual(rows[0]["visible_columns"], ["label", "type", "number"])
        rows = build_display_rows("urls", self.contacts)
        self.assertEqual(rows[0]["visible_columns"], ["type", "url"])

    def test_build_display_rows_carries_preferences_over(self):
        uid = "2dc381f0fb584381b8e4a19c84f53b35"
        preferences = {(uid, "+3287123456"): ["number"]}
        rows = build_display_rows("phones", self.contacts, preferences)
        self.assertEqual(rows[0]["visible_columns"], ["number"])
        # Untouched rows keep the default.
        self.assertEqual(rows[1]["visible_columns"], ["label", "type", "number"])

    def test_build_display_rows_keeps_an_explicit_empty_preference(self):
        # An empty list means "explicitly hidden" and must NOT be replaced by
        # the all-columns default.
        uid = "2dc381f0fb584381b8e4a19c84f53b35"
        preferences = {(uid, "+3287123456"): []}
        rows = build_display_rows("phones", self.contacts, preferences)
        self.assertEqual(rows[0]["visible_columns"], [])

    def test_build_display_rows_defaults_are_not_shared(self):
        # Every row must own its list, otherwise editing one row's checkboxes
        # would silently edit the others.
        rows = build_display_rows("phones", self.contacts)
        rows[0]["visible_columns"].append("boom")
        self.assertEqual(rows[1]["visible_columns"], ["label", "type", "number"])

    def test_build_display_rows_skips_rows_without_a_key(self):
        contacts = [
            {
                "UID": "uid1",
                "title": "C1",
                "urls": [
                    {"type": None, "url": None},
                    {"type": "facebook", "url": "https://example.be"},
                ],
            }
        ]
        rows = build_display_rows("urls", contacts)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["url"], "https://example.be")

    def test_build_display_rows_tolerates_missing_payload(self):
        self.assertEqual(build_display_rows("phones", []), [])
        self.assertEqual(
            build_display_rows("phones", [{"UID": "uid1", "title": "C1"}]), []
        )
        self.assertEqual(
            build_display_rows(
                "phones", [{"UID": "uid1", "title": "C1", "phones": None}]
            ),
            [],
        )

    @requests_mock.Mocker()
    def test_get_remote_contacts_preserves_the_requested_order(self, m):
        uids = [
            "af7bd1f547034b24a2e0da16c0ba0358",
            "2dc381f0fb584381b8e4a19c84f53b35",
        ]
        url = "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
            "&UID=".join(uids)
        )
        m.get(
            url,
            text=json.dumps(
                get_json("resources/json_contact_informations_raw_mock.json")
            ),
        )
        contacts = get_remote_contacts(uids)
        self.assertEqual([contact["UID"] for contact in contacts], uids)

    @requests_mock.Mocker()
    def test_get_remote_contacts_returns_empty_on_failure(self, m):
        uids = ["2dc381f0fb584381b8e4a19c84f53b35"]
        url = "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(uids[0])
        m.get(url, status_code=404)
        self.assertEqual(get_remote_contacts(uids), [])
        self.assertEqual(get_remote_contacts([]), [])


def _column_subsets(columns):
    """Every subset of `columns`, from the empty set to the full set."""
    return itertools.chain.from_iterable(
        itertools.combinations(columns, size) for size in range(len(columns) + 1)
    )


class TestSectionContactColumnCombinations(ImioSmartwebTestCase):
    """Exhaustive render coverage for `visible_columns` on a contact row.

    Two column-combination bugs (the `urls` `type`/`url` coupling) already
    slipped through review because nobody enumerated the combinations. This
    class brute-forces every subset of every kind's columns and asserts
    exactly what the rendered markup contains -- and, just as importantly,
    what it must NOT contain, including inside attributes such as `title=`.

    A parse error in `macros.pt` is swallowed by the section render (it
    degrades instead of raising), so a test that only asserts absences would
    pass against a dead template. Every non-empty-subset case therefore
    carries at least one positive assertion that the row actually rendered,
    and every empty-subset case asserts on markup that only
    `contents/sections/contact/macros.pt` itself can emit -- an untouched
    sibling row, or the list that would have held the hidden row -- so a dead
    template cannot masquerade as a correctly hidden row. The section title is
    NOT usable for that: it comes from `contents/sections/macros.pt`'s
    `section_title` macro, a different template that would still render.
    """

    layer = IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING

    uid = "2dc381f0fb584381b8e4a19c84f53b35"

    def setUp(self):
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        payload = get_json("resources/json_contact_informations_raw_mock.json")
        # Contact 1 only: the fixture also carries a second contact (CPAS)
        # that this class's cases never reference.
        payload["items"] = [payload["items"][0]]
        self.payload = payload
        self._page_counter = itertools.count()

    def _new_section(self, display_field, display_row):
        """A fresh Page + SectionContact, isolated from any other case.

        The render cache is keyed off `IAnnotations` on the section object
        itself (see `SECTION_ITEMS_HASH_KEY` in `contents/sections/views.py`),
        so a brand-new section per case cannot be served a stale render from
        a previous subset -- no `sleep`/`clear_cache` dance is needed here.
        """
        page = api.content.create(
            container=self.portal,
            type="imio.smartweb.Page",
            id="page-{}".format(next(self._page_counter)),
        )
        section = api.content.create(
            container=page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        section.visible_blocks = ["contact_informations"]
        section.related_contacts = [self.uid]
        setattr(section, display_field, [display_row])
        return page

    def _render(self, page, m):
        url = "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
            self.uid
        )
        m.get(url, text=json.dumps(self.payload))
        return queryMultiAdapter((page, self.request), name="full_view")()

    @requests_mock.Mocker()
    def test_phones_column_combinations(self, m):
        # {"label": "Secretariat", "type": "work", "number": "+3287123456"}
        label = "Secretariat"
        translated_type = "Work phone"
        number = "+3287123456"
        columns = ("label", "type", "number")

        for subset in _column_subsets(columns):
            with self.subTest(kind="phones", subset=subset):
                page = self._new_section(
                    "phones_display",
                    {
                        "contact_uid": self.uid,
                        "number": number,
                        "visible_columns": list(subset),
                    },
                )
                rendered = self._render(page, m)

                if not subset:
                    # Every column hidden -> the row is not rendered at all.
                    # The second phone of the fixture ("Direction") carries no
                    # preference, so it still renders: proof that the phones
                    # loop of contact/macros.pt really ran.
                    self.assertIn("+32475010203", rendered)
                    self.assertNotIn(label, rendered)
                    self.assertNotIn(translated_type, rendered)
                    self.assertNotIn(number, rendered)
                    continue

                if "label" in subset:
                    self.assertIn(label, rendered)
                else:
                    self.assertNotIn(label, rendered)
                if "type" in subset:
                    self.assertIn(translated_type, rendered)
                else:
                    self.assertNotIn(translated_type, rendered)
                if "number" in subset:
                    self.assertIn(number, rendered)
                else:
                    self.assertNotIn(number, rendered)

    @requests_mock.Mocker()
    def test_mails_column_combinations(self, m):
        # {"label": "Accueil", "type": "work", "mail_address": "info@example.be"}
        label = "Accueil"
        translated_type = "Work email"
        mail_address = "info@example.be"
        columns = ("label", "type", "mail_address")

        for subset in _column_subsets(columns):
            with self.subTest(kind="mails", subset=subset):
                page = self._new_section(
                    "mails_display",
                    {
                        "contact_uid": self.uid,
                        "mail_address": mail_address,
                        "visible_columns": list(subset),
                    },
                )
                rendered = self._render(page, m)

                if not subset:
                    # The fixture holds a single mail row -- the hidden one --
                    # so there is no untouched mail to assert on. The <ul> that
                    # would have carried it is emitted by
                    # contact/macros.pt alone (the untouched phone rows keep it
                    # alive), which proves the template ran and simply left the
                    # mail row out.
                    self.assertIn("contact_informations_genral", rendered)
                    self.assertNotIn(label, rendered)
                    self.assertNotIn(translated_type, rendered)
                    self.assertNotIn(mail_address, rendered)
                    continue

                if "label" in subset:
                    self.assertIn(label, rendered)
                else:
                    self.assertNotIn(label, rendered)
                if "type" in subset:
                    self.assertIn(translated_type, rendered)
                else:
                    self.assertNotIn(translated_type, rendered)
                if "mail_address" in subset:
                    self.assertIn(mail_address, rendered)
                else:
                    self.assertNotIn(mail_address, rendered)

    @requests_mock.Mocker()
    def test_urls_column_combinations(self, m):
        # {"type": "facebook", "url": "https://facebook.com/example"}
        #
        # Unlike phones/mails, `type` and `url` are NOT two independent
        # pieces of text: `type` drives the icon, `url` drives the `<a
        # href>`, and the translated label ("Facebook") only ever appears as
        # the link's `title=` attribute, which is only built when BOTH
        # columns are visible. So: icon <=> 'type' in subset; href/link text
        # <=> 'url' in subset; translated label <=> both.
        target_url = "https://facebook.com/example"
        href = 'href="{}"'.format(target_url)
        icon = "bi-facebook"
        translated_type = "Facebook"
        columns = ("type", "url")

        for subset in _column_subsets(columns):
            with self.subTest(kind="urls", subset=subset):
                page = self._new_section(
                    "urls_display",
                    {
                        "contact_uid": self.uid,
                        "url": target_url,
                        "visible_columns": list(subset),
                    },
                )
                rendered = self._render(page, m)

                if not subset:
                    # The `website` row of the fixture carries no preference,
                    # so it still renders: proof that the urls loop of
                    # contact/macros.pt really ran.
                    self.assertIn('href="https://example.be"', rendered)
                    self.assertNotIn(href, rendered)
                    self.assertNotIn(target_url, rendered)
                    self.assertNotIn(icon, rendered)
                    self.assertNotIn(translated_type, rendered)
                    continue

                if "url" in subset:
                    self.assertIn(href, rendered)
                else:
                    self.assertNotIn(href, rendered)
                    self.assertNotIn(target_url, rendered)

                if "type" in subset:
                    self.assertIn(icon, rendered)
                else:
                    self.assertNotIn(icon, rendered)

                if set(subset) == {"type", "url"}:
                    self.assertIn(translated_type, rendered)
                else:
                    self.assertNotIn(translated_type, rendered)
