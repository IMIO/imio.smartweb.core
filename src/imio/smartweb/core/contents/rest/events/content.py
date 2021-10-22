# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IEventsView(model.Schema):
    """Marker interface and Dexterity Python Schema for EventsView"""

    selected_agenda = schema.Choice(
        title=_(u"Selected agenda"),
        description=_(u"Select agenda to display"),
        vocabulary="imio.smartweb.vocabulary.RemoteAgendas",
        required=True,
    )

    nb_results = schema.Int(
        title=_(u"Number of items to display"), default=20, required=True
    )

    show_items_description = schema.Bool(
        title=_(u"Show items description"), default=True, required=False
    )


@implementer(IEventsView)
class EventsView(Container):
    """EventsView class"""
