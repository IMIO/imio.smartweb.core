# -*- coding: utf-8 -*-

from imio.smartweb.common.widgets.select import TranslatedAjaxSelectWidget
from imio.smartweb.core.contents.rest.search.endpoint import (
    get_default_view_url,
)
from imio.smartweb.core.contents.sections.base import carries_fields
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.core.utils import get_agenda_scope_uids
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.z3cform.widgets.contentbrowser import ContentBrowserFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def see_all_default(context):
    return translate(_("See all events"), context=getRequest())


class ISectionEvents(ISection):
    """Marker interface and Dexterity Python Schema for SectionEvents"""

    directives.widget(
        "linking_rest_view",
        ContentBrowserFieldWidget,
        vocabulary="imio.smartweb.vocabulary.EventsViewsSite",
        pattern_options={
            "selectableTypes": ["imio.smartweb.EventsView"],
            "favorites": [],
        },
    )
    linking_rest_view = RelationChoice(
        title=_("Events view used to display events details"),
        description=_(
            'Only used when "All the events of an agenda" is selected below. '
            "A hand-picked selection links to the default events view of the "
            "control panel instead."
        ),
        vocabulary="imio.smartweb.vocabulary.EventsViewsSite",
        required=False,
    )

    directives.widget(events_source=RadioFieldWidget)
    events_source = schema.Choice(
        title=_("Events to display"),
        description=_(
            "Choose whether this section lists a whole agenda or only the events "
            "you pick yourself. Only the field matching your choice is used."
        ),
        source="imio.smartweb.vocabulary.SectionEventsSource",
        required=True,
        default="agenda",
    )

    directives.widget(related_events=SelectFieldWidget)
    related_events = schema.Choice(
        title=_("Related agenda"),
        description=_(
            'Used when "All the events of an agenda" is selected above. '
            "Limited to the agendas the linking view above can display."
        ),
        source="imio.smartweb.vocabulary.ScopedAgendas",
        required=False,
    )

    specific_related_events = schema.List(
        title=_("Specific related events"),
        description=_(
            'Used when "Only the events I choose myself" is selected above. '
            "Any event of the entity can be picked, whatever its agenda. "
            "Items are displayed in the order you set here and link to the "
            "default events view of the control panel."
        ),
        value_type=schema.Choice(source="imio.smartweb.vocabulary.EventsFromEntity"),
        required=False,
    )
    directives.widget(
        "specific_related_events",
        TranslatedAjaxSelectWidget,
        vocabulary="imio.smartweb.vocabulary.EventsFromEntity",
        pattern_options={"multiple": True},
    )

    nb_results_by_batch = schema.Choice(
        title=_("Number of items per batch"),
        required=True,
        default=3,
        values=[1, 2, 3, 4],
    )

    max_nb_batches = schema.Int(
        title=_("Maximum number of batches to display"),
        required=True,
        default=2,
        min=1,
        max=12,
    )

    link_text = schema.TextLine(
        title=_("Text for the link to the events view"),
        defaultFactory=see_all_default,
        required=True,
    )

    model.fieldset("layout", fields=["show_items_description"])
    show_items_description = schema.Bool(
        title=_("Show items description"), required=False
    )

    model.fieldset("layout", fields=["display_agendas_titles"])
    display_agendas_titles = schema.Bool(
        title=_("Display agendas titles"),
        description=_("If checked, display agendas titles in the carousel view."),
        required=False,
    )

    @invariant
    def required_events_source(data):
        if not carries_fields(
            data,
            "linking_rest_view",
            "events_source",
            "related_events",
            "specific_related_events",
        ):
            return
        if data.events_source == "selection":
            # linking_rest_view plays no part here: hand-picked items come from
            # the whole entity and link to the control panel's default view.
            if not data.specific_related_events:
                raise Invalid(_("Please select at least one event."))
            if not get_default_view_url("events"):
                raise Invalid(
                    _("No default events view is configured in the Smartweb settings.")
                )
            return
        if not data.linking_rest_view:
            raise Invalid(_("Please select an events view."))
        if not data.related_events:
            raise Invalid(_("Please select an agenda."))
        # On a real submission this is the view *itself*, not a RelationValue
        # (see RelationChoiceContentBrowserWidgetConverter). Both shapes must
        # work: a RelationValue still arrives against a stored object.
        events_view = getattr(
            data.linking_rest_view, "to_object", data.linking_rest_view
        )
        # An empty scope means the authentic source is unreachable, never
        # "nothing is in scope", hence the "scope and" guard below.
        scope = get_agenda_scope_uids(getattr(events_view, "selected_agenda", None))
        if scope and data.related_events not in scope:
            raise Invalid(
                _("This agenda is not displayed by the selected events view.")
            )


@implementer(ISectionEvents)
class SectionEvents(Section):
    """SectionEvents class"""

    manage_display = True
    show_items_date = True
