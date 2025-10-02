from imio.smartweb.common.config import IPA_URL
from Products.Five import BrowserView

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
        url = f"{IPA_URL}/suggest-titles"
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            return current_html
        data = response.json()
        if not data:
            return current_html
        return json.dumps(data)