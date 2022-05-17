# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer


class ISectionContact(ISection):
    """Marker interface and Dexterity Python Schema for SectionContact"""

    directives.widget(related_contact=SelectFieldWidget)
    related_contact = schema.Choice(
        title=_("Related contact"),
        description=_(
            "Select a contact. If you can't find the contact you want, make sure "
            """it exists in the directory and that its "state" is published."""
        ),
        source="imio.smartweb.vocabulary.RemoteContacts",
        required=True,
    )

    directives.widget(visible_blocks=CheckBoxFieldWidget)
    visible_blocks = schema.List(
        title=_("Visible blocks"),
        description=_("Blocks that will be displayed in contact"),
        value_type=schema.Choice(vocabulary="imio.smartweb.vocabulary.ContactBlocks"),
        default=["address", "itinerary", "contact_informations", "schedule"],
    )

    model.fieldset(
        "layout",
        fields=[
            "is_in_portrait_mode",
            "gallery_mode",
            "nb_results_by_batch",
            "image_scale",
        ],
    )

    is_in_portrait_mode = schema.Bool(
        title=_("Switch lead image to portrait mode"), required=False, default=False
    )

    gallery_mode = schema.Choice(
        title=_("Gallery mode"),
        description=_("Choose your gallery layout mode"),
        source="imio.smartweb.vocabulary.GalleryMode",
        default="gallery",
    )

    nb_results_by_batch = schema.Choice(
        title=_("Number of items per batch (only for carousel mode)"),
        required=True,
        default=3,
        values=[1, 3, 4],
    )

    image_scale = schema.Choice(
        title=_("Image scale for images (only for gallery mode)"),
        default="preview",
        vocabulary="plone.app.vocabularies.ImagesScales",
        required=True,
    )


@implementer(ISectionContact)
class SectionContact(Section):
    """SectionContact class"""

    can_toggle_title_visibility = False
