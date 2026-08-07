# -*- coding: utf-8 -*-

from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.core.contents.sections.external_content.illiwap import (
    is_illiwap_agenda_url,
)
from imio.smartweb.core.contents.sections.external_content.illiwap import (
    is_illiwap_rss_url,
)
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope.interface import implementer
from zope import schema

import json


class ISectionExternalContent(ISection):
    """Marker interface and Dexterity Python Schema for SectionVideo"""

    description = schema.Text(
        title=_("Description"),
        description=_(
            "Use **text** to set text in bold. Limited to ${max} characters.",
            mapping={"max": DESCRIPTION_MAX_LENGTH},
        ),
        max_length=DESCRIPTION_MAX_LENGTH,
        required=False,
    )

    external_content_url = schema.URI(
        title=_("External content url"),
        required=True,
    )

    external_content_params = schema.Text(
        title=_("External content parameters"),
        required=False,
    )


@implementer(ISectionExternalContent)
class SectionExternalContent(Section):
    """SectionVideo class"""

    show_items_date = True

    @property
    def manage_display(self):
        """Only an Illiwap news feed or agenda has a table / carousel display
        to choose from
        """
        url = getattr(self, "external_content_url", None)
        return is_illiwap_rss_url(url) or is_illiwap_agenda_url(url)

    @property
    def params(self):
        """external_content_params holds a json dictionary, as it already does
        for the elloha, cognitoform and arcgis plugins.
        """
        try:
            params = json.loads(self.external_content_params or "{}")
        except ValueError:
            return {}
        return params if isinstance(params, dict) else {}

    def _int_param(self, name, default, minimum, maximum):
        try:
            value = int(self.params.get(name, default))
        except (TypeError, ValueError):
            return default
        return max(minimum, min(maximum, value))

    @property
    def nb_results_by_batch(self):
        return self._int_param("nb_results_by_batch", 3, 1, 4)

    @property
    def max_nb_batches(self):
        return self._int_param("max_nb_batches", 3, 1, 12)

    @property
    def show_items_description(self):
        return bool(self.params.get("show_items_description", False))

    @property
    def link_text(self):
        """Label of the link to the illiwap agenda. Empty means no link, which
        is what the templates expect.
        """
        return self.params.get("link_text", "")
