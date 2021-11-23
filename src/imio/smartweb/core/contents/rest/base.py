# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import get_json
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
