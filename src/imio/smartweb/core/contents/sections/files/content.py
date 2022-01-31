# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope import schema
from zope.interface import implementer


class ISectionFiles(ISection):
    """Marker interface and Dexterity Python Schema for SectionFiles"""

    nb_results_by_batch = schema.Choice(
        title=_("Number of items per batch"),
        required=True,
        default=3,
        values=[1, 3, 4],
    )


@implementer(ISectionFiles)
class SectionFiles(Section):
    """SectionText class"""

    manage_content = True
