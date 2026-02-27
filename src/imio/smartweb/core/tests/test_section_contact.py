# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from freezegun import freeze_time
from imio.smartweb.common.contact_utils import formatted_schedule
from imio.smartweb.common.contact_utils import get_schedule_for_today
from imio.smartweb.core.contents.sections.contact.utils import ContactProperties
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

import json
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
        self.assertIn("contact_informations", view())
        self.assertIn("schedule", view())
        self.assertNotIn("contact_gallery", view())
        contact.visible_blocks = ["titles", "gallery"]
        self.assertIn("contact_titles", view())
        self.assertNotIn("contact_address", view())
        self.assertNotIn("contact_informations", view())
        self.assertNotIn("schedule", view())
        contact.visible_blocks = ["contact_informations", "address", "schedule"]
        self.assertEqual(view().count("<h2"), 4)
        contact.visible_blocks = [
            "titles",
            "contact_informations",
            "address",
            "map",
            "schedule",
        ]
        self.assertIn('class="pat-leaflet map"', view())
        self.assertEqual(view().count("<h2"), 2)
        self.assertEqual(view().count("<h3"), 3)

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
