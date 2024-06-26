# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import RestView
from imio.smartweb.locales import SmartwebMessageFactory as _
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

    display_newsfolders_titles = schema.Bool(
        title=_("Display news folders titles"),
        description=_("If checked, display news folders titles"),
        required=False,
    )


@implementer(INewsView)
class NewsView(RestView):
    """NewsView class"""
