# -*- coding: utf-8 -*-

from datetime import date, datetime
from datetime import timedelta
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import get_json
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory

import json


class EventsView(SectionView):
    """Events Section view"""

    @property
    def Events(self):
        params = [
            "selected_events_folders={}".format(self.context.related_events),
            "portal_type=imio.events.EventsItem",
            "metadata_fields=category",
            "metadata_fields=effective",
        ]
        url = "{}/@search?{}".format(EVENTS_URL, "&".join(params))
        json_search_events = get_json(url)
        if (
            json_search_events is None
            or len(json_search_events.get("items", [])) == 0  # NOQA
        ):
            return

        # [{'@id': 'https://events.staging.imio.be/braine-lalleud/2021/actu2',
        #   '@type': 'imio.events.EventsItem',
        #   'category': None,
        #   'description': 'Nouvelle actu 2',
        #   'review_state': 'published',
        #   'title': 'Actu2'},
        #  {
        #      '@id': 'https://events.staging.imio.be/braine-lalleud/2021/inauguration-du-nouveau-site-de-la-commune-de-braine-lalleud',
        #      '@type': 'imio.events.EventsItem',
        #      'category': 'presse',
        #      'description': '',
        #      'review_state': 'published',
        #      'title': "Inauguration du nouveau site de la commune de Braine l'Alleud"}]
        return json_search_events.get("items")

    def lead_image(self, events):
        if events is None:
            return
        events_url = events["@id"]
        return "{}/{}".format(events_url,"@@images/image/")
