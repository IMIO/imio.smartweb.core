# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.vocabularies.catalog import CatalogSource
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class ISectionSelections(ISection):
    """Marker interface and Dexterity Python Schema for SectionSelections"""

    selected_items = RelationList(
        title=_(u"Selected items"),
        value_type=RelationChoice(
            title=u"",
            source=CatalogSource(),
        ),
        required=True,
    )

    nb_results_by_batch = schema.Choice(
        title=_(u"Number of items per batch"),
        required=True,
        default=3,
        values=[1, 3, 4],
    )

    model.fieldset("layout", fields=["show_items_lead_image", "show_items_description"])
    show_items_lead_image = schema.Bool(
        title=_(u"Show items lead image"), required=False
    )

    show_items_description = schema.Bool(
        title=_(u"Show items description"), required=False
    )


@implementer(ISectionSelections)
class SectionSelections(Section):
    """SectionSelections class"""

    manage_content = False
    manage_display = True
