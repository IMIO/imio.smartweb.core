# -*- coding: utf-8 -*-

from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope.interface import implementer
from zope import schema


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
