# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.folder.interfaces import IExplicitOrdering
from plone.namedfile.file import NamedBlobImage
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from urllib.parse import unquote
from urllib.parse import urlparse
from zope.interface import alsoProvides

import logging
import os
import re
import requests
import transaction

_IMG_RE = re.compile(r'<img\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?/?>', re.IGNORECASE)
_RESOLVEUID_RE = re.compile(r"resolveuid/([^/?\"'#\s]+)", re.IGNORECASE)
_REQUEST_TIMEOUT = 10  # seconds per HTTP request
_USER_AGENT = "imio.smartweb.core/sectiontext-image-migration (internal)"

logger = logging.getLogger("imio.smartweb.core")


def _iter_img_tags(raw_html):
    """Return each full <img …> tag substring found in *raw_html*.

    Works on the raw stored HTML so the exact substring can later be removed
    without reserialising (and thus altering) the rest of the HTML.
    """
    if not raw_html:
        return []
    return _IMG_RE.findall(raw_html)


def _extract_attr(tag, name):
    """Return the value of attribute *name* in an HTML *tag* substring, or ""."""
    match = re.search(
        r'(?<![\w\-])%s\s*=\s*"([^"]*)"|(?<![\w\-])%s\s*=\s*\'([^\']*)\''
        % (re.escape(name), re.escape(name)),
        tag,
        re.IGNORECASE,
    )
    if not match:
        return ""
    return match.group(1) if match.group(1) is not None else match.group(2)


def _classify_src(src, portal_url):
    """Classify an <img> src attribute. Returns a (kind, value) tuple:

    - ("resolveuid", uid)      internal Plone image referenced by UID
    - ("external", url)        http(s) URL hosted outside this portal
    - ("unsupported", reason)  data-URI, relative path, same portal, empty
    """
    src = (src or "").strip()
    if not src:
        return ("unsupported", "src vide")
    uid_match = _RESOLVEUID_RE.search(src)
    if uid_match:
        return ("resolveuid", uid_match.group(1))
    lower = src.lower()
    if lower.startswith(("http://", "https://")):
        if portal_url and src.startswith(portal_url):
            return ("unsupported", "image sur le même portail")
        return ("external", src)
    if lower.startswith("data:"):
        return ("unsupported", "data-URI")
    return ("unsupported", "chemin relatif ou non reconnu")


def _resolve_uid_image(uid):
    """Return the Image object referenced by *uid*, or None if it does not
    exist or is not an Image content type."""
    brains = api.content.find(UID=uid)
    if not brains:
        return None
    obj = brains[0].getObject()
    if obj.portal_type != "Image":
        return None
    return obj


def _filename_from_url(url):
    """Derive a filename from an external image URL (defaults to "image")."""
    path = urlparse(url).path
    return unquote(os.path.basename(path)) or "image"


def _download_external_image(url, cache):
    """Download an external image. Returns (data, filename, content_type, error)
    where error is None on success. Memoised in *cache*."""
    if url in cache:
        return cache[url]
    headers = {"User-Agent": _USER_AGENT}
    try:
        resp = requests.get(
            url, allow_redirects=True, timeout=_REQUEST_TIMEOUT, headers=headers
        )
        if resp.status_code >= 400:
            result = (None, None, None, "HTTP {}".format(resp.status_code))
        else:
            content_type = resp.headers.get("Content-Type", "").split(";")[0].strip()
            result = (
                resp.content,
                _filename_from_url(url),
                content_type or None,
                None,
            )
    except requests.exceptions.Timeout:
        result = (None, None, None, "Timeout")
    except requests.exceptions.SSLError as exc:
        result = (None, None, None, "SSL error: {}".format(str(exc)[:80]))
    except requests.exceptions.ConnectionError as exc:
        result = (None, None, None, "Connection error: {}".format(str(exc)[:80]))
    except Exception as exc:
        result = (None, None, None, "Unexpected error: {}".format(str(exc)[:80]))
    cache[url] = result
    return result


class MigrateSectionTextImagesView(BrowserView):
    """Find every imio.smartweb.SectionText whose rich text contains inline
    <img> tags, move those images into a imio.smartweb.SectionGallery created
    right after the SectionText in the parent page, and strip the migrated
    <img> tags from the rich text. Dry-run by default; ?apply=1 applies."""

    def __call__(self):
        self.apply = bool(self.request.form.get("apply"))
        if self.apply:
            alsoProvides(self.request, IDisableCSRFProtection)
        self.results = []
        self._download_cache = {}
        self._portal_url = api.portal.get().absolute_url()

        for brain in api.content.find(portal_type="imio.smartweb.SectionText"):
            self._process_section(brain.getObject())

        self.summary = self._compute_summary()
        return self.index()

    def _compute_summary(self):
        statuses = {}
        galleries = 0
        for entry in self.results:
            if entry["gallery_created"]:
                galleries += 1
            for img in entry["images"]:
                statuses[img["status"]] = statuses.get(img["status"], 0) + 1
        return {
            "sections": len(self.results),
            "galleries": galleries,
            "statuses": statuses,
        }

    def _process_section(self, obj):
        richtext = getattr(obj, "text", None)
        raw = getattr(richtext, "raw", None) if richtext is not None else None
        if not raw:
            return
        tags = _iter_img_tags(raw)
        if not tags:
            return

        images = []  # report rows, one per <img> tag
        to_migrate = []  # (tag, kind, value, alt, row, resolved) for migratable images
        for tag in tags:
            src = _extract_attr(tag, "src")
            alt = _extract_attr(tag, "alt")
            kind, value = _classify_src(src, self._portal_url)
            row = {
                "src": src,
                "alt": alt,
                "kind": kind,
                "value": value,
                "status": None,
                "reason": "",
            }
            if kind == "unsupported":
                row["status"] = "skipped"
                row["reason"] = value
            elif kind == "resolveuid":
                resolved = _resolve_uid_image(value)
                if resolved is None:
                    row["status"] = "failed"
                    row["reason"] = "Image resolveuid introuvable"
                else:
                    row["status"] = "to_migrate"
                    to_migrate.append((tag, kind, value, alt, row, resolved))
            else:  # external
                row["status"] = "to_migrate"
                to_migrate.append((tag, kind, value, alt, row, None))
            images.append(row)

        entry = {
            "section_url": obj.absolute_url(),
            "section_path": "/".join(obj.getPhysicalPath()),
            "parent_path": "/".join(aq_parent(obj).getPhysicalPath()),
            "gallery_title": "Galerie — {}".format(obj.title or obj.getId()),
            "gallery_created": False,
            "position_note": "",
            "error": "",
            "images": images,
        }

        if self.apply and to_migrate:
            self._apply_section(obj, raw, entry, to_migrate)

        self.results.append(entry)

    def _apply_section(self, obj, raw, entry, to_migrate):
        sp = transaction.savepoint(optimistic=True)
        try:
            self._migrate_images(obj, raw, entry, to_migrate)
        except Exception as exc:
            sp.rollback()
            entry["gallery_created"] = False
            entry["error"] = "section annulée: {}".format(str(exc)[:120])
            for tag, kind, value, alt, row, resolved in to_migrate:
                if row["status"] == "migrated":
                    row["status"] = "failed"
                    row["reason"] = "rollback de la section"
            logger.warning("Migration annulée pour %s: %s", obj.absolute_url(), exc)

    def _migrate_images(self, obj, raw, entry, to_migrate):
        parent = aq_parent(obj)
        gallery = None
        new_raw = raw
        for tag, kind, value, alt, row, resolved in to_migrate:
            try:
                if kind == "resolveuid":
                    if gallery is None:
                        gallery = self._create_gallery(parent, obj, entry)
                    api.content.copy(source=resolved, target=gallery)
                else:  # external
                    data, filename, content_type, error = _download_external_image(
                        value, self._download_cache
                    )
                    if error:
                        row["status"] = "failed"
                        row["reason"] = error
                        continue
                    if gallery is None:
                        gallery = self._create_gallery(parent, obj, entry)
                    new_image = api.content.create(
                        container=gallery, type="Image", title=alt or filename
                    )
                    new_image.image = NamedBlobImage(
                        data=data, filename=filename, contentType=content_type
                    )
            except Exception as exc:
                logger.warning("Echec migration image %s: %s", value, exc)
                row["status"] = "failed"
                row["reason"] = str(exc)[:120]
                continue
            row["status"] = "migrated"
            new_raw = new_raw.replace(tag, "", 1)

        if new_raw != raw:
            richtext = obj.text
            obj.text = RichTextValue(
                new_raw,
                mimeType=richtext.mimeType,
                outputMimeType=richtext.outputMimeType,
                encoding=richtext.encoding,
            )
            obj.reindexObject()

    def _create_gallery(self, parent, section, entry):
        gallery = api.content.create(
            container=parent,
            type="imio.smartweb.SectionGallery",
            title=entry["gallery_title"],
        )
        entry["gallery_created"] = True
        self._position_after(parent, section, gallery, entry)
        return gallery

    def _position_after(self, parent, section, gallery, entry):
        try:
            ordering = IExplicitOrdering(parent)
            position = ordering.getObjectPosition(section.getId()) + 1
            ordering.moveObjectToPosition(gallery.getId(), position)
        except Exception as exc:
            entry["position_note"] = "non repositionnée: {}".format(str(exc)[:80])
