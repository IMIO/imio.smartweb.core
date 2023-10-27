# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IOrientation(model.Schema):
    model.fieldset("layout", label=_("Layout"), fields=["orientation"])
    orientation = schema.Choice(
        title=_("Orientation"),
        required=True,
        vocabulary="imio.smartweb.vocabulary.Orientation",
        default="paysage",
    )
