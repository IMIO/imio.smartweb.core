# -*- coding: utf-8 -*-

from plone.memoize.ram import global_cache
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.ramcache.interfaces.ram import IRAMCache

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
        encoding="utf-8",
    ) as html_file:
        html_raw_mock = html_file.read()
        return html_raw_mock


def clear_cache(request):
    annotations = IAnnotations(request)
    del annotations["plone.memoize"]


def clear_ram_cache(*functions):
    """Drop the @ram.cache entries of the given functions.

    @ram.cache storage lives across requests, so a value cached by one test
    method is still there for the next one. plone.memoize.ram keys it on
    "<module>.<name>" and uses the IRAMCache utility when one is registered,
    its own module level cache otherwise : clear both.

    Targeted on purpose : invalidating the whole cache reaches unrelated
    tests that depend on their own cached values.
    """
    caches = [c for c in (queryUtility(IRAMCache), global_cache) if c is not None]
    for function in functions:
        key = f"{function.__module__}.{function.__name__}"
        for cache in caches:
            cache.invalidate(key)


def make_named_image(filename="plone.png"):
    path = os.path.join(os.path.dirname(__file__), f"resources/{filename}")
    with open(path, "rb") as f:
        image_data = f.read()
    return {"filename": filename, "data": image_data}


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
