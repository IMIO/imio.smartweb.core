# -*- coding: utf-8 -*-

from plone.app.layout.viewlets.social import SocialTagsViewlet as BaseSocialTagsViewlet
from plone.memoize.view import memoize
from Products.CMFPlone.browser.syndication.adapters import BaseItem
from Products.CMFPlone.browser.syndication.adapters import FolderFeed
from Products.CMFPlone.interfaces.syndication import IFeedItem
from Products.CMFPlone.utils import getSiteLogo
from zope.component import queryMultiAdapter
from zope.component.hooks import getSite


class SocialTagsViewlet(BaseSocialTagsViewlet):
    @memoize
    def _get_tags(self):
        """
        Change social tags to avoid getting full size images and take the
        vignette scale instead
        """
        tags = super(SocialTagsViewlet, self)._get_tags()

        # if image tag(s) contain logo url, we have nothing to do
        logo_url = getSiteLogo()
        tag_image_is_logo = False
        has_tag_image = False
        for tag in tags:
            if tag.get("property") != "og:image" and tag.get("itemprop") != "image":
                continue
            has_tag_image = True
            if tag["content"] == logo_url:
                tag_image_is_logo = True
                break

        if tag_image_is_logo or not has_tag_image:
            return tags

        # otherwise, we calculate an image url with the correct scale
        site = getSite()
        feed = FolderFeed(site)
        item = queryMultiAdapter((self.context, feed), IFeedItem, default=None)
        if item is None:
            item = BaseItem(self.context, feed)

        image_url = content_url = self.context.absolute_url()
        if item.file:
            image_url = f"{content_url}/@@images/{item.field_name}/vignette"
        for tag in tags:
            if tag.get("property") != "og:image" and tag.get("itemprop") != "image":
                continue
            tag["content"] = image_url

        return tags
