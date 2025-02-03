# -*- coding: utf-8 -*-

from imio.smartweb.core.browser.controlpanel import ISmartwebControlPanel
from imio.smartweb.core.contents import IPages
from imio.smartweb.locales import SmartwebMessageFactory as _
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from plone import api
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.registry import field
from plone.registry import Record
from plone.registry.interfaces import IRegistry
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.schema import getFieldNames
from zope.schema import TextLine

import logging

logger = logging.getLogger("imio.smartweb.core")
PROFILEID = "profile-imio.smartweb.core:default"


def configure_first_official_release(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "plone.app.registry")
    portal_setup.runImportStepFromProfile(PROFILEID, "typeinfo")

    portal_setup.runImportStepFromProfile(PROFILEID, "catalog")
    portal_catalog = api.portal.get_tool("portal_catalog")
    # we could index only imio.smartweb.Page contents, but for some reason
    # api.content.find() doesn't find all objects
    portal_catalog.clearFindAndRebuild()
    logger.info("Reindexed catalog for category_and_topics index / metadata")


def set_thumb_scales(context):
    api.portal.set_registry_record("plone.thumb_scale_listing", "liste")
    api.portal.set_registry_record("plone.thumb_scale_summary", "vignette")


def update_actions(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "actions")
    portal_actions = api.portal.get_tool("portal_actions")
    header_actions = getattr(portal_actions, "header_actions")
    if "e_guichet" in header_actions.objectIds():
        header_actions._delObject("e_guichet")
        logger.info("Deleted e_guichet header action")


def update_icons_and_names(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(
        "profile-imio.smartweb.core:icons-basic", "plone.app.registry"
    )
    registry = getUtility(IRegistry)
    for old_icon in [
        "annuaire",
        "demarches",
        "ecoles",
        "horaires",
        "mobilite",
        "parkings",
        "sports",
        "tourisme",
        "travaux",
    ]:
        if f"smartweb.icon.{old_icon}" in registry:
            del registry.records[f"smartweb.icon.{old_icon}"]


def reload_registry(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "plone.app.registry")


def reload_rolemap(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "rolemap")


def reload_types(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "typeinfo")


def reload_workflows(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILEID, "workflow")


def check_itinerary_if_address_is_checked(context):
    brains = api.content.find(portal_type="imio.smartweb.SectionContact")
    for brain in brains:
        obj = brain.getObject()
        if "address" in obj.visible_blocks:
            if "itinerary" not in obj.visible_blocks:
                obj.visible_blocks.append("itinerary")
                obj._p_changed = 1


def add_placeholder_to_faceted_textsearch(context):
    brains = api.content.find(object_provides=IFacetedNavigable)
    for brain in brains:
        obj = brain.getObject()
        handler = ICriteria(obj)
        for criterion in handler.criteria:
            if criterion.widget == "text":
                criterion.placeholder = "Recherche"
                handler.criteria._p_changed = 1


def exclude_footers_from_parent_listing(context):
    brains = api.content.find(portal_type="imio.smartweb.Footer")
    for brain in brains:
        footer = brain.getObject()
        footer.exclude_from_parent_listing = True
        footer.reindexObject(idxs=["exclude_from_parent_listing"])


def reindex_all_pages(context):
    brains = api.content.find(object_provides=IPages)
    for brain in brains:
        try:
            obj = brain.getObject()
        except KeyError:
            logger.warn(f"getObject failed on {brain.getURL()}")
        else:
            obj.reindexObject()


def add_sendinblue_button_settings(context):
    fields = getFieldNames(ISmartwebControlPanel)
    fields.remove("sendinblue_button_position")
    fields.remove("sendinblue_button_text")
    registry = getUtility(IRegistry)
    registry.registerInterface(ISmartwebControlPanel, omit=fields, prefix="smartweb")


def find_multiple_categories_directory_views(context):
    brains = api.content.find(portal_type="imio.smartweb.DirectoryView")
    for brain in brains:
        directory = brain.getObject()
        if (
            directory.selected_categories is None
            or len(directory.selected_categories) <= 1
        ):
            continue
        msg = f"Found directory view with multiple categories : {directory.absolute_url()}"
        logger.warning(msg)
        api.portal.send_email(
            recipient="boulch@imio.be",
            subject="Multiple contacts categories in directory view",
            body=msg,
        )


def to_related_contacts(context):
    brains = api.content.find(portal_type="imio.smartweb.SectionContact")
    for brain in brains:
        obj = brain.getObject()
        if hasattr(obj, "related_contact"):
            setattr(obj, "related_contacts", [obj.related_contact])
            setattr(obj, "nb_contact_by_line", 1)
            delattr(obj, "related_contact")


def remove_deprecated_cropping_annotations(context):
    with api.env.adopt_user(username="admin"):
        brains = api.content.find(portal_type="imio.smartweb.Folder")
        for brain in brains:
            obj = brain.getObject()
            annotations = IAnnotations(obj)
            scales = annotations.get(PAI_STORAGE_KEY)
            if scales is not None and "banner_banner" in scales:
                del scales["banner_banner"]
                obj.reindexObject()
                logger.info(
                    f"Remove deprecated banner_banner cropping annotation on {obj.absolute_url()}"
                )


def migrate_is_in_portrait_mode(context):
    with api.env.adopt_user(username="admin"):
        brains = api.content.find(portal_type="imio.smartweb.SectionContact")
        for brain in brains:
            obj = brain.getObject()
            is_in_portrait_mode = getattr(obj, "is_in_portrait_mode", False)
            if is_in_portrait_mode:
                obj.orientation = "portrait"
                logger.info(
                    f"Migrated potrait mode to orientation portrait for {obj.absolute_url()}"
                )


def migrate_old_scales_from_vocabulary(context):
    with api.env.adopt_user(username="admin"):
        brains = api.content.find(
            portal_type=[
                "imio.smartweb.SectionContact",
                "imio.smartweb.SectionGallery",
            ]
        )
        for brain in brains:
            obj = brain.getObject()
            old_scale = obj.image_scale
            if old_scale in ["affiche", "vignette", "liste"]:
                continue
            new_scale = "affiche"
            if old_scale == "preview":
                new_scale = "vignette"
            obj.image_scale = new_scale
            logger.info(
                f"Migrated deprecated scale from {old_scale} to {new_scale} for {obj.absolute_url()}"
            )


def migrate_old_sizes_from_section_text(context):
    with api.env.adopt_user(username="admin"):
        brains = api.content.find(portal_type=["imio.smartweb.SectionText"])
        for brain in brains:
            obj = brain.getObject()
            old_scale = obj.image_size
            if old_scale in ["affiche", "vignette"]:
                continue
            new_scale = "affiche"
            if old_scale == "preview":
                new_scale = "vignette"
            obj.image_size = new_scale
            logger.info(
                f"Migrated deprecated scale from {old_scale} to {new_scale} for {obj.absolute_url()}"
            )


def update_control_panel_combo_api_url(context):
    url_ts = ""
    try:
        url_ts = api.portal.get_registry_record("smartweb.url_formdefs_api") or ""
    except:
        logger.info("La clé 'smartweb.url_formdefs_api' a été supprimée.")
        return
    url_ts = url_ts.replace("/api", "")
    url_ts = url_ts.replace("-formulaires", "")
    api.portal.set_registry_record("smartweb.url_formdefs_api", url_ts)


def update_control_panel_combo_api_fieldname(context):
    url_ts = ""
    try:
        url_ts = api.portal.get_registry_record("smartweb.url_formdefs_api") or ""
    except:
        logger.info("La clé 'smartweb.url_formdefs_api' a été supprimée.")
    registry = getUtility(IRegistry)
    records = registry.records
    if "smartweb.url_ts" in records:
        return
    logger.info("Adding smartweb.url_ts to registry")  # noqa
    record = Record(
        field.TextLine(
            title=_("Url to e-guichet"),
            description=_("Exemple : https://COMMUNE.guichet-citoyen.be"),
            required=False,
        ),
        value=url_ts,
    )
    records["smartweb.url_ts"] = record

    record = Record(
        field.TextLine(
            title=_(
                "Username to consume e-guichet ideabox API (get Campaign, projects,...)"
            ),
            default="ideabox",
            required=False,
        )
    )
    records["smartweb.iaideabox_api_username"] = record

    record = Record(
        field.Password(
            title=_(
                "Password to consume e-guichet ideabox API (get Campaign, projects,...)"
            ),
            required=False,
        )
    )
    records["smartweb.iaideabox_api_password"] = record
    try:
        del registry.records["smartweb.url_formdefs_api"]
        logger.info("La clé 'smartweb.url_formdefs_api' a été supprimée.")
    except KeyError:
        logger.info("La clé 'smartweb.url_formdefs_api' n'existe pas dans le registre.")
