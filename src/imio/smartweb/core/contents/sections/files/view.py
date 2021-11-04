# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from zope.component import queryMultiAdapter


class FilesView(CarouselOrTableSectionView):
    """Files Section view"""

    def items(self):
        image_scale = self.image_scale
        items = self.context.listFolderContents()
        results = []
        for item in items:
            url = item.absolute_url()
            has_image = True if getattr(item.aq_base, "image", None) else False
            file_view = queryMultiAdapter((item, self.request), name="file_view")
            results.append(
                {
                    "title": item.title,
                    "description": item.description,
                    "url": url,
                    "image": f"{url}/@@images/image/{image_scale}",
                    "has_image": has_image,
                    "item_infos": file_view.human_readable_size(),
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)
