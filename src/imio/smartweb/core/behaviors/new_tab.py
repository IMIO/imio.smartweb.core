# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class INewTab(model.Schema):

    directives.order_after(open_in_new_tab="remoteUrl")
    open_in_new_tab = schema.Bool(
        title=_("Open in a new tab"),
        required=False,
        default=False,
    )
