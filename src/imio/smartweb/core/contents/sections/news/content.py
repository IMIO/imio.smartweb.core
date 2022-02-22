# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def see_all_default(context):
    return translate(_("See all news"), context=getRequest())


class ISectionNews(ISection):
    """Marker interface and Dexterity Python Schema for SectionNews"""

    directives.widget(related_news=SelectFieldWidget)
    related_news = schema.Choice(
        title=_("Related news folder"),
        source="imio.smartweb.vocabulary.RemoteNewsFolders",
        required=True,
    )

    directives.widget(
        "linking_rest_view",
        RelatedItemsFieldWidget,
        vocabulary="plone.app.vocabularies.Catalog",
        pattern_options={
            "selectableTypes": ["imio.smartweb.NewsView"],
            "favorites": [],
        },
    )
    linking_rest_view = RelationChoice(
        title=_("News view used to display news items details"),
        vocabulary="plone.app.vocabularies.Catalog",
        required=True,
    )

    nb_results_by_batch = schema.Choice(
        title=_("Number of items per batch"),
        required=True,
        default=3,
        values=[1, 3, 4],
    )

    max_nb_batches = schema.Int(
        title=_("Maximum number of batches to display"),
        required=True,
        default=2,
        min=1,
        max=12,
    )

    link_text = schema.TextLine(
        title=_("Text for the link to the news view"),
        defaultFactory=see_all_default,
        required=True,
    )

    model.fieldset("layout", fields=["show_items_description"])
    show_items_description = schema.Bool(
        title=_("Show items description"), required=False
    )


@implementer(ISectionNews)
class SectionNews(Section):
    """SectionNews class"""

    manage_display = True
    show_items_date = True
