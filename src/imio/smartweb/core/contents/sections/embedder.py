# -*- coding: utf-8 -*-

from embeddify import Embedder
from embeddify import OEmbedPlugin
from embeddify import Vimeo
from embeddify import YouTube
from embeddify.embeddify import STANDARD_PLUGINS
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.i18n import translate

import html
import re


class AccessibleTitleMixin:
    """Append the video provider name to the oembed title.

    The rewritten title is also injected back into the embed markup, where it
    ends up on the iframe "title" attribute read by screen readers.
    """

    provider_label = None

    def do_request(self, parts, config):
        if not self.test(parts):
            return
        res = super().do_request(parts, config)
        if res is None:
            return
        title = res.get("title", "")
        current_lang = api.portal.get_current_language()[:2]
        additional_accessibility_info = translate(
            self.provider_label, target_language=current_lang
        )
        res["title"] = f"{title} ({additional_accessibility_info})"
        if title != "":
            res["html"] = res["html"].replace(html.escape(title), res["title"])
        return res


class SmartwebYoutube(AccessibleTitleMixin, YouTube):

    provider_label = _("Youtube video")


class SmartwebVimeo(AccessibleTitleMixin, Vimeo):

    provider_label = _("Vimeo video")


class SmartwebPeertube(AccessibleTitleMixin, OEmbedPlugin):
    """PeerTube is federated : there is no domain to match on, so we match on
    the url path and derive the oembed endpoint from the host itself.
    """

    provider_label = _("Peertube video")
    video_path = re.compile(r"^/(w|videos/watch)/[\w-]+/?$")

    def test(self, parts):
        """https only : we do not want an editor to make the site request an
        arbitrary internal host.
        """
        return parts.scheme == "https" and bool(self.video_path.match(parts.path))

    def do_request(self, parts, config):
        if not self.test(parts):
            return
        self.api_url = f"https://{parts.netloc}/services/oembed"
        return super().do_request(parts, config)


def get_video_embedder(width=800, height=600):
    """Embedder shared by every section holding a video_url field"""
    plugins = [
        SmartwebYoutube() if isinstance(plugin, YouTube) else plugin
        for plugin in STANDARD_PLUGINS
    ]
    plugins = [
        SmartwebVimeo() if isinstance(plugin, Vimeo) else plugin for plugin in plugins
    ]
    # Last : matching on a path is looser than matching on a known domain.
    plugins.append(SmartwebPeertube())
    return Embedder(width=width, height=height, plugins=plugins)
