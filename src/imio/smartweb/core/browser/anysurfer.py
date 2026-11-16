from importlib.resources import files
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AccessibilityInfo(BrowserView):
    hide_herobanner = True
    index = ViewPageTemplateFile(
        str(files("Products.CMFPlone") / "browser/templates/accessibility-info.pt")
    )

    def __call__(self):
        return self.index()
