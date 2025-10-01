# browser/slugify.py
from Products.Five import BrowserView
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility

import json
import requests


class ProcessSuggestedTitlesView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def __call__(self):
        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )
        current_html = self.request.form.get("text", "")
        payload = {
            "input": current_html,
            "expansion_target": 50,
        }
        url = "http://127.0.0.1:8000/common/suggest-titles"
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            return current_html
        data = response.json()
        if not data:
            return current_html
        return json.dumps(data)

        # titles = data.get("suggested_titles", [])
        # new_html = "<ul>{}</ul>".format("".join(f"<li>{t}</li>" for t in titles))
        # return json.dumps({"html": f"{new_html}<br />{current_html}"})
        # text = self.request.form.get("text", "")
        # normalizer = getUtility(IIDNormalizer)
        # value = normalizer.normalize(text)
        # self.request.response.setHeader("Content-Type", "application/json")
        # return json.dumps({"value": value})
