# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.social import SocialTagsViewlet as BaseSocialTagsViewlet


class SocialTagsViewlet(BaseSocialTagsViewlet):
    social_image_scale = "paysage_vignette"
