# # -*- coding: utf-8 -*-

from plone import api
from plone.app.multilingual import api as api_lng
from Products.Five.browser import BrowserView


def get_translation(obj, lang):
    if not api_lng.is_translatable(obj):
        return None
    translation_manager = api_lng.get_translation_manager(obj)
    translated_obj = translation_manager.get_translation(lang)
    return translated_obj


class RestViewBaseView(BrowserView):

    def get_rest_view_object(self):
        rest_view_uid = api.portal.get_registry_record(self.registry_key, default=None)
        if rest_view_uid is None:
            return None
        brains = api.content.find(UID=rest_view_uid)
        if brains:
            return brains[0].getObject()
        return None

    def __call__(self):
        language = self.request.form.get("language", "fr")
        default_language = api.portal.get_default_language()
        rest_view_obj = self.get_rest_view_object()
        if rest_view_obj is None:
            self.request.response.redirect(api.portal.get().absolute_url())
            return ""
        if default_language != language:
            translated_obj = get_translation(rest_view_obj, language)
            if translated_obj is not None:
                rest_view_obj = translated_obj
        rest_view_url = rest_view_obj.absolute_url()
        self.request.response.redirect(rest_view_url)
        return ""


class DirectoryView(RestViewBaseView):
    registry_key = "smartweb.default_directory_view"


class EventsView(RestViewBaseView):
    registry_key = "smartweb.default_events_view"


class NewsView(RestViewBaseView):
    registry_key = "smartweb.default_news_view"
