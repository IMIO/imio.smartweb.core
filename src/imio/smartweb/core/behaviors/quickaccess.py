# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IQuickAccessSelection(model.Schema):

    quick_access_items = RelationList(
        title=_(u"Quick access contents"),
        value_type=RelationChoice(
            title=u"Items selection",
            source=CatalogSource(),
        ),
        required=False,
    )
    directives.widget(
        "quick_access_items",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "favorites": [],
        },
    )

    model.fieldset(
        "categorization", label=_(u"Categorization"), fields=["quick_access_items"]
    )


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
