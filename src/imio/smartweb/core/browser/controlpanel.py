# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import directives
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class ISendinblueTextRowSchema(Interface):
    language = schema.TextLine(
        title=_("Language (en, fr,...)"),
        description=_("Enter the language code. Ex.: en"),
    )

    text = schema.TextLine(title=_("Text"), description=_("Your button title"))


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

    propose_directory_url = schema.URI(
        title=_("Url to propose a new citizen contact"),
        required=False,
    )

    propose_events_url = schema.URI(
        title=_("Url to propose a new citizen event"),
        required=False,
    )

    propose_news_url = schema.URI(
        title=_("Url to propose a new citizen news"),
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

    sendinblue_button_position = schema.Choice(
        title=_("SendInBlue : Define button position"),
        source="imio.smartweb.vocabulary.SendInBlueButtonPosition",
        default="button_bottom",
        required=True,
    )

    sendinblue_button_text = schema.List(
        title=_("SendInBlue : Define button text"),
        description=_("Choose SendInblue submission button text"),
        value_type=DictRow(
            title="Value",
            schema=ISendinblueTextRowSchema,
        ),
        default=[],
        required=True,
    )
    directives.widget("sendinblue_button_text", DataGridFieldFactory, auto_append=False)

    plausible_url = schema.TextLine(
        title=_("Plausible URL"),
        description=_(
            "Example : plausible.imio.be (SMARTWEB_PLAUSIBLE_URL varenv has precedence over this.)"
        ),
        required=False,
    )

    plausible_site = schema.TextLine(
        title=_("Plausible Site"),
        description=_(
            "Example : namur.be (SMARTWEB_PLAUSIBLE_SITE varenv has precedence over this.)"
        ),
        required=False,
    )

    plausible_token = schema.TextLine(
        title=_("Plausible Token"),
        description=_(
            "Plausible authentification token (SMARTWEB_PLAUSIBLE_TOKEN varenv has precedence over this.)"
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
