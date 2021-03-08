# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.contenttypes.browser.folder import FolderView as BaseFolderView


class FolderView(BaseFolderView):

    def results(self, **kwargs):
        # Extra filter
        kwargs.update(self.request.get('contentFilter', {}))
        kwargs.setdefault('batch', True)
        kwargs.setdefault('b_size', self.b_size)
        kwargs.setdefault('b_start', self.b_start)
        kwargs.setdefault('orphan', 1)
        kwargs.setdefault('exclude_from_parent_listing', False)

        listing = aq_inner(self.context).restrictedTraverse(
            '@@folderListing', None)
        if listing is None:
            return []
        results = listing(**kwargs)
        return results
