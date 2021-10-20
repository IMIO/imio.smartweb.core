# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionWithCarouselView
from imio.smartweb.core.utils import batch_results


class LinksView(SectionWithCarouselView):
    """Links Section view"""

    def items(self):
        image_scale = self.image_scale
        items = self.context.listFolderContents()
        results = []
        for item in items:
            url = item.absolute_url()
            has_image = True if getattr(item.aq_base, "image", None) else False
            results.append(
                {
                    "title": item.title,
                    "description": item.description,
                    "url": url,
                    "image": f"{url}/@@images/image/{image_scale}",
                    "has_image": has_image,
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)
