# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results
from imio.smartweb.core.utils import get_scale_url


class LinksView(CarouselOrTableSectionView):
    """Links Section view"""

    def items(self):
        orientation = self.context.orientation
        image_scale = self.image_scale
        items = self.context.listFolderContents()
        results = []
        for item in items:
            url = item.absolute_url()
            has_icon = has_image = False
            if getattr(item.aq_base, "svg_icon", None):
                has_icon = True
            elif getattr(item.aq_base, "image", None):
                has_image = True
            scale_url = get_scale_url(
                item, self.request, "image", image_scale, orientation
            )
            results.append(
                {
                    "title": item.title,
                    "description": item.description,
                    "url": url,
                    "icon": item.svg_icon,
                    "has_icon": has_icon,
                    "image": scale_url,
                    "has_image": has_image,
                    "open_in_new_tab": item.open_in_new_tab,
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)
