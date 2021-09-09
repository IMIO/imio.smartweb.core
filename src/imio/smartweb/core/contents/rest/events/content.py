# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.autoform.directives import write_permission
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IEventsView(model.Schema):
    """ """

    nb_results = schema.Int(
        title=_(u"Number of items to display"), default=20, required=True
    )
    see_more_link = schema.URI(title=_(u"See more link"), required=False)
    directives.widget(selected_agendas=SelectFieldWidget)
    selected_agendas = schema.List(
        title=_(u"Selected agendas"),
        description=_(u"Select agendas to display"),
        value_type=schema.Choice(vocabulary="imio.smartweb.vocabulary.RemoteAgendas"),
        required=True,
    )
    show_items_description = schema.Bool(
        title=_(u"Show items description"), default=True, required=False
    )


@implementer(IEventsView)
class EventsView(Container):
    """EventsView class"""
