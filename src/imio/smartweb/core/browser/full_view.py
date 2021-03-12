# -*- coding: utf-8 -*-

from imio.smartweb.core.viewlets.files_and_gallery import IFilesAndGalleryView
from plone.app.contenttypes.browser.full_view import FullViewItem as BaseFullViewItem
from zope.interface import implementer


@implementer(IFilesAndGalleryView)
class FullViewItem(BaseFullViewItem):
    """"""
