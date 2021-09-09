# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class INewsView(model.Schema):
    """ """

    nb_results = schema.Int(
        title=_(u"Number of items to display"), default=20, required=True
    )

    see_more_link = schema.URI(title=_(u"See more link"), required=False)

    directives.widget(selected_news_folders=SelectFieldWidget)
    selected_news_folders = schema.List(
        title=_(u"Selected news folders"),
        description=_(u"Select news folders to display"),
        value_type=schema.Choice(
            vocabulary="imio.smartweb.vocabulary.RemoteNewsFolders"
        ),
        required=True,
    )

    show_items_description = schema.Bool(
        title=_(u"Show items description"), default=True, required=False
    )


@implementer(INewsView)
class NewsView(Container):
    """NewsView class"""
