# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView


class LinksView(SectionView):
    """Links Section view"""

    def items(self):
        return self.context.listFolderContents()
