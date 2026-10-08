# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from collective.behavior.talcondition.behavior import ITALCondition
from collective.messagesviewlet.messagesconfig import MessagesConfig
from imio.smartweb.core.behaviors.eguichet_message import IEguichetMessage
from plone import api
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from Products.CMFPlone.interfaces import IPloneSiteRoot


def is_root_message(message):
    """A message is at the root when it lives in the site or in messages-config"""
    container = aq_parent(message)
    return IPloneSiteRoot.providedBy(container) or isinstance(container, MessagesConfig)


def is_unconstrained_message(message):
    """A message has no constraint when it is not restricted to roles,
    to local roles or to a TAL expression"""
    if message.required_roles or message.use_local_roles:
        return False
    tal_condition = ITALCondition(message).tal_condition or ""
    return not tal_condition.strip()


def is_eguichet_message(message):
    """A message is exposed only when it is marked to be displayed in e-guichet"""
    if not IEguichetMessage.providedBy(message):
        return False
    return bool(message.eguichet_display_message)


class MessagesGet(Service):
    """Expose activated (published) messages located at the site root that
    have no role / local role / TAL expression constraint and that are marked
    to be displayed in e-guichet.
    Messages are not viewable by anonymous users (message_workflow), so we
    search unrestrictedly, as collective.messagesviewlet does."""

    def reply(self):
        catalog = api.portal.get_tool("portal_catalog")
        brains = catalog.unrestrictedSearchResults(
            portal_type="Message",
            review_state="activated",
            sort_on="getObjPositionInParent",
        )
        items = []
        for brain in brains:
            message = brain._unrestrictedGetObject()
            if not is_root_message(message):
                continue
            if not is_unconstrained_message(message):
                continue
            if not is_eguichet_message(message):
                continue
            items.append(self.serialize(message))
        return {"items": items, "items_total": len(items)}

    def serialize(self, message):
        text = message.text
        return {
            "title": message.title,
            "text": text.output_relative_to(message) if text else "",
            "msg_type": message.msg_type,
            "start": json_compatible(message.start),
            "end": json_compatible(message.end),
        }
