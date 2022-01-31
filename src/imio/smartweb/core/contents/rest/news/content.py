# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class INewsView(model.Schema):
    """Marker interface and Dexterity Python Schema for NewsView"""

    selected_news_folder = schema.Choice(
        title=_("Selected news folder"),
        description=_("Select news folder to display"),
        vocabulary="imio.smartweb.vocabulary.RemoteNewsFolders",
        required=True,
    )

    nb_results = schema.Int(
        title=_("Number of items to display"), default=20, required=True
    )

    show_items_description = schema.Bool(
        title=_("Show items description"), default=True, required=False
    )


@implementer(INewsView)
class NewsView(Container):
    """NewsView class"""
