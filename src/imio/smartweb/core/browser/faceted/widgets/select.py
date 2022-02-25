# -*- coding: utf-8 -*-

from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.select.widget import Widget


class Select(Widget):
    index = ViewPageTemplateFile("select.pt")
