# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
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
    # https://COMMUNE-formulaires.guichet-citoyen.be/api
    url_ts = schema.TextLine(
        title=_("Url to e-guichet"),
        description=_("Example : https://COMMUNE.guichet-citoyen.be"),
        required=False,
    )

    secret_key_api = schema.Password(
        title=_("Secret key"),
        description=_("Secret key to use API"),
        required=False,
    )

    iaideabox_api_username = schema.TextLine(
        title=_(
            "Username to consume e-guichet ideabox API (get Campaign, projects,...)"
        ),
        default="ideabox",
        required=False,
    )

    iaideabox_api_password = schema.Password(
        title=_(
            "Password to consume e-guichet ideabox API (get Campaign, projects,...)"
        ),
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

    iadeliberations_url = schema.TextLine(
        title=_("I.A. Deliberations' url"),
        description=_(
            "For staging : https://conseil.staging.imio.be | for production : https://www.deliberations.be"
        ),
        default="https://www.deliberations.be",
        required=False,
    )

    iadeliberations_api_username = schema.TextLine(
        title=_("Username to consume I.A. Deliberations API"),
        default="wsviewersmartweb",
        required=False,
    )

    iadeliberation_api_password = schema.Password(
        title=_("Password to consume I.A. Deliberations API"),
        required=False,
    )

    iadeliberations_institution = schema.Choice(
        title=_("I.A. Deliberations : Institutions"),
        source="imio.smartweb.vocabulary.IADeliberationsInstitutions",
        required=False,
    )


class SmartwebControlPanelForm(RegistryEditForm):
    schema = ISmartwebControlPanel
    schema_prefix = "smartweb"
    label = _("Smartweb Settings")

    def applyChanges(self, data):
        # Get current registry value for (controlpanel) passwords
        iadeliberation_pwd = api.portal.get_registry_record(
            "smartweb.iadeliberation_api_password"
        )

        iaideabox_pwd = api.portal.get_registry_record(
            "smartweb.iaideabox_api_password"
        )

        secret_key_api = api.portal.get_registry_record("smartweb.secret_key_api")

        # if data is None when we apply changes for password fields we keep password from registry
        if not data.get("iadeliberation_api_password"):
            data["iadeliberation_api_password"] = iadeliberation_pwd

        if not data.get("iaideabox_api_password"):
            data["iaideabox_api_password"] = iaideabox_pwd

        if not data.get("secret_key_api"):
            data["secret_key_api"] = secret_key_api

        return super().applyChanges(data)

    def updateFields(self):
        """Override updateFields to hide fields based on ideabox profile installation."""
        super(SmartwebControlPanelForm, self).updateFields()

        # Check if the 'ideabox' profile is installed
        portal_setup = api.portal.get_tool(name="portal_setup")
        profile_version = portal_setup.getLastVersionForProfile(
            "imio.smartweb.core:ideabox"
        )

        if profile_version == "unknown":
            # Hide the field related to Idea Box if the profile is not installed
            self.fields = self.fields.omit("iaideabox_api_username")
            self.fields = self.fields.omit("iaideabox_api_password")


SmartwebControlPanelView = layout.wrap_form(
    SmartwebControlPanelForm, ControlPanelFormWrapper
)
