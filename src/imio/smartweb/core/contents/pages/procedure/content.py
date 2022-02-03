# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider


@provider(IFormFieldProvider)
class IProcedure(IPages):
    """ """

    procedure_ts = schema.Choice(
        vocabulary="imio.smartweb.vocabulary.PublikProcedures",
        title=_("E-Guichet procedure"),
        required=False,
        default=None,
    )

    procedure_url = schema.URI(title=_("Procedure url"), required=False)

    @invariant
    def required_procedure(data):
        # if data.procedure_ts is None and data.procedure_url is None:
        #     raise Invalid(_(u"Procedure field is required !"))

        if data.procedure_ts and data.procedure_url:
            raise Invalid(_("Only one procedure field can be filled !"))


@implementer(IProcedure, IInstanceBehaviorAssignableContent)
class Procedure(Pages):
    """Procedure class"""

    category_name = "procedure_category"
