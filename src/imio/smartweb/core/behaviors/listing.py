# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IListing(model.Schema):

    directives.order_after(
        exclude_from_parent_listing="IExcludeFromNavigation.exclude_from_nav"
    )

    model.fieldset("settings", fields=["exclude_from_parent_listing"])
    exclude_from_parent_listing = schema.Bool(
        title=_("Exclude from parent listing"),
        description=_("If selected, this item will not appear in parent listing views"),
        required=False,
        default=False,
    )
