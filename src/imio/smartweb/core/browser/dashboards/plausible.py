from plone import api
from Products.Five.browser import BrowserView
import os
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from imio.smartweb.core.browser.utils import get_plausible_vars


class PlausibleView(BrowserView):
    index = ViewPageTemplateFile("plausible.pt")

    def __call__(self):
        return self.index()

    @property
    def is_plausible_set(self):
        if not get_plausible_vars(self):
            return False
        else:
            return True

    @property
    def get_embedhostjs_src(self):
        vars = get_plausible_vars(self)
        return f"https://{vars['plausible_url']}/js/embed.host.js"

    @property
    def get_iframe_src(self):
        vars = get_plausible_vars(self)
        return f"https://{vars['plausible_url']}/share/{vars['plausible_site']}?auth={vars['plausible_token']}&embed=true&theme=light&background=transparent"
