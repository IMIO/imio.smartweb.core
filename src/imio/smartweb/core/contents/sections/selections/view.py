# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView


class SelectionsView(SectionView):
    def items(self):
        return [rel.to_object for rel in self.context.selected_items]
