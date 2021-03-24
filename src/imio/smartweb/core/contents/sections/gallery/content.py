# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from zope.interface import implementer


class ISectionGallery(ISection):
    """Marker interface and Dexterity Python Schema for SectionGallery"""


@implementer(ISectionGallery)
class SectionGallery(Section):
    """SectionGallery class"""

    @property
    def get_last_mofication_date(self):
        items = self.listFolderContents()
        if not items:
            return super(SectionGallery, self).get_last_mofication_date
        dates_list = [item.ModificationDate() for item in items]
        return max(dates_list)
