# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from zope.interface import implementer


class ISectionText(ISection):
    """Marker interface and Dexterity Python Schema for SectionText"""


@implementer(ISectionText)
class SectionText(Section):
    """SectionText class"""

    manage_content = True
