# -*- coding: utf-8 -*-

from imio.smartweb.common.faceted.utils import configure_faceted
from imio.smartweb.common.utils import is_log_active
from imio.smartweb.common.utils import remove_cropping
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.utils import safe_html
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.imagecropping import PAI_STORAGE_KEY
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.namedfile.field import NamedBlobImage
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.lifecycleevent import ObjectRemovedEvent
from zope.lifecycleevent.interfaces import IAttributes
from zope.globalrequest import getRequest
from zope.schema import getFields

import logging
import os

logger = logging.getLogger("imio.smartweb.core")


def moved_folder(obj, event):
    """We use IObjectMovedEvent instead of IObjectAddedEvent because Minisite interface is not yet
    provided when we use IObjectAddedEvent"""
    if not IImioSmartwebMinisite.providedBy(obj):
        return
    if type(event) is ObjectRemovedEvent:
        # We don't have anything to do if minisite is being removed
        return
    parent = event.newParent
    if INavigationRoot.providedBy(parent):
        # Minisites must always be under navigation root
        if not IImioSmartwebMinisite.providedBy(parent):
            # We are not in another minisite, everything is good
            return
    request = getRequest()
    minisite_settings = getMultiAdapter((obj, request), name="minisite_settings")
    minisite_settings.disable()
    api.portal.show_message(
        _(
            "Your Folder was a minisite but this behaviour has been disabled with this action"
        ),
        request,
        type="warning",
    )


def added_collection(obj, event):
    faceted_config_path = "{}/faceted/config/collection.xml".format(
        os.path.dirname(__file__)
    )
    configure_faceted(obj, faceted_config_path)


def added_sectionhtml(obj, event):
    obj.html = safe_html(obj.html)


def modified_sectionhtml(obj, event):
    obj.html = safe_html(obj.html)


def check_image_field(obj, interface, class_name, field_name):
    """Check if the field is an image field to see if we have cropping
    information to remove"""
    if field_name.startswith(f"{class_name}."):
        field_name = field_name.split(".")[-1]
    fields = getFields(interface)
    if field_name not in fields:
        # strange! the field is not found in schema class
        logger.warning(f"{field_name} not found in {interface.__identifier__}")
        return
    field = fields[field_name]
    if not isinstance(field, NamedBlobImage):
        # the field is not an image, nothing to do
        return
    annotations = IAnnotations(obj)
    scales = annotations.get(PAI_STORAGE_KEY)
    if scales is None:
        return
    scales_to_purge = []
    for scale in scales:
        if scale.startswith(field_name):
            scale_suffix = scale.split(f"{field_name}_")[-1]
            scales_to_purge.append(scale_suffix)
    if scales_to_purge:
        remove_cropping(obj, field_name, scales_to_purge)
        if is_log_active():
            logger.info(f"{scales_to_purge} croppings were PURGED for {field_name} !")
    elif is_log_active():
        logger.info(f"No existing cropping to purge for {field_name}.")


def modified_content(obj, event):
    if not hasattr(event, "descriptions") or not event.descriptions:
        return
    for d in event.descriptions:
        if not IAttributes.providedBy(d):
            # we do not have fields change description, but maybe a request
            continue

        class_name = d.interface.__identifier__.split(".")[-1]
        for field_name in d.attributes:
            check_image_field(obj, d.interface, class_name, field_name)
