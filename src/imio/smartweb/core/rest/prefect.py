# -*- coding: utf-8 -*-
"""@prefect: the editorial content of a page, as JSON, for the Prefect ETL.

No rendering view is used. The only external service called is imio.directory,
for the contact sections; everything else is what is stored in the page and
its sections. Every section keeps its place in
the page; a section that cannot be serialized gets ``status: "error"`` instead
of failing the whole response.
"""

from Acquisition import aq_base
from Acquisition import aq_chain
from Acquisition import aq_inner
from imio.smartweb.common.contact_utils import formatted_schedule
from imio.smartweb.common.utils import translate_vocabulary_term
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.contents.sections.contact.utils import ContactProperties
from imio.smartweb.core.contents.sections.contact.utils import (
    get_contacts_search_url,
)
from imio.smartweb.core.utils import get_category
from lxml import html as lxml_html
from lxml_html_clean import Cleaner
from plone import api
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.utils import RESOLVEUID_RE
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot
from urllib.parse import urljoin
from urllib.parse import urlparse
from ZODB.POSException import ConflictError

import logging
import requests

logger = logging.getLogger("imio.smartweb.core")

SCHEMA_VERSION = 1

# seconds, for each request to imio.directory (contact sections only)
DIRECTORY_TIMEOUT = 10

PAGE_TYPES = {
    "imio.smartweb.Page": "page",
    "imio.smartweb.PortalPage": "portal_page",
    "imio.smartweb.Procedure": "procedure",
}

HTTP_SCHEMES = ("http", "https")
LINK_SCHEMES = HTTP_SCHEMES + ("mailto", "tel")

# Fixed options: the exposed HTML never depends on the portal filter settings
# (plone.base IFilterSchema), which a site administrator can relax.
CLEANER = Cleaner(
    scripts=True,
    javascript=True,
    comments=True,
    style=True,
    inline_style=True,
    links=True,
    meta=True,
    page_structure=True,
    processing_instructions=True,
    embedded=True,
    frames=True,
    forms=True,
    annoying_tags=True,
    remove_unknown_tags=True,
    safe_attrs_only=True,
    safe_attrs=frozenset(["href", "src", "alt", "title", "colspan", "rowspan"]),
)


class PrefectGet(Service):
    """GET {page_url}/@prefect"""

    def reply(self):
        return serialize_page(aq_inner(self.context))


def serialize_page(page):
    language = page.Language() or api.portal.get_default_language()
    return {
        "schema_version": SCHEMA_VERSION,
        "uid": page.UID(),
        "url": page.absolute_url(),
        "type": PAGE_TYPES[page.portal_type],
        "language": language,
        "title": page.title,
        "description": page.description or None,
        "modified": json_compatible(page.modified()),
        "procedure_url": procedure_url(page),
        "metadata": serialize_metadata(page, language),
        "sections": [serialize_section(page, s) for s in page.listFolderContents()],
    }


def procedure_url(page):
    # procedure_ts stores the URL of the e-guichet form itself (see
    # RemoteProceduresVocabulary): no request is needed to read it
    url = getattr(page, "procedure_ts", None) or getattr(page, "procedure_url", None)
    return url or None


def serialize_metadata(page, language):
    return {
        "minisite": ancestor_summary(page, IImioSmartwebMinisite, IPloneSiteRoot),
        "subsite": ancestor_summary(page, IImioSmartwebSubsite, INavigationRoot),
        # the label the category viewlet displays
        "category": get_category(page) or None,
        "topics": vocabulary_labels(
            "imio.smartweb.vocabulary.Topics", getattr(page, "topics", None), language
        ),
        "iam": vocabulary_labels(
            "imio.smartweb.vocabulary.IAm", getattr(page, "iam", None), language
        ),
    }


def ancestor_summary(page, interface, stop_interface):
    """Title and URL of the first ancestor providing `interface`, searched up to
    the first ancestor providing `stop_interface` (as the subsite viewlets do).
    An ancestor the user cannot view is not exposed."""
    for obj in aq_chain(page)[1:]:
        if interface.providedBy(obj):
            if not api.user.has_permission("View", obj=obj):
                return None
            return {"title": obj.title, "url": obj.absolute_url()}
        if stop_interface.providedBy(obj):
            return None
    return None


def vocabulary_labels(vocabulary, values, language):
    labels = []
    for value in values or []:
        try:
            labels.append(translate_vocabulary_term(vocabulary, value, language[:2]))
        except LookupError:
            # a term removed from the vocabulary is not shown on the site either
            continue
    return labels


def serialize_section(page, section):
    data = {
        "id": section.getId(),
        "type": None,
        "status": "unsupported",
        "title": section.title or None,
        "title_hidden": bool(getattr(section, "hide_title", False)),
    }
    known = SECTIONS.get(section.portal_type)
    if known is None:
        # "imio.smartweb.SectionSlide" -> "slide"
        name = section.portal_type.split(".")[-1]
        data["type"] = name.removeprefix("Section").lower()
        return data
    data["type"], serializer = known
    try:
        specific = serializer(page, section)
    except ConflictError:
        raise
    except Exception:
        logger.exception(f"@prefect: cannot serialize {section.absolute_url()}")
        data["status"] = "error"
        return data
    data["status"] = "ok"
    data.update(specific)
    return data


def serialize_text(page, section):
    # the raw text, not output_relative_to(): plone.outputfilters would resolve
    # the links to private contents. clean_html resolves them with permissions.
    text = section.text.raw if section.text else None
    html, iframes = clean_html(text, page_base_url(page))
    image = None
    if getattr(aq_base(section), "image", None):
        image = {
            "url": f"{section.absolute_url()}/@@images/image",
            "caption": section.image_caption or None,
        }
    return {"html": html, "iframes": iframes, "image": image}


def serialize_html(page, section):
    html, iframes = clean_html(section.html, page_base_url(page))
    return {
        "description": section.description or None,
        "html": html,
        "iframes": iframes,
    }


def serialize_links(page, section):
    portal_url = api.portal.get().absolute_url()
    links = []
    for item in section.listFolderContents():
        value = item.remoteUrl or ""
        url = link_url(item, value)
        # from what the editor entered: a link that cannot be followed keeps
        # its nature (a deleted internal target, a forbidden external scheme)
        internal = (
            "${" in value
            or RESOLVEUID_RE.match(value) is not None
            or (url or "").startswith(portal_url)
        )
        links.append(
            {
                "title": item.title,
                "description": item.description or None,
                "url": url,
                "internal": internal,
            }
        )
    return {"description": section.description or None, "links": links}


def serialize_gallery(page, section):
    images = []
    for item in section.listFolderContents():
        title = item.title or None
        if item.image and title == item.image.filename:
            # same rule as GalleryView.alt_label: a filename is not a title
            title = None
        images.append(
            {
                "url": f"{item.absolute_url()}/@@images/image",
                "title": title,
                "description": item.description or None,
            }
        )
    return {"images": images}


def serialize_files(page, section):
    files = []
    for item in section.listFolderContents():
        publication_url = getattr(item, "publication_url", None)
        if publication_url:
            # same URL as anonymous visitors get (FilesView.retrieve_item_url)
            attached = getattr(item, "publication_attached_file", None) or {}
            url = publication_url
            mime_type = attached.get("content-type")
            size = attached.get("size")
        else:
            blob = getattr(item, "file", None)
            url = f"{item.absolute_url()}/@@download/file"
            mime_type = blob.contentType if blob else None
            size = blob.getSize() if blob else None
        files.append(
            {
                "title": item.title,
                "description": item.description or None,
                "url": url,
                "mime_type": mime_type or None,
                "size": size,
            }
        )
    return {"files": files}


def serialize_video(page, section):
    # no oEmbed request: the URL is enough to rebuild a link
    return {
        "description": section.description or None,
        "video_url": section.video_url,
    }


def serialize_map(page, section):
    geolocation = getattr(section, "geolocation", None)
    return {
        "latitude": geolocation.latitude if geolocation else None,
        "longitude": geolocation.longitude if geolocation else None,
    }


def serialize_postit(page, section):
    postits = [
        {
            "title": postit.get("title") or None,
            "subtitle": postit.get("subtitle") or None,
            "description": postit.get("description") or None,
        }
        for postit in section.postits or []
    ]
    return {"description": section.description or None, "postits": postits}


def serialize_selections(page, section):
    items = []
    for relation in section.selected_items or []:
        obj = visible_object(relation)
        if obj is None:
            continue
        items.append(
            {
                "title": obj.title,
                "description": obj.description or None,
                "url": obj.absolute_url(),
            }
        )
    return {"items": items}


def serialize_external_content(page, section):
    # the plugins of ExternalContentView are not run: they render widgets
    return {
        "description": section.description or None,
        "url": section.external_content_url,
    }


def serialize_contact(page, section):
    """The contacts as the section displays them, from imio.directory.

    The only section that calls an external service. A network or HTTP error
    raises, so the section gets status "error" instead of looking empty. A
    contact that the directory does not give (deleted, not published) is not
    in `contacts`, as on the site."""
    uids = list(section.related_contacts or [])
    if not uids:
        return {"contact_uids": [], "contacts": []}
    found = {
        contact.get("UID"): contact
        for contact in directory_json(get_contacts_search_url(uids)).get("items", [])
    }
    visible_blocks = set(section.visible_blocks or [])
    contacts = [
        contact_details(section, found[uid], visible_blocks)
        for uid in uids
        if uid in found
    ]
    return {"contact_uids": uids, "contacts": contacts}


def contact_details(section, contact, visible_blocks):
    """What the contact section shows of a directory contact (see
    contents/sections/contact/macros.pt). A block that the editor did not make
    visible gives null or [], even when the directory has the data."""
    details = {
        "uid": contact.get("UID"),
        "title": None,
        "subtitle": None,
        "vat_number": None,
        "phones": [],
        "emails": [],
        "urls": [],
        "address": None,
        "itinerary_url": None,
        "schedule": None,
        "location": None,
        "description": None,
        "logo_url": None,
        "image_url": None,
        "images": [],
    }
    properties = ContactProperties(contact, section)
    if "titles" in visible_blocks:
        details["title"] = contact.get("title") or None
        details["subtitle"] = contact.get("subtitle") or None
    if "contact_informations" in visible_blocks:
        details["vat_number"] = contact.get("vat_number") or None
        details["phones"] = contact_phones(contact)
        details["emails"] = contact_emails(contact)
        details["urls"] = contact_urls(properties)
    if "address" in visible_blocks:
        details["address"] = contact_address(properties)
    if "itinerary" in visible_blocks:
        details["itinerary_url"] = properties.get_itinerary_link()
    if "schedule" in visible_blocks and not properties.is_empty_schedule():
        details["schedule"] = contact_schedule(contact)
    geolocation = contact.get("geolocation")
    if "map" in visible_blocks and contact.get("is_geolocated") and geolocation:
        details["location"] = {
            "latitude": geolocation.get("latitude"),
            "longitude": geolocation.get("longitude"),
        }
    if "description" in visible_blocks:
        details["description"] = contact.get("description") or None
    if "logo" in visible_blocks and contact.get("logo"):
        details["logo_url"] = f"{contact['@id']}/@@images/logo"
    if "leadimage" in visible_blocks and contact.get("image"):
        details["image_url"] = f"{contact['@id']}/@@images/image"
    if "gallery" in visible_blocks:
        details["images"] = contact_images(contact)
    return details


def contact_phones(contact):
    return [
        {
            "label": phone.get("label") or None,
            "type": phone.get("type") or None,
            "number": phone.get("number"),
        }
        for phone in contact.get("phones") or []
        if phone.get("number")
    ]


def contact_emails(contact):
    return [
        {
            "label": mail.get("label") or None,
            "type": mail.get("type") or None,
            "address": mail.get("mail_address"),
        }
        for mail in contact.get("mails") or []
        if mail.get("mail_address")
    ]


def contact_urls(properties):
    # get_urls drops the empty rows, as the template does
    return [
        {"type": url.get("type") or None, "url": url.get("url")}
        for url in properties.get_urls or []
        if url.get("url")
    ]


def contact_address(properties):
    address = properties.formatted_address()
    if address is None:
        return None
    return {
        "street": address["street"] or None,
        "locality": address["entity"] or None,
        "country": address["country"] or None,
    }


WEEK_DAYS = (
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
)


def contact_schedule(contact):
    """The opening hours as the editor entered them.

    The site shows the next 7 days from today, with the special periods and
    the closures applied, and an "open now" message: that changes every day.
    The stored, regular data is given instead, with the same formatting of
    the hours (formatted_schedule)."""
    return {
        "days": schedule_days(contact.get("schedule") or {}),
        "periods": [
            {
                "dates": [
                    {"start": dates.get("start_date"), "end": dates.get("end_date")}
                    for dates in period.get("dates")
                ],
                "days": schedule_days(period.get("schedule") or {}),
            }
            for period in contact.get("multi_schedule") or []
            if period.get("dates")
        ],
        "closures": [
            {"date": closure.get("date"), "title": closure.get("title") or None}
            for closure in contact.get("exceptional_closure") or []
        ],
    }


def schedule_days(schedule):
    return [
        {"day": day, "hours": formatted_schedule(schedule[day])}
        for day in WEEK_DAYS
        if day in schedule
    ]


def contact_images(contact):
    # the same search as ContactProperties.images: the images of a contact are
    # not in the first response (its "items" are cut to b_size)
    url = f"{contact['@id']}/@search?portal_type=Image&path.depth=1"
    return [
        {
            "url": f"{image['@id']}/@@images/image",
            "title": image.get("title") or None,
            "description": image.get("description") or None,
        }
        for image in directory_json(url).get("items", [])
    ]


def directory_json(url):
    """JSON of an imio.directory request, as an anonymous visitor gets it.

    Unlike utils.get_json, which gives None for every problem, errors raise:
    the caller must know that the data is missing."""
    language = api.portal.get_current_language()
    response = requests.get(
        url,
        headers={"Accept": "application/json", "Cookie": f"I18N_LANGUAGE={language}"},
        timeout=DIRECTORY_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def serialize_collection(page, section):
    return linked_view(section, section.collection)


def serialize_linked_rest_view(page, section):
    return linked_view(section, section.linking_rest_view)


def serialize_timestamped_publications(page, section):
    # resolved by Prefect against iA.Delib, never from here. The registry
    # record holds the URL of the institution in iA.Delib (its "@id").
    source_url = api.portal.get_registry_record(
        "smartweb.iadeliberations_institution", default=None
    )
    return {
        "publication_uids": list(section.related_timestamped_publications or []),
        "publications_source_url": source_url or None,
    }


def linked_view(section, relation):
    obj = visible_object(relation)
    return {
        "link_text": section.link_text or None,
        "url": obj.absolute_url() if obj is not None else None,
    }


def visible_object(relation):
    """Target of a relation, if it exists and the user can view it.
    RelationValue.to_object does not check permissions."""
    obj = relation.to_object if relation is not None else None
    if obj is None or not api.user.has_permission("View", obj=obj):
        return None
    return obj


def page_base_url(page):
    # a page is folderish: Plone renders it with <base href="{page_url}/">
    return f"{page.absolute_url()}/"


def link_url(context, value):
    """Absolute URL of a link field value, or None when it cannot be followed
    (deleted or not viewable target, forbidden scheme)"""
    url = replace_link_variables_by_paths(context, value or "")
    url = resolve_internal_url(url)
    if not url:
        return None
    url = urljoin(f"{api.portal.get().absolute_url()}/", url)
    return url if scheme(url) in LINK_SCHEMES else None


def resolve_internal_url(url):
    """URL of the target of a resolveuid link, or None when the target is
    deleted or not viewable. Other URLs are returned unchanged.

    plone.restapi resolve_uid and plone.outputfilters search the catalog
    unrestrictedly: they would give the URL of a private content."""
    match = RESOLVEUID_RE.match(url)
    if match is None:
        return url
    uid, suffix = match.groups()
    brains = api.content.find(UID=uid)
    if len(brains) != 1:
        return None
    return brains[0].getURL() + (suffix or "")


def scheme(url):
    return urlparse(url).scheme.lower()


def clean_html(value, base_url):
    """HTML without active code, with absolute URLs, and the iframes it held.

    Returns (html, iframes). Iframes are taken out of the HTML: a Markdown
    document cannot hold them, Prefect renders them from `iframes`.
    """
    if not value or not value.strip():
        return None, []
    root = lxml_html.fragment_fromstring(value, create_parent="div")
    root.make_links_absolute(
        base_url, resolve_base_href=False, handle_failures="discard"
    )
    iframes = []
    for iframe in list(root.iter("iframe")):
        src = resolve_internal_url(iframe.get("src") or "")
        if src and scheme(src) in HTTP_SCHEMES:
            iframes.append({"url": src, "title": iframe.get("title") or None})
        iframe.drop_tree()
    for img in list(root.iter("img")):
        src = resolve_internal_url(img.get("src") or "")
        if src is None or scheme(src) not in HTTP_SCHEMES:
            img.drop_tree()
        else:
            img.set("src", src)
    for link in list(root.iter("a")):
        if link.get("href") is None:
            continue
        href = resolve_internal_url(link.get("href"))
        if href is None or scheme(href) not in LINK_SCHEMES:
            # deleted or private target, or forbidden scheme: keep the text
            link.drop_tag()
        else:
            link.set("href", href)
    CLEANER(root)
    # strip the "<div>" "</div>" created above, as PortalTransforms does
    html = lxml_html.tostring(root, encoding="unicode")[5:-6].strip()
    return html or None, iframes


SECTIONS = {
    "imio.smartweb.SectionText": ("text", serialize_text),
    "imio.smartweb.SectionHTML": ("html", serialize_html),
    "imio.smartweb.SectionLinks": ("links", serialize_links),
    "imio.smartweb.SectionGallery": ("gallery", serialize_gallery),
    "imio.smartweb.SectionFiles": ("files", serialize_files),
    "imio.smartweb.SectionVideo": ("video", serialize_video),
    "imio.smartweb.SectionMap": ("map", serialize_map),
    "imio.smartweb.SectionPostit": ("postit", serialize_postit),
    "imio.smartweb.SectionSelections": ("selections", serialize_selections),
    "imio.smartweb.SectionExternalContent": (
        "external_content",
        serialize_external_content,
    ),
    "imio.smartweb.SectionContact": ("contact", serialize_contact),
    "imio.smartweb.SectionCollection": ("collection", serialize_collection),
    "imio.smartweb.SectionEvents": ("events", serialize_linked_rest_view),
    "imio.smartweb.SectionNews": ("news", serialize_linked_rest_view),
    "imio.smartweb.SectionTimestampedPublications": (
        "timestamped_publications",
        serialize_timestamped_publications,
    ),
}
