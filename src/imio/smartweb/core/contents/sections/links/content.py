# -*- coding: utf-8 -*-

from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope.interface import implementer
from zope import schema


class ISectionLinks(ISection):
    """Marker interface and Dexterity Python Schema for SectionLinks"""

    description = schema.Text(
        title=_("Description"),
        description=_(
            "Use **text** to set text in bold. Limited to ${max} characters.",
            mapping={"max": DESCRIPTION_MAX_LENGTH},
        ),
        max_length=DESCRIPTION_MAX_LENGTH,
        required=False,
    )

    nb_results_by_batch = schema.Choice(
        title=_("Number of items per batch"),
        required=True,
        default=3,
        values=range(1, 9),
    )


@implementer(ISectionLinks)
class SectionLinks(Section):
    """SectionLinks class"""

    manage_content = True
    manage_display = True
