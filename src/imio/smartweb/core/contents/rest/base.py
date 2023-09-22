# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import get_json
from plone import api
from plone.rest import Service

import json


class BaseEndpoint(object):
    language = "fr"
    remote_endpoint = ""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        results = get_json(self.query_url)
        return results

    @property
    def query_url(self):
        raise NotImplementedError

    def convert_cached_image_scales(
        self,
        item,
        modified_hash,
        field="image",
        scales=["vignette", "affiche"],
        orientation="paysage",
    ):
        """Remove image from result dict and add generated image scales URLs
        with cache key"""
        for scale in scales:
            scale_name = "_".join(filter(None, [orientation, scale]))
            cached_scale_url = (
                f"{item['@id']}/@@images/{field}/{scale_name}?cache_key={modified_hash}"
            )
            item[f"{field}_{scale}_scale"] = cached_scale_url
        item[
            f"{field}_full_scale"
        ] = f"{item['@id']}/@@images/{field}/?cache_key={modified_hash}"
        del item[field]

    def get_extra_params(self, params):
        form = self.request.form
        extra_params = []
        for k, v in form.items():
            if isinstance(v, list):
                # handles multiple metadata_fields
                for value in v:
                    extra_params.append("{}={}".format(k, value))
            else:
                extra_params.append("{}={}".format(k, v))
        current_lang = api.portal.get_current_language()[:2]
        if current_lang != "fr":
            extra_params.append("translated_in_{}=1".format(current_lang))
        params = params + extra_params
        return params


class BaseService(Service):
    def render(self):
        response = self.request.response
        response.setHeader("Content-type", "application/json")
        content = self.reply()
        return json.dumps(
            content,
            indent=2,
            separators=(", ", ": "),
        )
