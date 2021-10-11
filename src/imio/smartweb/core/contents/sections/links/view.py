# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView


class LinksView(SectionView):
    """Links Section view"""

    def items(self):
        items = self.context.listFolderContents()
        lst_dict = []

        for item in items:
            url = item.absolute_url()
            dict = {
                "title": item.title,
                "description": item.description,
                "url": url,
                "image": f"{url}/@@images/image/{self.context.image_scale}",
                "has_image": True if item.aq_base.image else False,
            }
            lst_dict.append(dict)
        return lst_dict
