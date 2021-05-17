# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.views import SectionView
from plone.app.contenttypes.browser.folder import FolderView


class FilesView(SectionView, FolderView):
    """Files Section view"""
