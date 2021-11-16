# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def see_all_default(context):
    return translate(_(u"See all events"), context=getRequest())


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

    nb_results_by_batch = schema.Choice(
        title=_(u"Number of items per batch"),
        required=True,
        default=3,
        values=[1, 3, 4],
    )

    max_nb_batches = schema.Int(
        title=_(u"Maximum number of batches to display"),
        required=True,
        default=2,
        min=1,
        max=12,
    )

    link_text = schema.TextLine(
        title=_(u"Text for the link to the events view"),
        defaultFactory=see_all_default,
        required=True,
    )


@implementer(ISectionEvents)
class SectionEvents(Section):
    """SectionEvents class"""

    manage_display = True
