# -*- coding: utf-8 -*-

from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from plone.memoize import ram
from zope.annotation.interfaces import IAnnotations

import json
import os

# "imio.smartweb.SectionContact",
# "imio.smartweb.SectionEvents",
# "imio.smartweb.SectionNews",
# "imio.smartweb.SectionSlide",


def get_sections_types(kw="type"):
    sections = [
        {
            "type": "imio.smartweb.SectionFiles",
            "empty_section": True,
        },
        {
            "type": "imio.smartweb.SectionGallery",
            "empty_section": True,
        },
        {
            "type": "imio.smartweb.SectionHTML",
            "empty_section": True,
        },
        {
            "type": "imio.smartweb.SectionLinks",
            "empty_section": True,
        },
        {
            "type": "imio.smartweb.SectionMap",
            "empty_section": True,
        },
        {
            "type": "imio.smartweb.SectionPostit",
            "empty_section": True,
        },
        {
            "type": "imio.smartweb.SectionSelections",
            "empty_section": True,
        },
        {
            "type": "imio.smartweb.SectionText",
            "empty_section": True,
        },
        {
            "type": "imio.smartweb.SectionVideo",
            "empty_section": True,
        },
    ]
    if kw == "empty_section":
        return [
            section.get("type")
            for section in sections
            if section.get("empty_section") is True
        ]
    else:
        return [section.get("type") for section in sections]


def get_json(json_filename):
    with open(
        os.path.join(
            os.path.dirname(__file__),
            json_filename,
        ),
    ) as json_file:
        json_procedures_raw_mock = json.load(json_file)
        return json_procedures_raw_mock


def get_html(html_filename):
    with open(
        os.path.join(
            os.path.dirname(__file__),
            html_filename,
        ),
    ) as html_file:
        html_raw_mock = html_file.read()
        return html_raw_mock


def clear_cache(request):
    annotations = IAnnotations(request)
    del annotations["plone.memoize"]


def clear_ram_cache():
    """Drop everything memoized with ``@ram.cache``.

    ``clear_cache()`` only drops the per-request annotation, while the remote
    vocabularies are cached in the *global* RAM cache for a minute. That cache
    otherwise leaks between tests: one test's mocked answer gets served to the
    next, and which one wins depends on the run order.
    """
    ram.global_cache.invalidateAll()


def make_named_image(filename="plone.png"):
    path = os.path.join(os.path.dirname(__file__), f"resources/{filename}")
    with open(path, "rb") as f:
        image_data = f.read()
    return {"filename": filename, "data": image_data}


def mock_agenda_scope(m, agenda_uid, title="Agenda global", populating=()):
    """Mock the two requests get_agenda_scope() makes for one agenda.

    ``populating`` is an iterable of ``(uid, title)`` for the agendas feeding
    this one.
    """
    agenda_url = f"http://localhost:8080/Plone/agendas/{agenda_uid}"
    m.get(
        f"{EVENTS_URL}/@search?UID={agenda_uid}&metadata_fields=UID",
        text=json.dumps({"items": [{"@id": agenda_url, "UID": agenda_uid}]}),
    )
    m.get(
        agenda_url,
        text=json.dumps(
            {
                "UID": agenda_uid,
                "title": title,
                "populating_agendas": [
                    {"UID": uid, "title": populating_title}
                    for uid, populating_title in populating
                ],
            }
        ),
    )


def mock_newsfolder_scope(m, newsfolder_uid, title="Dossier global", populating=()):
    """Mock the two requests get_newsfolder_scope() makes for one folder.

    ``populating`` is an iterable of ``(uid, title)`` for the folders feeding
    this one.
    """
    folder_url = f"http://localhost:8080/Plone/newsfolders/{newsfolder_uid}"
    m.get(
        f"{NEWS_URL}/@search?UID={newsfolder_uid}&metadata_fields=UID",
        text=json.dumps({"items": [{"@id": folder_url, "UID": newsfolder_uid}]}),
    )
    m.get(
        folder_url,
        text=json.dumps(
            {
                "UID": newsfolder_uid,
                "title": title,
                "populating_newsfolders": [
                    {"UID": uid, "title": populating_title}
                    for uid, populating_title in populating
                ],
            }
        ),
    )


class FakeResponse:
    status_code = 404
    headers = {}
    text = "{}"

    def __init__(self, status_code=None, headers=None):
        if status_code:
            self.status_code = status_code
        if headers:
            self.headers = headers

    def json(self):
        return json.loads(self.text)


def mock_entity_agendas(m):
    """Mock the two requests RemoteAgendasVocabulary makes for the entity.

    What ``EventsFromEntityVocabulary`` needs before it can query the events
    themselves -- it is entity-wide, not scoped to a linking view.
    """
    m.get(
        f"{EVENTS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee31",
        text=json.dumps(get_json("resources/json_events_entities_raw_mock.json")),
    )
    m.get(
        f"{EVENTS_URL}/imio-events-entity/@search?portal_type=imio.events.Agenda"
        "&sort_on=sortable_title&b_size=1000000&metadata_fields=UID",
        text=json.dumps(get_json("resources/json_events_agendas_raw_mock.json")),
    )


def mock_entity_newsfolders(m):
    """Mock the two requests RemoteNewsFoldersVocabulary makes for the entity.

    The news mirror of ``mock_entity_agendas()``.
    """
    m.get(
        f"{NEWS_URL}/@search?UID=7c69f9a738ec497c819725c55888ee32",
        text=json.dumps(get_json("resources/json_news_entities_raw_mock.json")),
    )
    m.get(
        f"{NEWS_URL}/imio-news-entity/@search?portal_type=imio.news.NewsFolder"
        "&sort_on=sortable_title&b_size=1000000&metadata_fields=UID",
        text=json.dumps(get_json("resources/json_news_newsfolder_raw_mock.json")),
    )
