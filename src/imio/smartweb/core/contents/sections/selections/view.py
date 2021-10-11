# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView


class SelectionsView(SectionView):
    """Selection Section view"""

    def items(self):
        items = [rel.to_object for rel in self.context.selected_items]
        lst_dict = []

        for item in items:
            url = item.absolute_url()
            dict = {
                "title": item.title,
                "description": item.description,
                "url": url,
                "image": f"{url}/@@images/image/{self.context.image_scale}",
                "has_image": True if getattr(item.aq_base, "image", None) else False,
            }
            lst_dict.append(dict)
        return lst_dict
