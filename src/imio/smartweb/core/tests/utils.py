# -*- coding: utf-8 -*-
import json
import os


def get_sections_types():
    return [
        "imio.smartweb.SectionContact",
        "imio.smartweb.SectionFiles",
        "imio.smartweb.SectionGallery",
        "imio.smartweb.SectionLinks",
        "imio.smartweb.SectionSelections",
        "imio.smartweb.SectionText",
        "imio.smartweb.SectionVideo",
    ]


def get_json(json_filename):
    with open(
        os.path.join(
            os.path.dirname(__file__),
            json_filename,
        ),
    ) as json_file:
        json_procedures_raw_mock = json.load(json_file)
        return json_procedures_raw_mock


def get_leadimage_filename():
    leadimage = os.path.join(
        os.path.dirname(__file__),
        "resources/plone.png",
    )
    return leadimage
