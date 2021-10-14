# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView


class CollectionView(SectionView):
    """Collection Section view"""

    def items(self):
        number_of_items_by_batch = self.context.nb_results_by_batch
        max_items = self.context.max_nb_results
        results = self.context.collection.to_object.results(
            batch=False, brains=True, limit=max_items
        )
        lst_dict = []
        batch = []
        list_size = len(results)
        for cpt, item in enumerate(results, start=1):
            url = item.getURL()
            dict = {
                "title": item.Title,
                "description": item.Description,
                "url": url,
                "image": f"{url}/@@images/image/{self.context.image_scale}",
                "has_image": item.has_leadimage,
            }
            batch.append(dict)
            if (
                cpt % number_of_items_by_batch == 0
                or list_size < number_of_items_by_batch  # noqa
            ) and cpt > 0:
                lst_dict.append(batch)
                batch = []
        if batch != []:
            lst_dict.append(batch)
        return lst_dict
