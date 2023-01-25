# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from imio.smartweb.locales import SmartwebMessageFactory as _
from zope.interface import implementer
from zope import schema


class ICirkwiView(IPages):
    """Marker interface and Dexterity Python Schema for CirkwiView"""

    cirkwi_widget_id = schema.TextLine(
        title=_("Cirkwi widget ID"),
        description=_(
            "Specify your cirkwi widget ID. You can find it when you create a new widget in Cirkwi."
        ),
        required=True,
    )


@implementer(ICirkwiView)
class CirkwiView(Pages):
    """CirkwiView class"""
