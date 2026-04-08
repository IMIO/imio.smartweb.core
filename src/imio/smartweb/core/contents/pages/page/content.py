# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from zope.interface import implementer
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.supermodel import model
from zope import schema


class IPage(IPages, model.Schema):
    """Marker interface and Dexterity Python Schema for Page"""

    model.fieldset("layout", label=_("Layout"), fields=["text_align_container"])
    text_align_container = schema.Bool(
        title=_("Align title with text"),
        required=False,
        default=False,
    )


@implementer(IPage, IInstanceBehaviorAssignableContent)
class Page(Pages):
    """Page class"""

    category_name = "page_category"
