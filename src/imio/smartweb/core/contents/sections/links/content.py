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
        title=_(u"Description"),
        description=_(
            u"Use **text** to set text in bold. Limited to ${max} characters.",
            mapping={u"max": DESCRIPTION_MAX_LENGTH},
        ),
        max_length=DESCRIPTION_MAX_LENGTH,
        required=False,
    )

    nb_results_by_batch = schema.Choice(
        title=_(u"Number of items per batch"),
        required=True,
        default=3,
        values=[1, 3, 4],
    )


@implementer(ISectionLinks)
class SectionLinks(Section):
    """SectionLinks class"""

    manage_content = True
    manage_display = True
