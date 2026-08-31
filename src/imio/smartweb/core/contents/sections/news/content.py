# -*- coding: utf-8 -*-

from imio.smartweb.common.widgets.select import TranslatedAjaxSelectWidget
from imio.smartweb.core.contents.rest.search.endpoint import (
    get_default_view_url,
)
from imio.smartweb.core.contents.sections.base import carries_fields
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.core.utils import get_newsfolder_scope_uids
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.z3cform.widgets.contentbrowser import ContentBrowserFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import RelationChoice
from zope import schema
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def see_all_default(context):
    return translate(_("See all news"), context=getRequest())


class ISectionNews(ISection):
    """Marker interface and Dexterity Python Schema for SectionNews"""

    directives.widget(
        "linking_rest_view",
        ContentBrowserFieldWidget,
        vocabulary="imio.smartweb.vocabulary.NewsViewsSite",
        pattern_options={
            "selectableTypes": ["imio.smartweb.NewsView"],
            "favorites": [],
        },
    )
    linking_rest_view = RelationChoice(
        title=_("News view used to display news items details"),
        description=_(
            'Only used when "All the news items of a news folder" is selected '
            "below. A hand-picked selection links to the default news view of "
            "the control panel instead."
        ),
        vocabulary="imio.smartweb.vocabulary.NewsViewsSite",
        required=False,
    )

    directives.widget(news_source=RadioFieldWidget)
    news_source = schema.Choice(
        title=_("News items to display"),
        description=_(
            "Choose whether this section lists a whole news folder or only the "
            "news items you pick yourself. Only the field matching your choice "
            "is used."
        ),
        source="imio.smartweb.vocabulary.SectionNewsSource",
        required=True,
        default="newsfolder",
    )

    directives.widget(related_news=SelectFieldWidget)
    related_news = schema.Choice(
        title=_("Related news folder"),
        description=_(
            'Used when "All the news items of a news folder" is selected above. '
            "Limited to the news folders the linking view above can display."
        ),
        source="imio.smartweb.vocabulary.ScopedNewsFolders",
        required=False,
    )

    specific_related_newsitems = schema.List(
        title=_("Specific related news"),
        description=_(
            'Used when "Only the news items I choose myself" is selected above. '
            "Any news item of the entity can be picked, whatever its folder. "
            "Items are displayed in the order you set here and link to the "
            "default news view of the control panel."
        ),
        value_type=schema.Choice(source="imio.smartweb.vocabulary.NewsItemsFromEntity"),
        required=False,
    )
    directives.widget(
        "specific_related_newsitems",
        TranslatedAjaxSelectWidget,
        vocabulary="imio.smartweb.vocabulary.NewsItemsFromEntity",
        pattern_options={"multiple": True},
    )

    nb_results_by_batch = schema.Choice(
        title=_("Number of items per batch"),
        required=True,
        default=3,
        values=[1, 2, 3, 4],
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

    model.fieldset("layout", fields=["display_newsfolders_titles"])
    display_newsfolders_titles = schema.Bool(
        title=_("Display news folders titles"),
        description=_("If checked, display news folders titles in the carousel view."),
        required=False,
    )

    @invariant
    def required_news_source(data):
        if not carries_fields(
            data,
            "linking_rest_view",
            "news_source",
            "related_news",
            "specific_related_newsitems",
        ):
            return
        if data.news_source == "selection":
            # linking_rest_view plays no part here: hand-picked items come from
            # the whole entity and link to the control panel's default view.
            if not data.specific_related_newsitems:
                raise Invalid(_("Please select at least one news item."))
            if not get_default_view_url("news"):
                raise Invalid(
                    _("No default news view is configured in the Smartweb settings.")
                )
            return
        if not data.linking_rest_view:
            raise Invalid(_("Please select a news view."))
        if not data.related_news:
            raise Invalid(_("Please select a news folder."))
        # On a real submission this is the view *itself*, not a RelationValue
        # (see RelationChoiceContentBrowserWidgetConverter). Both shapes must
        # work: a RelationValue still arrives against a stored object.
        news_view = getattr(data.linking_rest_view, "to_object", data.linking_rest_view)
        # An empty scope means the authentic source is unreachable, never
        # "nothing is in scope", hence the "scope and" guard below.
        scope = get_newsfolder_scope_uids(
            getattr(news_view, "selected_news_folder", None)
        )
        if scope and data.related_news not in scope:
            raise Invalid(
                _("This news folder is not displayed by the selected news view.")
            )


@implementer(ISectionNews)
class SectionNews(Section):
    """SectionNews class"""

    manage_display = True
    show_items_date = True
