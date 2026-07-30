# -*- coding: utf-8 -*-

from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.row import DictRow
from imio.smartweb.common.widgets.select import TranslatedAjaxSelectWidget
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.core.widgets.frozen_label import FrozenLabelTextFieldWidget
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class IPhoneDisplayRow(Interface):
    """One phone row of a related contact, plus the columns to display.

    Every column but `visible_columns` is remote directory data rendered as a
    frozen label: read-only looking, yet still submitted, because DictRow
    rejects a row whose keys are missing. Those stored copies are RESIDUE --
    the page render always reads the live directory payload. Never read them
    back.
    """

    directives.mode(contact_uid="hidden")
    contact_uid = schema.TextLine(title=_("Contact UID"), required=False)

    directives.widget("contact_title", FrozenLabelTextFieldWidget)
    contact_title = schema.TextLine(title=_("Contact"), required=False)

    directives.widget("label", FrozenLabelTextFieldWidget)
    label = schema.TextLine(title=_("Label"), required=False)

    directives.widget("type", FrozenLabelTextFieldWidget)
    type = schema.TextLine(title=_("Type"), required=False)

    directives.widget("number", FrozenLabelTextFieldWidget)
    number = schema.TextLine(title=_("Number"), required=False)

    directives.widget("visible_columns", CheckBoxFieldWidget)
    visible_columns = schema.List(
        title=_("Displayed columns"),
        value_type=schema.Choice(
            vocabulary="imio.smartweb.vocabulary.PhoneDisplayColumns"
        ),
        required=False,
    )


class IMailDisplayRow(Interface):
    """One e-mail row of a related contact, plus the columns to display.

    See IPhoneDisplayRow: the data columns are residue, never read back.
    """

    directives.mode(contact_uid="hidden")
    contact_uid = schema.TextLine(title=_("Contact UID"), required=False)

    directives.widget("contact_title", FrozenLabelTextFieldWidget)
    contact_title = schema.TextLine(title=_("Contact"), required=False)

    directives.widget("label", FrozenLabelTextFieldWidget)
    label = schema.TextLine(title=_("Label"), required=False)

    directives.widget("type", FrozenLabelTextFieldWidget)
    type = schema.TextLine(title=_("Type"), required=False)

    directives.widget("mail_address", FrozenLabelTextFieldWidget)
    mail_address = schema.TextLine(title=_("E-mail"), required=False)

    directives.widget("visible_columns", CheckBoxFieldWidget)
    visible_columns = schema.List(
        title=_("Displayed columns"),
        value_type=schema.Choice(
            vocabulary="imio.smartweb.vocabulary.MailDisplayColumns"
        ),
        required=False,
    )


class IUrlDisplayRow(Interface):
    """One URL row of a related contact, plus the columns to display.

    See IPhoneDisplayRow: the data columns are residue, never read back.
    """

    directives.mode(contact_uid="hidden")
    contact_uid = schema.TextLine(title=_("Contact UID"), required=False)

    directives.widget("contact_title", FrozenLabelTextFieldWidget)
    contact_title = schema.TextLine(title=_("Contact"), required=False)

    directives.widget("type", FrozenLabelTextFieldWidget)
    type = schema.TextLine(title=_("Type"), required=False)

    directives.widget("url", FrozenLabelTextFieldWidget)
    url = schema.TextLine(title=_("Url"), required=False)

    directives.widget("visible_columns", CheckBoxFieldWidget)
    visible_columns = schema.List(
        title=_("Displayed columns"),
        value_type=schema.Choice(
            vocabulary="imio.smartweb.vocabulary.UrlDisplayColumns"
        ),
        required=False,
    )


class ISectionContact(ISection):
    """Marker interface and Dexterity Python Schema for SectionContact"""

    directives.widget(
        "related_contacts",
        TranslatedAjaxSelectWidget,
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
        "contact_informations",
        label=_("Contact informations"),
        fields=["phones_display", "mails_display", "urls_display"],
    )

    directives.widget(
        "phones_display",
        DataGridFieldFactory,
        allow_insert=False,
        allow_delete=False,
        allow_reorder=False,
        auto_append=False,
    )
    phones_display = schema.List(
        title=_("Phones"),
        description=_(
            "Read-only rows loaded from the related contacts with the button "
            "at the bottom of this form. Check the columns you want to "
            "display; uncheck them all to hide the row."
        ),
        value_type=DictRow(title="Value", schema=IPhoneDisplayRow),
        required=False,
    )

    directives.widget(
        "mails_display",
        DataGridFieldFactory,
        allow_insert=False,
        allow_delete=False,
        allow_reorder=False,
        auto_append=False,
    )
    mails_display = schema.List(
        title=_("E-mails"),
        description=_(
            "Read-only rows loaded from the related contacts with the button "
            "at the bottom of this form. Check the columns you want to "
            "display; uncheck them all to hide the row."
        ),
        value_type=DictRow(title="Value", schema=IMailDisplayRow),
        required=False,
    )

    directives.widget(
        "urls_display",
        DataGridFieldFactory,
        allow_insert=False,
        allow_delete=False,
        allow_reorder=False,
        auto_append=False,
    )
    urls_display = schema.List(
        title=_("URLs"),
        description=_(
            "Read-only rows loaded from the related contacts with the button "
            "at the bottom of this form. Check the columns you want to "
            "display; uncheck them all to hide the row."
        ),
        value_type=DictRow(title="Value", schema=IUrlDisplayRow),
        required=False,
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
