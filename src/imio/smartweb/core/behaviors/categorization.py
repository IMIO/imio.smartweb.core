# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class ICategoryDisplay(model.Schema):
    directives.order_before(show_categories_or_topics="IOrientation.orientation")

    model.fieldset("layout", fields=["show_categories_or_topics"])
    show_categories_or_topics = schema.Choice(
        title=_("Show category or topic"),
        description=_(
            "Select if you want (specific) category or (first) topic displayed on items"
        ),
        source="imio.smartweb.vocabulary.CategoriesDisplay",
        required=True,
        default="category",
    )
