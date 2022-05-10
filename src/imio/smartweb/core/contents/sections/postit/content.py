# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import schema
from plone.autoform import directives
from zope.interface import Interface
from zope.interface import implementer


class IPostit(Interface):
    """Postit schema"""

    title = schema.TextLine(
        title=_("Title"),
        required=False,
        default="",
        missing_value="",
    )

    subtitle = schema.TextLine(
        title=_("Subtitle"),
        required=False,
        default="",
        missing_value="",
    )

    description = schema.Text(
        title=_("Description"),
        description=_(
            "Use **text** to set text in bold. Limited to ${max} characters.",
            mapping={"max": DESCRIPTION_MAX_LENGTH},
        ),
        max_length=DESCRIPTION_MAX_LENGTH,
        required=False,
        default="",
        missing_value="",
    )


class ISectionPostit(ISection):
    """Marker interface and Dexterity Python Schema for SectionPostit"""

    description = schema.Text(
        title=_("Description"),
        description=_(
            "Use **text** to set text in bold. Limited to ${max} characters.",
            mapping={"max": DESCRIPTION_MAX_LENGTH},
        ),
        max_length=DESCRIPTION_MAX_LENGTH,
        required=False,
    )

    directives.widget("postits", DataGridFieldFactory, allow_reorder=True)
    postits = schema.List(
        title=_("Post-its"),
        value_type=DictRow(title=_("Post-it"), schema=IPostit),
        min_length=1,
        missing_value=[],
    )

    nb_results_by_batch = schema.Choice(
        title=_("Number of items per batch"),
        required=True,
        default=3,
        values=range(1, 9),
    )


@implementer(ISectionPostit)
class SectionPostit(Section):
    """SectionPostit class"""

    show_items_description = True
    show_items_lead_image = False
