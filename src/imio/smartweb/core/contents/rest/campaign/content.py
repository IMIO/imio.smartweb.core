# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import RestView
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


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
