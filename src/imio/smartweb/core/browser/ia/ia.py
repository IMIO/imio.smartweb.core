from imio.smartweb.common.config import IPA_URL
from imio.smartweb.common.utils import get_vocabulary
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import ISectionText
from imio.smartweb.core.utils import get_categories
from plone import api
from Products.Five import BrowserView
from zope.i18n import translate

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


class ProcessCategorizeContentView(BrowserView):

    def __init__(self, context, request):
        self.current_lang = api.portal.get_current_language()[:2]
        self.context = context
        self.request = request
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def _get_structured_data_from_vocabulary(self, vocabulary_name):

        voc = get_vocabulary(vocabulary_name)
        voc_translated_dict = [
            {
                "title": translate(t.title, target_language=self.current_lang),
                "token": t.token,
            }
            for t in voc
        ]
        return voc_translated_dict

    def _ask_categorization_to_ia(self, text, voc):
        payload = {"input": text, "vocabulary": voc, "unique": False}
        url = f"{IPA_URL}/categorize-content"
        response = requests.post(url, headers=self.headers, json=payload)
        data = response.json()
        return data

    def __call__(self):
        results = {}

        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )
        all_text = ""
        if IPages.providedBy(self.context):
            for item in self.context.objectItems():
                obj = item[1]
                if ISectionText.providedBy(obj):
                    all_text += obj.text.output or ""

        categories_taxo = get_categories()
        categories_voca = categories_taxo.makeVocabulary(self.current_lang).inv_data
        categories_voc = [{"title": v, "token": k} for k, v in categories_voca.items()]
        data = self._ask_categorization_to_ia(all_text, categories_voc)
        if not data:
            return ""
        results["form-widgets-page_category-taxonomy_page_category"] = [
            {"title": r.get("title"), "token": r.get("token")}
            for r in data.get("result")
        ]

        iam_voc = self._get_structured_data_from_vocabulary(
            "imio.smartweb.vocabulary.IAm"
        )
        data = self._ask_categorization_to_ia(all_text, iam_voc)
        if not data:
            return ""
        results["form-widgets-IAm-iam"] = [
            {"title": r.get("title"), "token": r.get("token")}
            for r in data.get("result")
        ]

        topics_voc = self._get_structured_data_from_vocabulary(
            "imio.smartweb.vocabulary.Topics"
        )
        data = self._ask_categorization_to_ia(all_text, topics_voc)
        if not data:
            return ""
        results["form-widgets-ITopics-topics"] = [
            {"title": r.get("title"), "token": r.get("token")}
            for r in data.get("result")
        ]

        return json.dumps(
            {
                "ok": True,
                "message": "Catégorisation calculée",
                "data": results,
            }
        )
