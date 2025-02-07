# -*- coding: utf-8 -*-

from embeddify import Embedder
from embeddify import Vimeo
from embeddify import YouTube
from embeddify.embeddify import STANDARD_PLUGINS
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from zope.i18n import translate

import html


class VideoView(SectionView):
    def get_embed_video(self, width=800, height=600):
        plugins = STANDARD_PLUGINS
        plugins = [
            SmartwebYoutube() if isinstance(plugin, YouTube) else plugin
            for plugin in plugins
        ]
        plugins = [
            SmartwebVimeo() if isinstance(plugin, Vimeo) else plugin
            for plugin in plugins
        ]
        embedder = Embedder(width=width, height=height, plugins=plugins)
        return embedder(self.context.video_url, params=dict(autoplay=False))


class SmartwebYoutube(YouTube):

    def do_request(self, parts, config):
        if self.test(parts):
            res = super(SmartwebYoutube, self).do_request(parts, config)
            title = res.get("title", "")
            current_lang = api.portal.get_current_language()[:2]
            additional_accessibility_info = translate(
                _("Youtube video"), target_language=current_lang
            )
            res["title"] = f"{title} ({additional_accessibility_info})"
            if title != "":
                res["html"] = res["html"].replace(html.escape(title), res["title"])
            return res
        return


class SmartwebVimeo(Vimeo):

    def do_request(self, parts, config):
        if self.test(parts):
            res = super(SmartwebVimeo, self).do_request(parts, config)
            title = res.get("title", "")
            current_lang = api.portal.get_current_language()[:2]
            additional_accessibility_info = translate(
                _("Vimeo video"), target_language=current_lang
            )
            res["title"] = f"{title} ({additional_accessibility_info})"
            if title != "":
                res["html"] = res["html"].replace(html.escape(title), res["title"])
            return res
        return
