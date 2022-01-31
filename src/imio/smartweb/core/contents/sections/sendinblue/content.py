# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope import schema
from zope.interface import implementer


class ISectionSendinblue(ISection):
    """Marker interface and Dexterity Python Schema for SectionSendinblue"""

    newsletter_list = schema.Choice(
        title=_("List"),
        description=_("Select list to enable subscriptions to"),
        required=True,
        vocabulary="collective.sendinblue.vocabularies.AvailableLists",
    )


@implementer(ISectionSendinblue)
class SectionSendinblue(Section):
    """SectionSendinblue class"""
