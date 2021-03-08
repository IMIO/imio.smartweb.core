# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from plone.app.contenttypes.browser.folder import FolderView as BaseFolderView


class FolderView(BaseFolderView):
    """"""

    def results(self, **kwargs):
        """
        Gets results for folder listings with exclude_from_parent_listing into
        filters
        """
        # Extra filter
        kwargs.update(self.request.get("contentFilter", {}))
        kwargs.setdefault("batch", True)
        kwargs.setdefault("b_size", self.b_size)
        kwargs.setdefault("b_start", self.b_start)
        kwargs.setdefault("orphan", 1)
        kwargs.setdefault("exclude_from_parent_listing", False)

        listing = aq_inner(self.context).restrictedTraverse("@@folderListing", None)
        if listing is None:
            return []
        results = listing(**kwargs)
        return results

    def blocks_results(self, **kwargs):
        """
        Gets results for blocks folder view, combining standard folder listing
        results and quick access contents (without duplicates)
        """
        results = self.results(batch=False)
        quick_access_brains = api.content.find(
            context=self.context,
            include_in_quick_access=True,
            sort_on="sortable_title",
        )
        paths = [item.getPath() for item in results]
        # Use path instead of uuid in comparison because uuid can wake up object.
        quick_access_brains = [
            brain for brain in quick_access_brains if brain.getPath() not in paths
        ]
        return {"results": results, "quick_access": quick_access_brains}
