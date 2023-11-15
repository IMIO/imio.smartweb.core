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

    directives.widget(
        "related_contacts",
        SelectFieldWidget,
        vocabulary="imio.smartweb.vocabulary.RemoteContacts",
        pattern_options={"multiple": True},
    )
    related_contacts = schema.List(
        title=_("Related contacts"),
        description=_(
            "Select contacts. If you can't find contacts you want, make sure "
            """it exists in the directory and that its "state" is published."""
        ),
        value_type=schema.Choice(source="imio.smartweb.vocabulary.RemoteContacts"),
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
            "gallery_mode",
            "nb_results_by_batch",
            "image_scale",
        ],
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
        values=[1, 2, 3, 4],
    )

    nb_contact_by_line = schema.Choice(
        title=_("Maximum number of contacts by line"),
        description=_("Maximum number of contacts by line (on PC)"),
        required=True,
        default=4,
        values=[1, 2, 3, 4],
    )

    image_scale = schema.Choice(
        title=_("Image scale for images (only for gallery mode)"),
        default="affiche",
        vocabulary="imio.smartweb.vocabulary.Scales",
        required=True,
    )


@implementer(ISectionContact)
class SectionContact(Section):
    """SectionContact class"""

    can_toggle_title_visibility = False
