# -*- coding: utf-8 -*-
import json
import os


def get_sections_types():
    return [
        "imio.smartweb.SectionContact",
        # "imio.smartweb.SectionEvents",
        "imio.smartweb.SectionFiles",
        "imio.smartweb.SectionGallery",
        "imio.smartweb.SectionHTML",
        "imio.smartweb.SectionLinks",
        "imio.smartweb.SectionMap",
        # "imio.smartweb.SectionNews",
        "imio.smartweb.SectionSelections",
        # "imio.smartweb.SectionSendinblue",
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


def make_named_image(filename="plone.png"):
    path = os.path.join(os.path.dirname(__file__), f"resources/{filename}")
    with open(path, "rb") as f:
        image_data = f.read()
    return {"filename": filename, "data": image_data}
