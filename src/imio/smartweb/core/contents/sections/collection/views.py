# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_scale_url


class CollectionView(CarouselOrTableSectionView):
    """Collection Section view"""

    def items(self):
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        orientation = self.context.orientation
        image_scale = self.image_scale
        items = self.context.collection.to_object.results(
            batch=False, brains=True, limit=max_items
        )
        results = []
        for item in items:
            url = item.getURL()
            scale_url = get_scale_url(
                item, self.request, "image", image_scale, orientation
            )
            dict_item = {
                "title": item.Title,
                "description": item.Description,
                "effective": item.effective,
                "url": url,
                "has_image": item.has_leadimage,
            }
            if scale_url == "":
                dict_item["bad_scale"] = image_scale
                scale_url = f"{url}/@@images/image/{image_scale}"
            dict_item["image"] = scale_url
            results.append(dict_item)
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def see_all_url(self):
        return self.context.collection.to_object.absolute_url()
