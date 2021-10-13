# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView


class CollectionView(SectionView):
    """Collection Section view"""

    def items(self):
        number_of_items_in_batch = self.context.number_of_items_in_batch
        max_items = self.context.maximum_number_of_items
        results = self.context.collection.to_object.results(
            batch=False, brains=True, limit=max_items
        )
        lst_dict = []
        lst_objects = [i.getObject() for i in results]
        batch = []
        list_size = len(lst_objects)
        for cpt, item in enumerate(lst_objects, start=1):
            url = item.absolute_url()
            dict = {
                "title": item.title,
                "description": item.description,
                "url": url,
                "image": f"{url}/@@images/image/{self.context.image_scale}",
                "has_image": True if item.aq_base.image else False,
            }
            batch.append(dict)
            if (
                cpt % number_of_items_in_batch == 0
                or list_size < number_of_items_in_batch # noqa
            ) and cpt > 0:
                lst_dict.append(batch)
                batch = []
        if batch != []:
            lst_dict.append(batch)
        return lst_dict
