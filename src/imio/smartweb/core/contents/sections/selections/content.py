# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.vocabularies.catalog import CatalogSource
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import implementer
from zope import schema


class ISectionSelections(ISection):
    """Marker interface and Dexterity Python Schema for SectionSelections"""

    model.fieldset("layout", fields=["image_scale"])
    image_scale = schema.Choice(
        title=_(u"Image scale"),
        default=u"tile",
        vocabulary="plone.app.vocabularies.ImagesScales",
        required=True,
    )

    selected_items = RelationList(
        title=_(u"Selected items"),
        value_type=RelationChoice(
            title=u"",
            source=CatalogSource(),
        ),
        required=True,
    )


@implementer(ISectionSelections)
class SectionSelections(Section):
    """SectionSelections class"""

    manage_content = True
    manage_display = True
