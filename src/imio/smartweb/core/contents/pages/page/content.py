# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

CATEGORY_TAXONOMY = "collective.taxonomy.page_category"


class IPage(IPages):
    """Marker interface and Dexterity Python Schema for Page"""

    directives.order_before(category="ICategorization.subjects")
    model.fieldset("categorization", fields=["category"])
    category = schema.Choice(
        title=_(u"Category"),
        source=CATEGORY_TAXONOMY,
        required=False,
    )


@implementer(IPage)
class Page(Pages):
    """Page class"""

    category_taxonomy = CATEGORY_TAXONOMY
