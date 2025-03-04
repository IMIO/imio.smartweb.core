# -*- coding: utf-8 -*-

from imio.smartweb.common.widgets.select import TranslatedAjaxSelectWidget
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class ISectionTimestampedPublications(ISection):
    """Marker interface and Dexterity Python Schema for SectionTimestampedPublications"""

    related_timestamped_publications = schema.List(
        title=_("Related timestamped publications"),
        value_type=schema.Choice(
            source="imio.smartweb.vocabulary.IADeliberationsPublications"
        ),
        required=False,
    )
    directives.widget(
        "related_timestamped_publications",
        TranslatedAjaxSelectWidget,
        vocabulary="imio.smartweb.vocabulary.IADeliberationsPublications",
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

    model.fieldset("layout", fields=["show_items_description"])
    show_items_description = schema.Bool(
        title=_("Show items description"), required=False
    )


@implementer(ISectionTimestampedPublications)
class SectionTimestampedPublications(Section):
    """SectionTimestampedPublications class"""

    # We don't need to manage display on timestamped publications
    # only common table view / don't need common carousel view
    manage_display = False
    show_items_date = True
