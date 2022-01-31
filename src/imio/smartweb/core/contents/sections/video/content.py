# -*- coding: utf-8 -*-

from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope.interface import implementer
from zope import schema


class ISectionVideo(ISection):
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

    video_url = schema.URI(
        title=_("Video url"),
        description=_("Video url from youtube, vimeo"),
        required=True,
    )


@implementer(ISectionVideo)
class SectionVideo(Section):
    """SectionVideo class"""
