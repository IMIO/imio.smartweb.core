# -*- coding: utf-8 -*-
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from zope.interface import classImplements


class EditForm(DefaultEditForm):
    """ EditForm """


DefaultEditView = layout.wrap_form(EditForm)
classImplements(DefaultEditView, IDexterityEditForm)


class EditView(DefaultEditView):
    """ EditView """
