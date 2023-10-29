# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from imio.smartweb.core.contents import IFolder
from imio.smartweb.core.interfaces import IViewWithoutLeadImage
from imio.smartweb.core.utils import get_scale_url
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.content.browser.contents import ContextInfo
from plone.app.content.utils import json_dumps
from plone.app.content.utils import json_loads
from plone.app.contenttypes.browser.folder import FolderView as BaseFolderView
from plone.app.contenttypes.interfaces import ICollection
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.contentprovider import ContentProviders
from z3c.form.field import Fields
from z3c.form.form import EditForm
from z3c.form.interfaces import IFieldsAndContentProvidersForm
from zope.component import queryMultiAdapter
from zope.contentprovider.provider import ContentProviderBase
from zope.interface import implementer


class FolderContextInfo(ContextInfo):
    """View used to fetch informations for folder_contents"""

    def __call__(self):
        json = super(FolderContextInfo, self).__call__()
        brain = self.context.get_default_item()
        if brain:
            infos = json_loads(json)
            infos["defaultPage"] = brain.getId
            json = json_dumps(infos)
        return json


@implementer(IViewWithoutLeadImage)
class FolderView(BaseFolderView):
    """ """

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
        return listing(**kwargs)

    def blocks_results(self, **kwargs):
        """
        Gets results for blocks folder view, combining standard folder listing
        results and quick access contents (without duplicates)
        """
        results = self.results(batch=False)
        if self.context.quick_access_items is None:
            return {"results": results, "quick_access": []}
        quick_access_uids = [
            item.to_object.UID()
            for item in self.context.quick_access_items
            if item.isBroken() is False
        ]
        quick_access_brains = api.content.find(
            UID=quick_access_uids,
            sort_on="sortable_title",
        )
        paths = [item.getPath() for item in results]
        # Use path instead of uuid in comparison because uuid can wake up object.
        quick_access_brains = [
            brain for brain in quick_access_brains if brain.getPath() not in paths
        ]
        return {"results": results, "quick_access": quick_access_brains}

    def get_scale_url(self, item, scale):
        request = self.request
        orientation = self.context.orientation
        return get_scale_url(item, request, "image", scale, orientation)


@implementer(IViewWithoutLeadImage)
class FolderViewWithImages(FolderView):
    """ """

    show_images = True


class DefaultElementTextView(ContentProviderBase):
    render = ViewPageTemplateFile("element_view.pt")


@implementer(IFieldsAndContentProvidersForm, IViewWithoutLeadImage)
class ElementView(EditForm):
    """ """

    label = _("Form to choose item to be displayed as the home page of the folder")
    contentProviders = ContentProviders()
    contentProviders["defaultElementText"] = DefaultElementTextView
    contentProviders["defaultElementText"].position = 0

    def __call__(self):
        if api.user.is_anonymous():
            default_item = self.context.get_default_item(object=True)
            if default_item:
                # we choose the view depending on content type (pages or collection)
                view_name = (
                    ICollection.providedBy(default_item)
                    and "facetednavigation_view"
                    or "full_view"
                )
                return queryMultiAdapter((default_item, self.request), name=view_name)()
            # Element view with no default item selected -> fallback to summary_view
            return queryMultiAdapter(
                (self.context, self.request), name="summary_view"
            )()
        return super(ElementView, self).__call__()

    @property
    def fields(self):
        fields = Fields(IFolder).select("default_page_uid")
        fields["default_page_uid"].required = True
        fields["default_page_uid"].widgetFactory = RadioFieldWidget
        return fields

    @button.buttonAndHandler(_("Apply"), name="apply")
    def handleApply(self, action):
        data, errors = self.extractData()
        old_default_page = self.context.get_default_item(object=True)
        changes = self.applyChanges(data)
        if changes:
            self.context.set_default_item(old_default_item=old_default_page)
            self.status = self.successMessage
        else:
            self.status = self.noChangesMessage


@implementer(IViewWithoutLeadImage)
class SummaryView(FolderView):
    """ """

    show_images = False


@implementer(IViewWithoutLeadImage)
class SummaryViewWithImages(SummaryView):
    """ """

    show_images = True
