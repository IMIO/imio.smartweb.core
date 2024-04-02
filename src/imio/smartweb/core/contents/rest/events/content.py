# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import RestView
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer


class IEventsView(model.Schema):
    """Marker interface and Dexterity Python Schema for EventsView"""

    directives.widget(selected_event_types=CheckBoxFieldWidget)
    selected_event_types = schema.List(
        title=_("Selected event types"),
        value_type=schema.Choice(vocabulary="imio.smartweb.vocabulary.EventsTypes"),
        required=True,
    )

    selected_agenda = schema.Choice(
        title=_("Selected agenda"),
        description=_("Select agenda to display"),
        vocabulary="imio.smartweb.vocabulary.RemoteAgendas",
        required=True,
    )

    nb_results = schema.Int(
        title=_("Number of items to display"), default=20, required=True
    )

    display_map = schema.Bool(
        title=_("Display map"),
        description=_("If selected, map will be displayed"),
        required=False,
        default=True,
    )

    display_agendas_titles = schema.Bool(
        title=_("Display agendas titles"),
        description=_("If checked, display agendas titles"),
        required=False,
    )

    only_past_events = schema.Bool(
        title=_("Display only past events"),
        description=_("If selected, only past events will be displayed"),
        required=False,
        default=False,
    )


@implementer(IEventsView)
class EventsView(RestView):
    """EventsView class"""
