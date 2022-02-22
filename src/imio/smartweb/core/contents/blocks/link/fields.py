# -*- coding: utf-8 -*-

from z3c.form.browser.radio import RadioWidget
from z3c.form.interfaces import IRadioWidget
from zope.interface import implementer
from zope.schema import TextLine
from zope.schema.interfaces import ITextLine


class ILinkField(ITextLine):
    """ """


class IIconsRadioWidget(IRadioWidget):
    """ """


@implementer(ILinkField)
class LinkField(TextLine):
    """ """


@implementer(IIconsRadioWidget)
class IconsRadioWidget(RadioWidget):
    """ """
