# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.httpheaders import HeaderViewlet


class ArcgisHeaderViewlet(HeaderViewlet):
    def update(self):
        super(ArcgisHeaderViewlet, self).update()


class OdwbWidgetHeaderViewlet(HeaderViewlet):

    def should_render(self):
        view = self.view
        if hasattr(view, "should_display_odwb_widget_viewlet"):
            return view.should_display_odwb_widget_viewlet
        return False

    def render(self):
        # if self.should_render():
        return self.index()
        # return ""
