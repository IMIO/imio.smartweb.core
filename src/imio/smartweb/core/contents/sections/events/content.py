# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.interface import implementer


class ISectionEvents(ISection):
    """Marker interface and Dexterity Python Schema for SectionEvents"""

    directives.widget(related_events=SelectFieldWidget)
    related_events = schema.Choice(
        title=_(u"Related agenda"),
        source="imio.smartweb.vocabulary.RemoteAgendas",
        required=True,
    )

    directives.widget(
        "linking_rest_view",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["imio.smartweb.EventsView"],
            "favorites": [],
        },
    )
    linking_rest_view = RelationChoice(
        title=_(u"Events view used to display events details"),
        source=CatalogSource(),
        required=True,
    )

    max_nb_results = schema.Int(
        title=_(u"Maximum number of items to display"), default=9, required=True
    )

    nb_results_by_batch = schema.Int(
        title=_(u"Number of items per batch"), default=3, required=True
    )

    model.fieldset("layout", fields=["image_scale"])
    image_scale = schema.Choice(
        title=_(u"Image scale for news"),
        default=u"tile",
        vocabulary="plone.app.vocabularies.ImagesScales",
        required=True,
    )


@implementer(ISectionEvents)
class SectionEvents(Section):
    """SectionEvents class"""
