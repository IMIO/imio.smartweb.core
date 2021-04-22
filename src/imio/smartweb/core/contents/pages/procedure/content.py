# -*- coding: utf-8 -*-

from imio.smartweb.core.contents import IPages
from imio.smartweb.core.contents import Pages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import implementer
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider

CATEGORY_TAXONOMY = "collective.taxonomy.procedure"


@provider(IFormFieldProvider)
class IProcedure(IPages):
    """"""

    procedure_ts = schema.Choice(
        vocabulary="imio.smartweb.vocabulary.PublikProcedures",
        title=_(u"E-Guichet procedure"),
        required=False,
        default=None,
    )

    procedure_url = schema.URI(title=_(u"Procedure url"), required=False)
    category = schema.Choice(
        title=_(u"Category"),
        source=CATEGORY_TAXONOMY,
        required=False,
    )

    @invariant
    def required_procedure(data):
        # if data.procedure_ts is None and data.procedure_url is None:
        #     raise Invalid(_(u"Procedure field is required !"))

        if data.procedure_ts and data.procedure_url:
            raise Invalid(_(u"Only one procedure field can be filled !"))


@implementer(IProcedure)
class Procedure(Pages):
    """Procedure class"""

    category_taxonomy = CATEGORY_TAXONOMY
