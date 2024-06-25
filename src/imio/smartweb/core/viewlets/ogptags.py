# -*- coding: utf-8 -*-

from imio.smartweb.core.config import DIRECTORY_URL
from imio.smartweb.core.config import EVENTS_URL
from imio.smartweb.core.config import NEWS_URL
from imio.smartweb.core.contents import IDirectoryView
from imio.smartweb.core.contents import IEventsView
from imio.smartweb.core.contents import INewsView
from imio.smartweb.core.utils import get_json
from imio.smartweb.core.utils import get_wca_token
from imio.smartweb.core.utils import hash_md5
from plone import api
from plone.app.layout.viewlets.httpheaders import HeaderViewlet

import os


class OgpTagsViewlet(HeaderViewlet):
    _item = None
    _image = None
    _default_scale = "paysage_vignette"

    def update(self):
        if not self.request.form.get("u", None):
            # We are on the view
            self.set_ogp_informations_for_view()
        else:
            # We are on an item
            self.set_ogp_informations_for_item()
        super(OgpTagsViewlet, self).update()

    def set_ogp_informations_for_view(self):
        self._item = {
            "title": self.context.Title,
            "description": self.context.description,
            "url": self.context.absolute_url(),
        }
        dict_image = None
        image = self.context.image
        if image is not None:
            modified_hash = hash_md5(str(self.context.modified()))
            url = f"{self.context.absolute_url()}/@@images/image/paysage_vignette?cache_key={modified_hash}"
            dict_image = {
                "download": url,
                "filename": image.filename,
                "content-type": image.contentType,
                "scales": {
                    self._default_scale: {
                        "width": image.getImageSize()[0],
                        "height": image.getImageSize()[1],
                    }
                },
            }
        self._item["image"] = dict_image
        self._set_image()

    def set_ogp_informations_for_item(self):
        uid = self.request.form["u"]
        auth_source_url = ""
        endpoint = "@search"
        if IDirectoryView.providedBy(self.context):
            params = "fullobjects=1"
            auth_source_url = DIRECTORY_URL
            client_id = os.environ.get("RESTAPI_DIRECTORY_CLIENT_ID")
            client_secret = os.environ.get("RESTAPI_DIRECTORY_CLIENT_SECRET")
        elif IEventsView.providedBy(self.context):
            params = """metadata_fields=category&
            metadata_fields=local_category&
            metadata_fields=container_uid&
            metadata_fields=topics&
            metadata_fields=start&
            metadata_fields=end&
            metadata_fields=has_leadimage&
            metadata_fields=UID&
            fullobjects=1"""
            auth_source_url = EVENTS_URL
            endpoint = "@events"
            client_id = os.environ.get("RESTAPI_EVENTS_CLIENT_ID")
            client_secret = os.environ.get("RESTAPI_EVENTS_CLIENT_SECRET")
        elif INewsView.providedBy(self.context):
            params = "fullobjects=1"
            auth_source_url = NEWS_URL
            client_id = os.environ.get("RESTAPI_NEWS_CLIENT_ID")
            client_secret = os.environ.get("RESTAPI_NEWS_CLIENT_SECRET")
        auth = get_wca_token(client_id, client_secret)
        auth_source_url = f"{auth_source_url}/{endpoint}?UID={uid}&{params}"
        result_json = get_json(auth_source_url, auth=None)
        if result_json:
            self._item = result_json["items"][0]
            self._set_image()

    def _set_image(self):
        if not self._item or not self._item.get("image", None):
            return None
        self._image = self._item.get("image")

    @property
    def image(self):
        return {} if not self._image else self._image

    @property
    def image_url(self):
        return self.scale(self._default_scale).get("download", "") or self.image.get(
            "download", ""
        )

    def scale(self, scale="paysage_vignette"):
        return self.image.get("scales", {}).get(scale, {})

    @property
    def title(self):
        if not self._item:
            return ""
        return self._item.get("title", "")

    @property
    def description(self):
        if not self._item:
            return ""
        return self._item.get("description", "")

    @property
    def url(self):
        if not self._item:
            return ""
        try:
            url = f'{self.request.ACTUAL_URL}?u={self.request.form["u"]}'
        except Exception:
            url = self.request.URL
        return url

    @property
    def site_name(self):
        return api.portal.get().title

    @property
    def image_type(self):
        return self.image.get("content-type", "")

    @property
    def image_width(self):
        return self.scale().get("width", "")

    @property
    def image_height(self):
        return self.scale().get("height")

    @property
    def image_alt(self):
        if not self.image:
            return ""
        return ""
