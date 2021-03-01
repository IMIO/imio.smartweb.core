# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from zope import schema
from plone.autoform import directives

# from imio.behavior.teleservices.widgets import SelectProcedureWidget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider


@provider(IFormFieldProvider)
class IProcedure(model.Schema):
    """"""

    # directives.widget("procedures", SelectProcedureWidget)
    procedure_ts = schema.Choice(
        vocabulary="imio.smartweb.vocabulary.PublikProcedures",
        title=_(u"E-Guichet procedure"),
        required=False,
        default=None,
    )

    procedure_url = schema.URI(title=_(u"Procedure url"), required=False)

    @invariant
    def required_procedure(data):
        if data.procedure_ts is None and data.procedure_url is None:
            raise Invalid(_(u"Procedure field is required !"))

        if data.procedure_ts and data.procedure_url:
            raise Invalid(_(u"Only one procedure field can be filled !"))
