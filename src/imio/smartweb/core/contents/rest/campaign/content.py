# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import RestView
from imio.smartweb.core.utils import get_basic_auth_json
from imio.smartweb.core.utils import get_ts_api_url
from imio.smartweb.core.utils import get_value_from_registry
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.content.namechooser import NormalizingNameChooser
from plone.i18n.normalizer.interfaces import IURLNormalizer
from plone.supermodel import model
from zope import schema
from zope.component import getUtility
from zope.container.interfaces import INameChooser
from zope.interface import implementer

import logging

logger = logging.getLogger("imio.smartweb.core")


class ICampaignView(model.Schema):
    """ """

    linked_campaign = schema.Choice(
        vocabulary="imio.smartweb.vocabulary.PublikCampaigns",
        title=_("E-Guichet campaign"),
        required=False,
        default=None,
    )

    nb_results = schema.Int(
        title=_("Number of items to display"), default=20, required=True
    )

    display_map = schema.Bool(
        title=_("Display map"),
        description=_("If selected, map will be displayed"),
        required=False,
        default=True,
    )


@implementer(ICampaignView, IInstanceBehaviorAssignableContent)
class CampaignView(RestView):
    """Campaign class"""


@implementer(INameChooser)
class CampaignNameChooser(NormalizingNameChooser):
    def chooseName(self, name, obj):
        if ICampaignView.providedBy(obj):
            # Order in test : added subscriber > chooseName !!
            # order in instance : chooseName > added subscriber ??
            if not obj.title:
                wcs_api = get_ts_api_url("wcs")
                ts_campaign_endpoint = "imio-ideabox-campagne"
                url = f"{wcs_api}/cards/{ts_campaign_endpoint}/{obj.linked_campaign}"
                user = get_value_from_registry("smartweb.iaideabox_api_username")
                pwd = get_value_from_registry("smartweb.iaideabox_api_password")
                json_campaign = get_basic_auth_json(url, user, pwd)
                obj.title = json_campaign.get("fields").get("titre")
            normalized_id = super(CampaignNameChooser, self).chooseName(obj.title, obj)
            return normalized_id
        return super(CampaignNameChooser, self).chooseName(name, obj)
