# -*- coding: utf-8 -*-

import requests


class BaseEndpoint(object):

    language = "fr"
    remote_endpoint = ""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        results = self.getResult()
        return results

    @property
    def query_url(self):
        raise NotImplementedError

    def getResult(self):
        headers = {"Accept": "application/json"}
        result = requests.get(self.query_url, headers=headers)
        return result.json()

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
