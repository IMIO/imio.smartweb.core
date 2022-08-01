# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from freezegun import freeze_time
from imio.smartweb.core.contents.sections.contact.view import formatted_schedule
from imio.smartweb.core.contents.sections.contact.view import get_schedule_for_today
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_FUNCTIONAL_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.tests.utils import clear_cache
from imio.smartweb.core.tests.utils import get_json
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.zope import Browser
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
        self.assertIsNone(contact_view.contact)
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contact = authentic_contact_uid
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        contact_images_url = "http://localhost:8080/Plone/{}/@search?portal_type=Image&path.depth=1".format(
            authentic_contact_uid
        )
        m.get(contact_search_url, exc=requests.exceptions.ConnectTimeout)
        clear_cache(self.request)
        self.assertIsNone(contact_view.contact)
        m.get(contact_search_url, status_code=404)
        clear_cache(self.request)
        self.assertIsNone(contact_view.contact)
        m.get(contact_search_url, text=json.dumps(self.json_no_contact))
        clear_cache(self.request)
        self.assertIsNone(contact_view.contact)
        self.assertEqual(contact_view.contact_type_class, "")
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        self.assertIsNotNone(contact_view.contact)
        self.assertEqual(contact_view.contact_type_class, "contact-type-organization")
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
        clear_cache(self.request)
        self.assertIn("contact_gallery", view())
        self.assertEqual(len(contact_view.images[0]), 2)

        m.get(contact_search_url, exc=requests.exceptions.ConnectTimeout)
        clear_cache(self.request)
        self.assertIsNone(contact_view.images)
        m.get(contact_search_url, status_code=404)
        clear_cache(self.request)
        self.assertIsNone(contact_view.images)
        m.get(contact_search_url, text=json.dumps(self.json_no_contact))
        clear_cache(self.request)
        self.assertIsNone(contact_view.images)

        m.get(contact_search_url, text=json.dumps(self.json_contact))
        m.get(contact_images_url, text=json.dumps(self.json_no_image))
        clear_cache(self.request)
        self.assertIsNone(contact_view.images)
        m.get(contact_images_url, status_code=404)
        clear_cache(self.request)
        self.assertIsNone(contact_view.images)
        m.get(contact_images_url, exc=requests.exceptions.ConnectTimeout)
        clear_cache(self.request)
        self.assertIsNone(contact_view.images)

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
        self.assertIsNone(contact_view.get_opening_informations())
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contact = authentic_contact_uid
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        self.assertIsNotNone(contact_view.get_opening_informations())

        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow_str = (today + timedelta(days=1)).strftime("%Y-%m-%d")

        self.json_contact["items"][0]["exceptional_closure"] = [
            {"date": today_str, "title": "Exceptional closure !"}
        ]
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        self.assertIsNotNone(contact_view.get_opening_informations())

        today = datetime.now().strftime("%Y-%m-%d")
        self.json_contact["items"][0]["multi_schedule"][0]["dates"] = [
            {"end_date": tomorrow_str, "start_date": yesterday_str}
        ]
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        self.assertIsNotNone(contact_view.get_opening_informations())

        self.json_contact["items"][0]["multi_schedule"][0]["dates"] = [
            {"end_date": yesterday_str, "start_date": yesterday_str}
        ]
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        self.assertIsNotNone(contact_view.get_opening_informations())

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
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        self.assertIsNone(contact_view.get_opening_informations())
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contact = authentic_contact_uid
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        clear_cache(self.request)
        with freeze_time("2021-06-30 12:20:00"):
            schedule = contact_view.get_opening_informations()
            self.assertEqual(
                "13:00 - 17:30 (Ouverture PM)",
                contact_view.formatted_schedule(schedule),
            )
        with freeze_time("2021-07-07 12:20:00"):
            schedule = contact_view.get_opening_informations()
            self.assertEqual(
                "13:00 - 15:00 (Ouverture PM vacances)",
                contact_view.formatted_schedule(schedule),
            )
        with freeze_time("2021-09-01 12:20:00"):
            schedule = contact_view.get_opening_informations()
            self.assertEqual(
                "13:00 - 17:30 (Ouverture PM)",
                contact_view.formatted_schedule(schedule),
            )
        with freeze_time("2021-12-29 12:20:00"):
            schedule = contact_view.get_opening_informations()
            self.assertEqual(
                "13:00 - 15:00 (Ouverture PM vacances)",
                contact_view.formatted_schedule(schedule),
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
        contact_view = queryMultiAdapter((contact, self.request), name="view")
        self.assertIsNone(contact_view.get_opening_informations())
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contact = authentic_contact_uid
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        m.get(contact_search_url, text=json.dumps(json_contact_empty_schedule))
        clear_cache(self.request)
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        is_empty = contact_view.is_empty_schedule()
        self.assertEqual(is_empty, True)
        self.assertNotIn('class="schedule"', view())
        json_contact_empty_schedule["items"][0].get("schedule")["monday"] = {
            "morningstart": "8:00",
            "morningend": "12:00",
            "afternoonstart": "",
            "afternoonend": "",
            "comments": "",
        }
        m.get(contact_search_url, text=json.dumps(json_contact_empty_schedule))
        clear_cache(self.request)
        is_empty = contact_view.is_empty_schedule()
        self.assertEqual(is_empty, False)
        self.assertIn('class="schedule"', view())

    @requests_mock.Mocker()
    def test_leadimage_is_in_portrait_mode(self, m):
        contact = api.content.create(
            container=self.page,
            type="imio.smartweb.SectionContact",
            title="My contact",
        )
        view = queryMultiAdapter((self.page, self.request), name="full_view")
        authentic_contact_uid = "2dc381f0fb584381b8e4a19c84f53b35"
        contact.related_contact = authentic_contact_uid
        contact_search_url = (
            "http://localhost:8080/Plone/@search?UID={}&fullobjects=1".format(
                authentic_contact_uid
            )
        )
        contact.visible_blocks = ["titles", "leadimage"]
        m.get(contact_search_url, text=json.dumps(self.json_contact))
        self.assertNotIn("contact_leadimage portrait", view())
        contact.is_in_portrait_mode = True
        self.assertIn("contact_leadimage portrait", view())
