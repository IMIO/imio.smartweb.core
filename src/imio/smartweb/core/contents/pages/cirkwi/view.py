# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

import logging
import requests

logger = logging.getLogger("imio.smartweb.core")


class CirkwiViewView(BrowserView):
    cirwki_api_uri = "https://www.modulesbox.com/fr/api/module/"

    def get_cirkwi_html(self):
        cirkwi_widget_id = self.context.cirkwi_widget_id
        cirkwi_widget_mb_key = self.context.cirkwi_widget_mb_key
        url = f"{self.cirwki_api_uri}{cirkwi_widget_id}?mb_key={cirkwi_widget_mb_key}&{self.request.get('QUERY_STRING')}"
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException:
            # Don't log the URL: it carries the widget's mb_key.
            logger.warning(f"Cirkwi request failed for widget {cirkwi_widget_id}")
            return 504
        if response.status_code != 200:
            return response.status_code
        return response.text
