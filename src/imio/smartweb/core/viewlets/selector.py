# -*- coding: utf-8 -*-

from plone import api
from plone.app.multilingual.browser.selector import (
    LanguageSelectorViewlet as BaseLanguageSelectorViewlet,
)


class LanguageSelectorViewlet(BaseLanguageSelectorViewlet):
    """Language selector that renders either as a Bootstrap dropdown (current
    language first) or as the classic flat list, depending on the
    'smartweb.language_selector_dropdown' control panel setting."""

    @property
    def use_dropdown(self):
        return api.portal.get_registry_record(
            "smartweb.language_selector_dropdown", default=False
        )
