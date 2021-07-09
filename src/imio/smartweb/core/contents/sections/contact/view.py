# -*- coding: utf-8 -*-

from datetime import date, datetime
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_directory_json
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api


class ContactView(SectionView):
    """Contact Section view"""

    @property
    def contact(self):
        smartweb_directory_url = api.portal.get_registry_record("imio.directory.url")
        url = "{}/@search?UID={}&fullobjects=1".format(
            smartweb_directory_url, self.context.related_contact
        )
        json_search_contact = get_directory_json(url)
        if (
            json_search_contact is None
            or len(json_search_contact.get("items", [])) == 0  # NOQA
        ):
            return
        return json_search_contact.get("items")[0]

    @property
    def images(self):
        contact = self.contact
        if contact is None:
            return
        contact_url = contact["@id"]
        query = "@search?portal_type=Image&path.depth=1"
        images_url_request = "{}/{}".format(contact_url, query)
        json_images = get_directory_json(images_url_request)
        if json_images is None or len(json_images.get("items", [])) == 0:
            return
        return json_images.get("items")

    @property
    def days(self):
        return (
            ("monday", _("Monday")),
            ("tuesday", _("Tuesday")),
            ("wednesday", _("Wednesday")),
            ("thursday", _("Thursday")),
            ("friday", _("Friday")),
            ("saturday", _("Saturday")),
            ("sunday", _("Sunday")),
        )

    def get_opening_informations(self):
        contact = self.contact
        if contact is None:
            return
        schedule = contact.get("schedule")
        multi_schedule = contact.get("multi_schedule")
        exceptional_closure = contact.get("exceptional_closure")

        current_date = date.today()
        # current_hour = datetime.now()
        week_day = self.days[current_date.weekday()][0]
        day_schedule = schedule[week_day]
        for schedule_info in multi_schedule:
            if schedule_info.get("dates") == []:
                continue
            for daterange in schedule_info.get("dates"):
                min_date = datetime.strptime(
                    daterange.get("start_date"), "%Y-%m-%d"
                ).date()
                max_date = datetime.strptime(
                    daterange.get("end_date"), "%Y-%m-%d"
                ).date()
                if not (min_date < current_date < max_date):
                    continue
                day_schedule = schedule_info.get("schedule")[week_day]

        for exceptional_closure_info in exceptional_closure:
            exceptional_closure_date = datetime.strptime(
                exceptional_closure_info.get("date"), "%Y-%m-%d"
            ).date()
            if not current_date == exceptional_closure_date:
                continue
            for k, v in day_schedule.items():
                if k == "comment":
                    day_schedule[k] = exceptional_closure_info.get("title")
                day_schedule[k] = ""
        return day_schedule
