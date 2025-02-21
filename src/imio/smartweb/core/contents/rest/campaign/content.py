# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import RestView
from imio.smartweb.core.utils import get_basic_auth_json
from imio.smartweb.core.utils import get_ts_api_url
from imio.smartweb.core.utils import get_value_from_registry
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.content.namechooser import NormalizingNameChooser
from plone.i18n.normalizer import idnormalizer
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

    propose_project_url = schema.TextLine(
        title=_("Propose project URL"),
        description=_("URL to propose a project"),
        required=False,
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
        """Génère un ID basé sur le titre récupéré de l'API."""
        if ICampaignView.providedBy(obj):
            if not obj.title:
                # Récupération du titre via l'API
                wcs_api = get_ts_api_url("wcs")
                ts_campaign_endpoint = "imio-ideabox-campagne"
                url = f"{wcs_api}/cards/{ts_campaign_endpoint}/{obj.linked_campaign}"
                user = get_value_from_registry("smartweb.iaideabox_api_username")
                pwd = get_value_from_registry("smartweb.iaideabox_api_password")
                json_campaign = get_basic_auth_json(url, user, pwd)

                if json_campaign and "fields" in json_campaign:
                    obj.title = json_campaign["fields"].get(
                        "titre", "campagne-sans-nom"
                    )
                else:
                    obj.title = "campaign-without-name"

            # Normaliser l'ID en utilisant le titre
            normalized_id = idnormalizer.normalize(obj.title)

            # Vérifier que l'ID généré est bien unique dans le conteneur
            return super().chooseName(normalized_id, obj)

        return super().chooseName(name, obj)
