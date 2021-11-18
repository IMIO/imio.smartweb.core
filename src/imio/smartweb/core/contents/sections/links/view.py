# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import CarouselOrTableSectionView
from imio.smartweb.core.utils import batch_results


class LinksView(CarouselOrTableSectionView):
    """Links Section view"""

    def items(self):
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
            results.append(
                {
                    "title": item.title,
                    "description": item.description,
                    "url": url,
                    "icon": item.svg_icon,
                    "has_icon": has_icon,
                    "image": f"{url}/@@images/image/{image_scale}",
                    "has_image": has_image,
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)
