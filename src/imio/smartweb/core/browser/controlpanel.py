# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ISmartwebControlPanel(Interface):

    url_formdefs_api = schema.TextLine(
        title=_("Url to get forms from your e-guichet"),
        description=_(
            "Example : https://COMMUNE-formulaires.guichet-citoyen.be/api/formdefs/"
        ),
        required=False,
    )

    secret_key_api = schema.Password(
        title=_("Secret key"),
        description=_("Secret key to use API"),
        required=False,
    )

    directory_entity_uid = schema.Choice(
        title=_("Directory entity"),
        source="imio.smartweb.vocabulary.RemoteDirectoryEntities",
        required=False,
    )

    events_entity_uid = schema.Choice(
        title=_("Events entity"),
        source="imio.smartweb.vocabulary.RemoteEventsEntities",
        required=False,
    )

    news_entity_uid = schema.Choice(
        title=_("News entity"),
        source="imio.smartweb.vocabulary.RemoteNewsEntities",
        required=False,
    )

    directory_solr_core = schema.TextLine(
        title=_("Directory SolR Core ID"),
        default="directory",
        required=False,
    )

    events_solr_core = schema.TextLine(
        title=_("Events SolR Core ID"),
        default="events",
        required=False,
    )

    news_solr_core = schema.TextLine(
        title=_("News SolR Core ID"),
        default="news",
        required=False,
    )

    default_directory_view = schema.Choice(
        title=_("Default directory view"),
        description=_("This information is used for search results redirection"),
        source="imio.smartweb.vocabulary.DirectoryViews",
        required=False,
    )

    default_events_view = schema.Choice(
        title=_("Default events view"),
        description=_("This information is used for search results redirection"),
        source="imio.smartweb.vocabulary.EventsViews",
        required=False,
    )

    default_news_view = schema.Choice(
        title=_("Default news view"),
        description=_("This information is used for search results redirection"),
        source="imio.smartweb.vocabulary.NewsViews",
        required=False,
    )

    category_and_topics_vocabulary = schema.Dict(
        title=_("Category and topics vocabulary setting for TeleServices"),
        description=_(
            "Choose a term from the vocabulary and define the corresponding name"
        ),
        key_type=schema.Choice(
            title=_("Vocabulary term"),
            source="imio.smartweb.vocabulary.CategoryAndTopics",
        ),
        value_type=schema.TextLine(
            title=_("Name"),
        ),
        required=False,
    )


class SmartwebControlPanelForm(RegistryEditForm):
    schema = ISmartwebControlPanel
    schema_prefix = "smartweb"
    label = _("Smartweb Settings")


SmartwebControlPanelView = layout.wrap_form(
    SmartwebControlPanelForm, ControlPanelFormWrapper
)
