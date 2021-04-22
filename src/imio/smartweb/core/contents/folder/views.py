# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from imio.smartweb.core.contents import IFolder
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.contenttypes.browser.folder import FolderView as BaseFolderView
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ISiteSchema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.contentprovider import ContentProviders
from z3c.form.field import Fields
from z3c.form.form import EditForm
from z3c.form.interfaces import IFieldsAndContentProvidersForm
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.contentprovider.provider import ContentProviderBase
from zope.interface import implementer


class FolderView(BaseFolderView):
    """"""

    show_images = False

    def results(self, **kwargs):
        """
        Gets results for folder listings with exclude_from_parent_listing into
        filters and without taking care of friendly_types
        """
        # Extra filter
        kwargs.update(self.request.get("contentFilter", {}))
        kwargs.setdefault("batch", True)
        kwargs.setdefault("b_size", self.b_size)
        kwargs.setdefault("b_start", self.b_start)
        kwargs.setdefault("orphan", 1)
        kwargs.setdefault("exclude_from_parent_listing", False)

        listing = aq_inner(self.context).restrictedTraverse("@@folderListing", None)
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


class FolderViewWithImages(FolderView):
    """"""

    show_images = True

    def get_thumb_scale(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISiteSchema, prefix="plone", check=False)
        if settings.no_thumbs_summary:
            return None
        return settings.thumb_scale_summary


class DefaultElementTextView(ContentProviderBase):
    render = ViewPageTemplateFile("element_view.pt")


@implementer(IFieldsAndContentProvidersForm)
class ElementView(EditForm):
    """"""

    label = _(u"Element view form")
    # description = _(u"Choose an item as your default folder view")
    contentProviders = ContentProviders()
    contentProviders["defaultElementText"] = DefaultElementTextView
    contentProviders["defaultElementText"].position = 0

    def __call__(self):
        if api.user.is_anonymous():
            default_item = self.context.get_default_item(object=True)
            if default_item:
                return queryMultiAdapter(
                    (default_item, self.request), name="full_view"
                )()
            # Element view with no default item selected -> fallback to summary_view
            return queryMultiAdapter(
                (self.context, self.request), name="summary_view"
            )()
        return super(ElementView, self).__call__()

    @property
    def fields(self):
        fields = Fields(IFolder).select(
            "default_page_uid",
        )
        fields["default_page_uid"].required = True
        fields["default_page_uid"].widgetFactory = RadioFieldWidget
        return fields

    @button.buttonAndHandler(_("Apply"), name="apply")
    def handleApply(self, action):
        data, errors = self.extractData()
        old_default_page = self.context.get_default_item(object=True)
        changes = self.applyChanges(data)
        if changes:
            self.context.set_default_item(old_default_page)
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage


class SummaryView(FolderView):
    """"""

    show_images = False


class SummaryViewWithImages(SummaryView):
    """"""

    show_images = True
