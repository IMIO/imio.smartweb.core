# -*- coding: utf-8 -*-
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Item

# from plone.namedfile import field as namedfile
from plone.supermodel import model

# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
from zope.interface import implementer


from imio.smartweb.core import _


class IProcedure(model.Schema):
    """Marker interface and Dexterity Python Schema for Procedure"""


@implementer(IProcedure)
class Procedure(Item):
    """"""
