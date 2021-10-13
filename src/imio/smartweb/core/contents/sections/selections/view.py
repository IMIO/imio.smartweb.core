# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView


class SelectionsView(SectionView):
    """Selection Section view"""

    def items(self):
        number_of_items_in_batch = 1
        items = [rel.to_object for rel in self.context.selected_items]
        lst_dict = []
        batch = []
        list_size = len(items)
        for cpt, item in enumerate(items, start=1):
            url = item.absolute_url()
            dict = {
                "title": item.title,
                "description": item.description,
                "url": url,
                "image": f"{url}/@@images/image/{self.context.image_scale}",
                "has_image": True if getattr(item.aq_base, "image", None) else False,
            }
            batch.append(dict)
            if (
                cpt % number_of_items_in_batch == 0
                or list_size < number_of_items_in_batch  # noqa
            ) and cpt > 0:
                lst_dict.append(batch)
                batch = []
        if batch != []:
            lst_dict.append(batch)
        return lst_dict
