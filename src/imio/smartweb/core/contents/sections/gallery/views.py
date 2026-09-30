# -*- coding: utf-8 -*-

from plone.gallery.views.photo_gallery import PhotoGallery
from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.common.ia.browser.views import BaseIAView
from imio.smartweb.common.ia.browser.views import get_image_file
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.protect import CheckAuthenticator
from zope.lifecycleevent import modified

import logging

logger = logging.getLogger("imio.smartweb.core")


class GalleryView(SectionView, PhotoGallery):
    """Gallery Section view"""

    def get_scale_url(self, item, scale, orientation="paysage"):
        request = self.request
        return get_scale_url(item, request, "image", scale, orientation)

    def alt_label(self, item):
        title = item.title or ""
        description = item.description or ""
        # Accessibility: if title is the same as the filename, return empty string because, filename is not a good practice in alt tag for an img.
        if item.image and title == item.image.filename and len(description) == 0:
            title = ""
        # Accessibility : Return description if longer is same or greater than title.
        if len(description) >= len(title):
            return description
        return title


class GenerateImagesDescriptionView(SectionView, BaseIAView):
    """Fill the empty description of the gallery images with the description
    deduced by Omnia (deduce-metadata agent) from each image.
    Images that already have a description are left untouched."""

    def __call__(self):
        CheckAuthenticator(self.request)
        done = failed = 0
        for image in self.context.listFolderContents(
            contentFilter={"portal_type": "Image"}
        ):
            if (image.description or "").strip():
                continue
            if not api.user.has_permission("Modify portal content", obj=image):
                continue
            image_file = get_image_file(image)
            if image_file is None:
                continue
            try:
                data = self.ia_service.deduce_metadata(image_file=image_file)
            except Exception:
                logger.warning(
                    "Could not deduce metadata for %s",
                    image.absolute_url(),
                    exc_info=True,
                )
                failed += 1
                continue
            description = self._clean_description((data or {}).get("description"))
            if not description:
                failed += 1
                continue
            image.description = description
            modified(image)
            done += 1
        api.portal.show_message(
            _(
                "${done} image description(s) generated.",
                mapping={"done": done},
            ),
            self.request,
        )
        if failed:
            api.portal.show_message(
                _(
                    "${failed} image description(s) could not be generated.",
                    mapping={"failed": failed},
                ),
                self.request,
                type="warning",
            )
        self.redirect_to_section(self.context.id)

    @staticmethod
    def _clean_description(text):
        text = " ".join((text or "").split())
        if len(text) > DESCRIPTION_MAX_LENGTH:
            text = text[:DESCRIPTION_MAX_LENGTH].rsplit(" ", 1)[0]
        return text
