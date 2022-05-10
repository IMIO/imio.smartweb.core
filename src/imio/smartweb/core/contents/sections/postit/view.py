# -*- coding: utf-8 -*-

from imio.smartweb.common.utils import rich_description
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.core.utils import batch_results


class PostitView(SectionView):
    """ """

    def items(self):
        items = self.context.postits or []
        results = []
        for item in items:
            description = rich_description(item["description"])
            results.append(
                {
                    "title": item["title"],
                    "subtitle": item["subtitle"],
                    "description": description,
                    "url": "",
                    "icon": None,
                    "has_icon": False,
                    "image": "",
                    "has_image": False,
                    "open_in_new_tab": False,
                }
            )
        return batch_results(results, self.context.nb_results_by_batch)
