# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_scale_url
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
            scale_url = get_scale_url(item, self.request, "image", image_scale)
            results.append(
                {
                    "title": item.title,
                    "description": item.description,
                    "url": url,
                    "image": scale_url,
                    "has_image": has_image,
                    "item_infos": file_view.human_readable_size(),
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)
