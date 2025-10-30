from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import pkg_resources


class AccessibilityInfo(BrowserView):
    hide_herobanner = True
    index = ViewPageTemplateFile(
        pkg_resources.resource_filename(
            "Products.CMFPlone", "browser/templates/accessibility-info.pt"
        )
    )

    def __call__(self):
        return self.index()
