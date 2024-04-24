# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

import requests


class CirkwiViewView(BrowserView):
    cirwki_api_uri = "https://www.modulesbox.com/fr/api/module/"

    def get_cirkwi_html(self):
        cirkwi_widget_id = self.context.cirkwi_widget_id
        cirkwi_widget_mb_key = self.context.cirkwi_widget_mb_key
        url = f"{self.cirwki_api_uri}{cirkwi_widget_id}?mb_key={cirkwi_widget_mb_key}&{self.request.get('QUERY_STRING')}"
        response = requests.get(url)
        if response.status_code != 200:
            return response.status_code
        return response.text
