# -*- coding: utf-8 -*-

from eea.facetednavigation.config import ANNO_FACETED_LAYOUT
from eea.facetednavigation.layout.layout import FacetedLayout
from zope.annotation.interfaces import IAnnotations


class SmartwebFacetedLayout(FacetedLayout):
    @property
    def layout(self):
        return IAnnotations(self.context).get(
            ANNO_FACETED_LAYOUT, "faceted-summary-view"
        )
