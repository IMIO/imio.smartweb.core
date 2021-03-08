# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IQuickAccess(model.Schema):

    directives.order_after(
        include_in_quick_access="IExcludeFromNavigation.exclude_from_nav"
    )
    model.fieldset("settings", fields=["include_in_quick_access"])
    include_in_quick_access = schema.Bool(
        title=_(u"Include in quick access menu"),
        description=_(u"If selected, this item will appear in quick access menu"),
        required=False,
        default=False,
    )
