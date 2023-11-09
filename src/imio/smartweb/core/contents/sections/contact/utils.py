# -*- coding: utf-8 -*-

from datetime import date, datetime
from datetime import timedelta
from decimal import Decimal
from imio.smartweb.common.utils import rich_description
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import hash_md5
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

import json


class ContactProperties:
    def __init__(self, json_dict, section):
        self.contact = json_dict
        self.context = section

    def __getattr__(self, name):
        return self.contact.get(name)

    @property
    def contact_type_class(self):
        contact_type = self.contact.get("type").get("token")
        return "contact-type-{}".format(contact_type)

    @property
    def description(self):
        description = rich_description(self.contact.get("description"))
        return description

    def logo(self):
        if self.contact.get("logo") is None:
            return ""
        modified_hash = hash_md5(self.contact["modified"])
        logo = f"{self.contact['@id']}/@@images/logo/preview?cache_key={modified_hash}"
        return logo

    def leadimage(self):
        if self.contact.get("image") is None:
            return ""
        modified_hash = hash_md5(self.contact["modified"])
        leadimage = f"{self.contact['@id']}/@@images/image/{self.context.orientation}_affiche?cache_key={modified_hash}"
        return leadimage

    def data_geojson(self):
        """Return the contact geolocation as GeoJSON string."""
        current_lang = api.portal.get_current_language()[:2]
        coordinates = self.contact.get("geolocation")
        longitude = coordinates.get("longitude")
        latitude = coordinates.get("latitude")
        link_text = translate(_("Itinerary"), target_language=current_lang)
        geo_json = {
            "type": "Feature",
            "properties": {
                "popup": '<a href="{}">{}</a>'.format(
                    self.get_itinerary_link(), link_text
                ),
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    longitude,
                    latitude,
                ],
            },
        }
        return json.dumps(geo_json)

    def images(self, image_scale, nb_results_by_batch):
        contact_url = self.contact["@id"]
        query = "@search?portal_type=Image&path.depth=1&metadata_fields=modified"
        images_url_request = "{}/{}".format(contact_url, query)
        json_images = get_json(images_url_request)
        if json_images is None or len(json_images.get("items", [])) == 0:
            return
        results = []
        thumb_scale = image_scale
        for image in json_images.get("items"):
            base_url = image["@id"]
            modified_hash = hash_md5(image["modified"])
            large_url = f"{base_url}/@@images/image/?cache_key={modified_hash}"
            url = f"{base_url}/@@images/image/paysage_{thumb_scale}?cache_key={modified_hash}"
            dict_item = {
                "title": image["title"],
                "description": image["description"],
                "image_large_url": large_url,
                "image_url": url,
            }
            results.append(dict_item)
        return batch_results(results, nb_results_by_batch)

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

    def get_itinerary_link(self):
        address_parts = [
            self.contact.get("street"),
            self.contact.get("number") and str(self.contact.get("number")) or "",
            self.contact.get("complement"),
            self.contact.get("zipcode") and str(self.contact.get("zipcode")) or "",
            self.contact.get("city"),
        ]
        if self.contact.get("country"):
            address_parts.append(self.contact.get("country").get("title"))
        address = "+".join(filter(None, address_parts))
        if not address:
            return
        return "https://www.google.com/maps/dir/?api=1&destination={}".format(address)

    def get_translated_url_type(self, url_type_id):
        current_lang = api.portal.get_current_language()[:2]
        url_type_label = url_type_id[0].upper() + url_type_id[1:]
        return translate(_(url_type_label), target_language=current_lang)

    def get_opening_informations(self, a_date=None):
        current_date = a_date or date.today()
        schedule = self.contact.get("schedule")
        multi_schedule = self.contact.get("multi_schedule")
        exceptional_closure = self.contact.get("exceptional_closure")
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
                    week_day = week_day  # Fix coverage issue with continue.
                    continue
                day_schedule = schedule_info.get("schedule")[week_day]

        for exceptional_closure_info in exceptional_closure:
            exceptional_closure_date = datetime.strptime(
                exceptional_closure_info.get("date"), "%Y-%m-%d"
            ).date()
            if not current_date == exceptional_closure_date:
                continue
            for k, v in day_schedule.items():
                day_schedule[k] = ""
                if k == "comment":
                    day_schedule[k] = exceptional_closure_info.get("title")
        # sample : {'afternoonend': '16:00', 'afternoonstart': '14:00', 'comment': '', 'morningend': '14:00', 'morningstart': '09:00'}
        return day_schedule

    def get_week_days(self):
        """Returns a list of Messages for the weekday names."""
        PLMF = MessageFactory("plonelocales")
        ts = api.portal.get_tool("translation_service")
        weekdays = []
        now = date.today()
        for i in range(0, 7):
            ref_date = now + timedelta(days=i)
            # weekday 0 == monday in python
            # ts.day_msgid 0 = sunday in plone
            ref_date_tsweekday = (ref_date.weekday() + 1) % 7
            weekdays.append(
                {
                    PLMF(
                        ts.day_msgid(ref_date_tsweekday, format="s"),
                        default=ts.weekday_english(ref_date_tsweekday, format="a"),
                    ): self.get_schedule_for_date(ref_date)
                }
            )
        return weekdays

    def get_schedule_for_date(self, a_date):
        return self.get_opening_informations(a_date)

    def get_schedule_for_today(self, schedule):
        return get_schedule_for_today(schedule)

    def formatted_schedule(self, schedule):
        return formatted_schedule(schedule)

    def is_empty_schedule(self):
        schedule = self.contact.get("schedule") or {}
        for day in schedule.values():
            for value in day.values():
                if value:
                    return False
        return True

    def formatted_address(self):
        street_parts = [
            self.contact.get("street"),
            self.contact.get("number") and str(self.contact.get("number")) or "",
            self.contact.get("complement"),
        ]
        street = " ".join(filter(None, street_parts))
        entity_parts = [
            self.contact.get("zipcode") and str(self.contact.get("zipcode")) or "",
            self.contact.get("city"),
        ]
        entity = " ".join(filter(None, entity_parts))
        country = (
            self.contact.get("country")
            and self.contact.get("country").get("title")
            or ""
        )
        if not (street or entity or country):
            return None
        return {"street": street, "entity": entity, "country": country}


def formatted_schedule(schedule):
    # opening = {'afternoonend': '', 'afternoonstart': '', 'comment': '', 'morningend': '12:00', 'morningstart': '08:30'}
    current_lang = api.portal.get_current_language()[:2]
    morningstart = schedule.get("morningstart")
    morningend = schedule.get("morningend")
    afternoonstart = schedule.get("afternoonstart")
    afternoonend = schedule.get("afternoonend")
    comment = schedule.get("comment")
    str_opening = ""
    morning = False
    if morningend:
        morning = True
        str_opening = "{} - {}".format(morningstart, morningend)
    if morning is True and afternoonstart:
        str_opening += " | {} - {}".format(afternoonstart, afternoonend)
    elif morning is False and afternoonstart:
        str_opening = "{} - {}".format(afternoonstart, afternoonend)
    elif not morningend and not afternoonstart:
        str_opening = "{} - {}".format(morningstart, afternoonend)
    if not morningstart and not morningend and not afternoonstart and not afternoonend:
        str_opening = translate(_("Closed"), target_language=current_lang)
    return "{} ({})".format(str_opening, comment) if comment else str_opening


# {'afternoonend': '', 'afternoonstart': '', 'comment': 'vendredi : apéro à midi', 'morningend': '11:00', 'morningstart': '08:30'}
def get_schedule_for_today(schedule):
    current_lang = api.portal.get_current_language()[:2]
    message = translate(_("Open"), target_language=current_lang)
    comment = schedule.get("comment") or ""
    morningstart = Decimal(schedule.get("morningstart").replace(":", ".") or "0.00")
    morningend = Decimal(schedule.get("morningend").replace(":", ".") or "0.00")
    afternoonstart = Decimal(schedule.get("afternoonstart").replace(":", ".") or "0.00")
    afternoonend = Decimal(schedule.get("afternoonend").replace(":", ".") or "0.00")

    now_str = Decimal(datetime.now().strftime("%H.%M"))
    if not morningstart and not morningend and not afternoonstart and not afternoonend:
        translated_closed = translate(_("Closed"), target_language=current_lang)
        return (
            "{} ({})".format(translated_closed, comment)
            if comment
            else translated_closed
        )
    before_opened = now_str < (morningstart or afternoonstart)
    if before_opened:
        translated_open_at = translate(_("Open at "), target_language=current_lang)
        hour, minute = str(morningstart or afternoonstart).split(".")
        message = "{} {:02d}:{:02d}".format(translated_open_at, int(hour), int(minute))

    lunch_time = is_now_between(now_str, morningend, afternoonstart)
    if lunch_time:
        message = translate(_("Lunch time"), target_language=current_lang)

    after_closed = now_str >= (afternoonend or morningend)
    if after_closed:
        message = translate(_("Closed"), target_language=current_lang)
    return "{} ({})".format(message, comment) if comment else message


def is_now_between(now, start, end):
    if not start or not end:
        return False
    return now >= start and now < end
