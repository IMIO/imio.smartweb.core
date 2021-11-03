# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ISmartwebControlPanel(Interface):

    url_formdefs_api = schema.TextLine(
        title=_(u"Url to get forms from your e-guichet"),
        description=_(
            u"Example : https://COMMUNE-formulaires.guichet-citoyen.be/api/formdefs/"
        ),
        required=False,
    )

    secret_key_api = schema.Password(
        title=_(u"Secret key"),
        description=_(u"Secret key to use API"),
        required=False,
    )

    directory_entity_uid = schema.Choice(
        title=_(u"Directory entity"),
        source="imio.smartweb.vocabulary.RemoteDirectoryEntities",
        required=False,
    )

    events_entity_uid = schema.Choice(
        title=_(u"Events entity"),
        source="imio.smartweb.vocabulary.RemoteEventsEntities",
        required=False,
    )

    news_entity_uid = schema.Choice(
        title=_(u"News entity"),
        source="imio.smartweb.vocabulary.RemoteNewsEntities",
        required=False,
    )

    directory_solr_core = schema.TextLine(
        title=_(u"Directory SolR Core ID"),
        default="directory",
        required=False,
    )

    events_solr_core = schema.TextLine(
        title=_(u"Events SolR Core ID"),
        default="events",
        required=False,
    )

    news_solr_core = schema.TextLine(
        title=_(u"News SolR Core ID"),
        default="news",
        required=False,
    )

    default_directory_view = schema.Choice(
        title=_(u"Default directory view"),
        description=_(u"This information is used for search results redirection"),
        source="imio.smartweb.vocabulary.DirectoryViews",
        required=False,
    )

    default_events_view = schema.Choice(
        title=_(u"Default events view"),
        description=_(u"This information is used for search results redirection"),
        source="imio.smartweb.vocabulary.EventsViews",
        required=False,
    )

    default_news_view = schema.Choice(
        title=_(u"Default news view"),
        description=_(u"This information is used for search results redirection"),
        source="imio.smartweb.vocabulary.NewsViews",
        required=False,
    )

    category_and_topics_vocabulary = schema.Dict(
        title=_(u"Category and topics vocabulary setting for TeleServices"),
        description=_(
            u"Choose a term from the vocabulary and define the corresponding name"
        ),
        key_type=schema.Choice(
            title=_(u"Vocabulary term"),
            source="imio.smartweb.vocabulary.CategoryAndTopics",
        ),
        value_type=schema.TextLine(
            title=_(u"Name"),
        ),
        required=False,
    )


class SmartwebControlPanelForm(RegistryEditForm):
    schema = ISmartwebControlPanel
    schema_prefix = "smartweb"
    label = _(u"Smartweb Settings")


SmartwebControlPanelView = layout.wrap_form(
    SmartwebControlPanelForm, ControlPanelFormWrapper
)
