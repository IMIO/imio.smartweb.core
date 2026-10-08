# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IEguichetMessage(model.Schema):

    eguichet_display_message = schema.Bool(
        title=_("Display this message in our e-guichet"),
        required=False,
        default=False,
    )
