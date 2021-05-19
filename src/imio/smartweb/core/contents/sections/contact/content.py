# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer


class ISectionContact(ISection):
    """Marker interface and Dexterity Python Schema for SectionContact"""

    visible_blocks = schema.List(
        title=_(u"Visible blocks"),
        description=_(u"Blocks that will be displayed in contact"),
        value_type=schema.Choice(vocabulary="imio.smartweb.vocabulary.ContactBlocks"),
        default=["address", "contact_informations", "schedule"],
    )

    directives.widget(
        "visible_blocks",
        CheckBoxFieldWidget,
    )

    related_contact = schema.Choice(
        title=_(u"Related contact"),
        description=_(u"Related contact"),
        source="imio.smartweb.vocabulary.RemoteContacts",
        required=True,
    )


@implementer(ISectionContact)
class SectionContact(Section):
    """SectionContact class"""
