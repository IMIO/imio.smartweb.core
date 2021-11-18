# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL, EVENTS_URL, NEWS_URL
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents.pages.procedure.utils import sign_url
from imio.smartweb.core.interfaces import ISmartwebIcon
from imio.smartweb.core.utils import concat_voca_term
from imio.smartweb.core.utils import concat_voca_title
from imio.smartweb.core.utils import get_categories
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import get_wca_token
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.dexterity.content import Item
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import json
import os
import requests


class IconsVocabularyFactory:
    def __call__(self, context=None):
        icon_prefix = "smartweb.icon."
        registry = getUtility(IRegistry)
        icons = []
        for record in registry.records.values():
            if record.interfaceName != ISmartwebIcon.__identifier__:
                continue
            name = record.__name__.replace(icon_prefix, "")
            icons.append(
                {
                    "title": record.field.title,
                    "name": name,
                }
            )
        icons.sort(key=lambda k: k["title"])
        terms = [
            SimpleTerm(value=i["name"], token=i["name"], title=i["title"])
            for i in icons
        ]
        return SimpleVocabulary(terms)


IconsVocabulary = IconsVocabularyFactory()


class RemoteProceduresVocabularyFactory:
    def __call__(self, context=None):
        # sample : "https://olln-formulaires.guichet-citoyen.be/api/formdefs/"
        url = api.portal.get_registry_record("smartweb.url_formdefs_api")
        # sample : "568DGess2x8j8twv7x2Y2MApjn789xfG7jM27r399q4xSD27Jz"
        key = api.portal.get_registry_record("smartweb.secret_key_api")
        orig = "ia.smartweb"
        if not url:
            return SimpleVocabulary([])
        query_full = sign_url(url, key, orig)
        try:
            response = requests.get(query_full)
        except Exception:
            return SimpleVocabulary([])

        if response.status_code != 200:
            return SimpleVocabulary([])

        json_procedures = json.loads(response.text)
        return SimpleVocabulary(
            [
                SimpleTerm(value=elem["url"], title=elem["title"])
                for elem in json_procedures.get("data", [])
            ]
        )


RemoteProceduresVocabulary = RemoteProceduresVocabularyFactory()


class CurrentFolderPagesVocabularyFactory:
    def __call__(self, context=None):
        brains = api.content.find(
            context=context, depth=1, object_provides=IPages, sort_on="sortable_title"
        )
        brains = [b for b in brains if b.portal_type != "imio.smartweb.Footer"]
        terms = [SimpleTerm(value=b.UID, token=b.UID, title=b.Title) for b in brains]
        return SimpleVocabulary(terms)


CurrentFolderPagesVocabulary = CurrentFolderPagesVocabularyFactory()


class BootstrapCSSVocabularyFactory:
    def __call__(self, context=None):
        bootstrap_css = [
            ("col-sm-3", _("Quarter of width")),
            ("col-sm-4", _("Third of width")),
            ("col-sm-6", _("Half of width")),
            ("col-sm-8", _("Two third of width")),
            ("col-sm-9", _("Three quarter of width")),
            ("col-sm-12", _("Full width")),
        ]
        terms = [SimpleTerm(value=t[0], token=t[0], title=t[1]) for t in bootstrap_css]
        return SimpleVocabulary(terms)


BootstrapCSSVocabulary = BootstrapCSSVocabularyFactory()


class SubsiteDisplayModeVocabularyFactory:
    def __call__(self, context=None):
        display_mode = [
            ("title", _("Title")),
            ("logo", _("Logo")),
            ("logo_title", _("Logo and title")),
        ]
        terms = [SimpleTerm(value=t[0], token=t[0], title=t[1]) for t in display_mode]
        return SimpleVocabulary(terms)


SubsiteDisplayModeVocabulary = SubsiteDisplayModeVocabularyFactory()


class ContactBlocksVocabularyFactory:
    def __call__(self, context=None):
        values = [
            ("logo", _("Logo")),
            ("leadimage", _("Lead Image")),
            ("titles", _("Title and Subtitle")),
            ("contact_informations", _("Contact informations")),
            ("address", _("Address")),
            ("map", _("Map")),
            ("schedule", _("Schedule")),
            ("description", _("Description")),
            ("gallery", _("Gallery")),
        ]
        terms = [
            SimpleVocabulary.createTerm(value[0], value[0], value[1])
            for value in values
        ]
        return SimpleVocabulary(terms)


ContactBlocksVocabulary = ContactBlocksVocabularyFactory()


class RemoteContactsVocabularyFactory:
    def __call__(self, context=None):
        entity_uid = api.portal.get_registry_record("smartweb.directory_entity_uid")
        params = [
            "portal_type=imio.directory.Contact",
            "selected_entities={}".format(entity_uid),
            "sort_on=breadcrumb",
            "b_size=1000000",
            "metadata_fields=UID",
            "metadata_fields=breadcrumb",
        ]
        url = "{}/@search?{}".format(DIRECTORY_URL, "&".join(params))
        json_contacts = get_json(url)
        if json_contacts is None or len(json_contacts.get("items", [])) == 0:
            return SimpleVocabulary([])
        return SimpleVocabulary(
            [
                SimpleTerm(value=elem["UID"], title=elem["breadcrumb"])
                for elem in json_contacts.get("items")
            ]
        )


RemoteContactsVocabulary = RemoteContactsVocabularyFactory()


def get_entities_vocabulary(portal_type, base_url):
    params = [
        "portal_type={}".format(portal_type),
        "sort_on=sortable_title",
        "b_size=1000000",
        "metadata_fields=UID",
    ]
    url = "{}/@search?{}".format(base_url, "&".join(params))
    json_entities = get_json(url)
    if json_entities is None or len(json_entities.get("items", [])) == 0:
        return SimpleVocabulary([])
    return SimpleVocabulary(
        [
            SimpleTerm(value=elem["UID"], title=elem["title"])
            for elem in json_entities.get("items")
        ]
    )


class RemoteDirectoryEntitiesVocabularyFactory:
    def __call__(self, context=None):
        return get_entities_vocabulary("imio.directory.Entity", DIRECTORY_URL)


RemoteDirectoryEntitiesVocabulary = RemoteDirectoryEntitiesVocabularyFactory()


class RemoteEventsEntitiesVocabularyFactory:
    def __call__(self, context=None):
        return get_entities_vocabulary("imio.events.Entity", EVENTS_URL)


RemoteEventsEntitiesVocabulary = RemoteEventsEntitiesVocabularyFactory()


class RemoteNewsEntitiesVocabularyFactory:
    def __call__(self, context=None):
        return get_entities_vocabulary("imio.news.Entity", NEWS_URL)


RemoteNewsEntitiesVocabulary = RemoteNewsEntitiesVocabularyFactory()


def content_container_vocabulary(entity_uid, portal_type, base_url):
    """Gets containers of events / news"""
    url = "{}/@search?UID={}".format(base_url, entity_uid)
    entity_json = get_json(url)
    entity_url = entity_json.get("items")[0].get("@id")
    params = [
        "portal_type={}".format(portal_type),
        "sort_on=sortable_title",
        "b_size=1000000",
        "metadata_fields=UID",
    ]
    url = "{}/@search?{}".format(entity_url, "&".join(params))
    json_folders = get_json(url)
    if json_folders is None or len(json_folders.get("items", [])) == 0:
        return SimpleVocabulary([])
    return SimpleVocabulary(
        [
            SimpleTerm(value=elem["UID"], token=elem["UID"], title=elem["title"])
            for elem in json_folders.get("items")
        ]
    )


class RemoteAgendasVocabularyFactory:
    def __call__(self, context=None):
        entity_uid = api.portal.get_registry_record("smartweb.events_entity_uid")
        return content_container_vocabulary(
            entity_uid, "imio.events.Agenda", EVENTS_URL
        )


RemoteAgendasVocabulary = RemoteAgendasVocabularyFactory()


class RemoteNewsFoldersVocabularyFactory:
    def __call__(self, context=None):
        entity_uid = api.portal.get_registry_record("smartweb.news_entity_uid")
        return content_container_vocabulary(
            entity_uid, "imio.news.NewsFolder", NEWS_URL
        )


RemoteNewsFoldersVocabulary = RemoteNewsFoldersVocabularyFactory()


class AlignmentVocabularyFactory:
    def __call__(self, context=None):
        alignment = [
            ("left", _("Left")),
            ("right", _("Right")),
            ("bottom", _("Bottom")),
            ("top", _("Top")),
        ]
        terms = [SimpleTerm(value=t[0], token=t[0], title=t[1]) for t in alignment]
        return SimpleVocabulary(terms)


AlignmentVocabulary = AlignmentVocabularyFactory()


class ImageSizeVocabularyFactory:
    def __call__(self, context=None):
        image_size = [
            ("large", _("Full width")),
            ("preview", _("Half page")),
            ("mini", _("Third page")),
        ]
        terms = [SimpleTerm(value=t[0], token=t[0], title=t[1]) for t in image_size]
        return SimpleVocabulary(terms)


ImageSizeVocabulary = ImageSizeVocabularyFactory()


class DirectoryViewsVocabularyFactory(object):
    def __call__(self, context=None):
        if not isinstance(context, Item):
            context = api.portal.get()
        brains = api.content.find(
            context=context, portal_type="imio.smartweb.DirectoryView"
        )
        terms = [SimpleTerm(value=b.UID, token=b.UID, title=b.Title) for b in brains]
        return SimpleVocabulary(terms)


DirectoryViewsVocabulary = DirectoryViewsVocabularyFactory()


class EventsViewsVocabularyFactory(object):
    def __call__(self, context=None):
        if not isinstance(context, Item):
            context = api.portal.get()
        brains = api.content.find(
            context=context, portal_type="imio.smartweb.EventsView"
        )
        terms = [SimpleTerm(value=b.UID, token=b.UID, title=b.Title) for b in brains]
        return SimpleVocabulary(terms)


EventsViewsVocabulary = EventsViewsVocabularyFactory()


class NewsViewsVocabularyFactory(object):
    def __call__(self, context=None):
        if not isinstance(context, Item):
            context = api.portal.get()
        brains = api.content.find(context=context, portal_type="imio.smartweb.NewsView")
        terms = [SimpleTerm(value=b.UID, token=b.UID, title=b.Title) for b in brains]
        return SimpleVocabulary(terms)


NewsViewsVocabulary = NewsViewsVocabularyFactory()


class CategoryAndTopicsVocabularyFactory:
    def __call__(self, context=None):
        categories_taxo = get_categories()
        language = api.portal.get_current_language(context=context)
        categories_voca = categories_taxo.makeVocabulary(language).inv_data

        topics_voca_factory = getUtility(
            IVocabularyFactory, "imio.smartweb.vocabulary.Topics"
        )
        topics_voca = topics_voca_factory(context)

        terms = []

        for cat in categories_voca:
            for topic in topics_voca:
                term = SimpleTerm(
                    value=concat_voca_term(cat, topic.value),
                    token=concat_voca_term(cat, topic.token),
                    title=concat_voca_title(
                        categories_voca[cat],
                        translate(topic.title, target_language=language),
                    ),
                )
                terms.append(term)

            terms.append(
                SimpleTerm(
                    value=cat,
                    token=cat,
                    title=categories_voca[cat],
                )
            )
        return SimpleVocabulary(terms)


CategoryAndTopicsVocabulary = CategoryAndTopicsVocabularyFactory()


class FilteredCategoryAndTopicsVocabularyFactory:
    def __call__(self, context=None):
        voca_registry = api.portal.get_registry_record(
            name="smartweb.category_and_topics_vocabulary"
        )
        terms = []
        if voca_registry is not None:
            terms = [
                SimpleTerm(value=r, token=r, title=voca_registry[r])
                for r in voca_registry
            ]

        return SimpleVocabulary(terms)


FilteredCategoryAndTopicsVocabulary = FilteredCategoryAndTopicsVocabularyFactory()


class DirectoryCategoriesVocabularyFactory:
    def __call__(self, context=None):
        client_id = os.environ.get("RESTAPI_DIRECTORY_CLIENT_ID")
        client_secret = os.environ.get("RESTAPI_DIRECTORY_CLIENT_SECRET")
        id_token = get_wca_token(client_id, client_secret)
        url = f"{DIRECTORY_URL}/@vocabularies/collective.taxonomy.contact_category"
        categories_json = get_json(url, auth="Bearer {0}".format(id_token))
        if categories_json is None or len(categories_json.get("items", [])) == 0:
            return SimpleVocabulary([])
        return SimpleVocabulary(
            [
                SimpleTerm(
                    value=elem["token"], token=elem["token"], title=elem["title"]
                )
                for elem in categories_json.get("items")
            ]
        )


DirectoryCategoriesVocabulary = DirectoryCategoriesVocabularyFactory()


class EventsTypesVocabularyFactory:
    def __call__(self, context=None):
        client_id = os.environ.get("RESTAPI_EVENTS_CLIENT_ID")
        client_secret = os.environ.get("RESTAPI_EVENTS_CLIENT_SECRET")
        id_token = get_wca_token(client_id, client_secret)
        url = f"{EVENTS_URL}/@vocabularies/imio.events.vocabulary.EventTypes"
        eventstypes_json = get_json(url, auth="Bearer {0}".format(id_token))
        if eventstypes_json is None or len(eventstypes_json.get("items", [])) == 0:
            return SimpleVocabulary([])
        return SimpleVocabulary(
            [
                SimpleTerm(
                    value=elem["token"], token=elem["token"], title=elem["title"]
                )
                for elem in eventstypes_json.get("items")
            ]
        )


EventsTypesVocabulary = EventsTypesVocabularyFactory()
