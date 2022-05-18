# -*- coding: utf-8 -*-

from imio.smartweb.common.config import DESCRIPTION_MAX_LENGTH
from imio.smartweb.core.contents.blocks.link.fields import LinkField
from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform import directives
from plone.namedfile.field import NamedBlobImage
from zope import schema
from zope.interface import implementer


class ISectionSlide(ISection):
    """Marker interface and Dexterity Python Schema for SectionSlide"""

    directives.omitted(
        "hide_title", "collapsible_section", "background_image", "bootstrap_css_class"
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

    show_title_and_description = schema.Bool(
        title=_(
            "Title and description will be displayed in front of picture as a slogan"
        ),
        required=False,
        default=False,
    )

    image = NamedBlobImage(
        title=_("Image"),
        description=_("Picture will be displayed as slide background"),
        required=False,
    )

    color = schema.TextLine(
        title=_("Color"),
        description=_("Like supplement or alternatively to picture"),
        required=False,
    )

    video_url = schema.URI(
        title=_("Youtube video URL"),
        description=_("Alternatively as a picture"),
        required=False,
    )

    link_title = schema.TextLine(
        title=_("Link title"),
        description=_("Link title will be display on picture as clickable element"),
        required=False,
    )

    remoteUrl = LinkField(title=_("Link URL"), required=False)

    open_in_new_tab = schema.Bool(
        title=_("Open in a new tab"), required=False, default=False
    )


@implementer(ISectionSlide)
class SectionSlide(Section):
    """SectionSlide class"""

    can_toggle_title_visibility = False
