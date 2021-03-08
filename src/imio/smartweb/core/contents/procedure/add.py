# -*- coding: utf-8 -*-
from plone.dexterity.browser import add


class AddForm(add.DefaultAddForm):
    portal_type = "imio.smartweb.Procedure"


class AddView(add.DefaultAddView):
    form = AddForm
