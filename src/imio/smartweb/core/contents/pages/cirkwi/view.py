# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

import requests


class CirkwiViewView(BrowserView):
    cirwki_api_uri = "https://www.modulesbox.com/fr/api/module/"

    def get_cirkwi_html(self):
        cirkwi_widget_id = self.context.cirkwi_widget_id
        url = f"{self.cirwki_api_uri}{cirkwi_widget_id}"
        response = requests.get(url)
        if response.status_code != 200:
            return response.status_code
        return response.text
