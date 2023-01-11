# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results

import Missing


class CollectionView(CarouselOrTableSectionView):
    """Collection Section view"""

    def items(self):
        max_items = self.context.nb_results_by_batch * self.context.max_nb_batches
        image_scale = self.image_scale
        items = self.context.collection.to_object.results(
            batch=False, brains=True, limit=max_items
        )
        results = []
        for item in items:
            url = item.getURL()
            scale_url = None
            if hasattr(item, "image_scales") and item['image_scales'] != Missing.Value:
                scale_url = "{}/{}".format(url, item['image_scales']['image'][0]['scales'][image_scale]['download'])
            results.append(
                {
                    "title": item.Title,
                    "description": item.Description,
                    "effective": item.effective,
                    "url": url,
                    "image": scale_url,
                    "has_image": item.has_leadimage,
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)

    @property
    def see_all_url(self):
        return self.context.collection.to_object.absolute_url()
