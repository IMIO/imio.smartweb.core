# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.procedure.utils import sign_url
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
import json
import requests


class PageSectionsVocabularyFactory:
    def __call__(self, context=None):
        values = [
            ("title", _(u"Title")),
            ("description", _(u"Description")),
            ("body", _(u"Body text")),
            ("leadimage", _(u"Lead Image")),
            ("images", _(u"Images thumbnails")),
            ("files", _(u"Files")),
        ]
        terms = [
            SimpleVocabulary.createTerm(value[0], value[0], value[1])
            for value in values
        ]
        return SimpleVocabulary(terms)


PageSectionsVocabulary = PageSectionsVocabularyFactory()


class RemoteProceduresVocabularyFactory:
    def __call__(self, context=None):
        # sample : "https://olln-formulaires.guichet-citoyen.be/api/formdefs/"
        url = api.portal.get_registry_record("smartweb.url_formdefs_api")
        # sample : "568DGess2x8j8twv7x2Y2MApjn789xfG7jM27r399q4xSD27Jz"
        key = api.portal.get_registry_record("smartweb.secret_key_api")
        orig = "ia.smartweb"
        if not url:
            return SimpleVocabulary([])
        query_full = sign_url(url, key, orig)
        try:
            response = requests.get(query_full)
        except Exception:
            return SimpleVocabulary([])

        if response.status_code != 200:
            return SimpleVocabulary([])

        json_procedures = json.loads(response.text)
        return SimpleVocabulary(
            [
                SimpleTerm(value=elem["url"], title=elem["title"])
                for elem in json_procedures.get("data", [])
            ]
        )


RemoteProceduresVocabulary = RemoteProceduresVocabularyFactory()
