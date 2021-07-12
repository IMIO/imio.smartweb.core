# -*- coding: utf-8 -*-

from datetime import date, datetime
from datetime import timedelta
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_directory_json
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.i18nmessageid import MessageFactory


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

    def get_opening_informations(self, a_date=None):
        current_date = a_date or date.today()
        contact = self.contact
        if contact is None:
            return
        schedule = contact.get("schedule")
        multi_schedule = contact.get("multi_schedule")
        exceptional_closure = contact.get("exceptional_closure")

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

        return day_schedule

    def get_week_days(self):
        """Returns a list of Messages for the weekday names."""
        PLMF = MessageFactory("plonelocales")
        ts = api.portal.get_tool("translation_service")
        weekdays = []
        now = date.today()
        weekday = now.weekday() + 1
        # list of ordered weekdays as numbers
        for day in range(weekday, weekday + 7):
            weekdays.append(
                {
                    PLMF(
                        ts.day_msgid(day % 7, format="s"),
                        default=ts.weekday_english(day % 7, format="a"),
                    ): self.get_schedule_for_date(now + timedelta(days=(day - 1) % 7))
                }
            )
        return weekdays

    def get_schedule_for_date(self, a_date):
        return self.get_opening_informations(a_date)

    def get_schedule_for_today(self, schedule):
        return get_schedule_for_today(schedule)

    def formatted_schedule(self, schedule):
        return formatted_schedule(schedule)


def formatted_schedule(schedule):
    # opening = {'afternoonend': '', 'afternoonstart': '', 'comment': '', 'morningend': '12:00', 'morningstart': '08:30'}
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
        str_opening = _("Closed")
    return "{} ({})".format(str_opening, comment) if comment else str_opening


# {'afternoonend': '', 'afternoonstart': '', 'comment': 'vendredi : apéro à midi', 'morningend': '11:00', 'morningstart': '08:30'}
def get_schedule_for_today(schedule):
    message = _("Open")
    morningstart = schedule.get("morningstart")
    morningend = schedule.get("morningend")
    afternoonstart = schedule.get("afternoonstart")
    afternoonend = schedule.get("afternoonend")
    comment = schedule.get("comment")
    if morningstart:
        morningstart = float(schedule.get("morningstart").replace(":", "."))
    if morningend:
        morningend = float(schedule.get("morningend").replace(":", "."))
    if afternoonstart:
        afternoonstart = float(schedule.get("afternoonstart").replace(":", "."))
    if afternoonend:
        afternoonend = float(schedule.get("afternoonend").replace(":", "."))

    now_str = float(datetime.now().strftime("%H.%M"))
    if not morningstart and not morningend and not afternoonstart and not afternoonend:
        return "{} ({})".format(_("Closed"), comment) if comment else _("Closed")

    before_opened = now_str < (morningstart or afternoonstart)
    if before_opened:
        message = _("Open at ") + str(morningstart or afternoonstart)

    lunch_time = is_now_between(now_str, morningend, afternoonstart)
    if lunch_time:
        message = _("Lunch time")

    after_closed = now_str >= (afternoonend or morningend)
    if after_closed:
        message = _("Closed")
    return "{} ({})".format(message, comment) if comment else message


def is_now_between(now, start, end):
    if not start or not end:
        return False
    return now >= start and now < end
