# -*- coding: utf-8 -*-

from zope.annotation.interfaces import IAnnotations

import json
import os


# "imio.smartweb.SectionContact",
# "imio.smartweb.SectionEvents",
# "imio.smartweb.SectionNews",
# "imio.smartweb.SectionSendinblue",
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


def make_named_image(filename="plone.png"):
    path = os.path.join(os.path.dirname(__file__), f"resources/{filename}")
    with open(path, "rb") as f:
        image_data = f.read()
    return {"filename": filename, "data": image_data}
