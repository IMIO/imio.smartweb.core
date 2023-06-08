from plone import api
from Products.Five.browser import BrowserView
import os
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PlausibleView(BrowserView):
    index = ViewPageTemplateFile("plausible.pt")

    def __call__(self):
        return self.index()

    @property
    def src_iframe(self):
        env_plausible_url = os.getenv("SMARTWEB_PLAUSIBLE_URL")
        env_plausible_site = os.getenv("SMARTWEB_PLAUSIBLE_SITE")
        env_plausible_token = os.getenv("SMARTWEB_PLAUSIBLE_TOKEN")

        plausible_url = (
            env_plausible_url
            if (env_plausible_url and env_plausible_url != "")
            else api.portal.get_registry_record("smartweb.plausible_url")
        )
        plausible_site = (
            env_plausible_site
            if (env_plausible_site and env_plausible_site != "")
            else api.portal.get_registry_record("smartweb.plausible_site")
        )
        plausible_token = (
            env_plausible_token
            if (env_plausible_token and env_plausible_token != "")
            else api.portal.get_registry_record("smartweb.plausible_token")
        )

        return f"https://{plausible_url}/share/{plausible_site}?auth={plausible_token}&embed=true&theme=light&background=transparent"
