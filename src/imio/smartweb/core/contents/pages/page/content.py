# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope import schema
from zope.interface import implementer

CATEGORY_TAXONOMY = "collective.taxonomy.page"


class IPage(IPages):
    """Marker interface and Dexterity Python Schema for Page"""

    category = schema.Choice(
        title=_(u"Category"),
        source=CATEGORY_TAXONOMY,
        required=False,
    )


@implementer(IPage)
class Page(Pages):
    """Page class"""

    category_taxonomy = CATEGORY_TAXONOMY
