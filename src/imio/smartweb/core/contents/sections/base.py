# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class ISection(model.Schema):
    """ Shared mecanism for sections """

    title = schema.TextLine(title=_(u"Title"), required=True)
    hide_title = schema.Bool(title=_(u"Hide title"), required=False, default=False)
    model.fieldset("settings", fields=["css_class"])
    css_class = schema.TextLine(title=_(u"CSS class"), required=False)


@implementer(ISection)
class Section(Container):
    """ Shared mecanism for sections """

    @property
    def get_last_mofication_date(self):
        return self.ModificationDate()
