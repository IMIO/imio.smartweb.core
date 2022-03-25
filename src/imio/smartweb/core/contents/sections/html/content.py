# -*- coding: utf-8 -*-

from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.directives import write_permission
from zope import schema
from zope.interface import implementer


class ISectionHTML(ISection):
    """Marker interface and Dexterity Python Schema for SectionHTML"""

    write_permission(html="imio.smartweb.core.CanManageSectionHTML")
    html = schema.SourceText(
        title=_("HTML"),
        description=_(
            "Enter your HTML code directly here. It must be nested in tags such as: "
            "<code>&lt;p&gt;code&lt;/p&gt;</code>, "
            "<code>&lt;span&gt;code&lt;/span&gt;</code>, "
            "<code>&lt;div&gt;code&lt;/div&gt;</code>"
        ),
        required=True,
    )

    description = schema.Text(
        title=_("Description"),
        description=_(
            "Use **text** to set text in bold. Limited to ${max} characters.",
            mapping={"max": DESCRIPTION_MAX_LENGTH},
        ),
        max_length=DESCRIPTION_MAX_LENGTH,
        required=False,
    )


@implementer(ISectionHTML)
class SectionHTML(Section):
    """SectionHTML class"""

    manage_content = True
