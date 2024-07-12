# -*- coding: utf-8 -*-

# from imio.smartweb.core.contents import IPortalPage
from plone.app.layout.viewlets.social import SocialTagsViewlet as BaseSocialTagsViewlet


class SocialTagsViewlet(BaseSocialTagsViewlet):
    social_image_scale = "paysage_vignette"

    @property
    def tags(self):
        tags = super(SocialTagsViewlet, self).tags
        # if IPortalPage.providedBy(self.context):
        if getattr(self.context, "image", None) is None:
            return tags
        tags = [item for item in tags if "og:image" not in item.get("property", "")]
        scales = self.context.restrictedTraverse("@@images")
        scale = scales.scale("image", scale=self.social_image_scale)
        scale_url = scale.absolute_url()
        image = self.context.image
        tags.extend(
            [
                dict(property="og:image", content=scale_url),
                dict(property="og:image:width", content=scale.width),
                dict(property="og:image:height", content=scale.height),
                dict(itemprop="image", content=scale_url),
                dict(property="og:image:type", content=image.contentType),
            ]
        )
        return tags
