# -*- coding: utf-8 -*-

from imio.smartweb.common.utils import get_vocabulary
from imio.smartweb.core.contents import IPage
from imio.smartweb.core.contents import IProcedure
from Products.Five.browser import BrowserView


class UtilsView(BrowserView):
    """ """

    def is_instancebehaviors_assignable_content(self):
        instance_behaviors_voc = get_vocabulary(
            "imio.smartweb.vocabulary.AvailableInstanceBehaviors"
        )
        if len(instance_behaviors_voc) == 0:
            return False
        return IPage.providedBy(self.context) or IProcedure.providedBy(self.context)
