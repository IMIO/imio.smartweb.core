# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import provider


@provider(IFormFieldProvider)
class IQuickAccessSelection(model.Schema):

    quick_access_items = RelationList(
        title=_("Quick access contents"),
        value_type=RelationChoice(
            title="Items selection",
            vocabulary="plone.app.vocabularies.Catalog",
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
        "categorization", label=_("Categorization"), fields=["quick_access_items"]
    )
