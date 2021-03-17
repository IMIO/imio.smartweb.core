# -*- coding: utf-8 -*-

from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.supermodel import model
from zope import schema


class ISection(model.Schema):
    """ Shared mecanism for sections """
    title = schema.TextLine(
        title=_(u'label_title', default=u'Title'),
        required=True
    )


class Section():
    """ Shared mecanism for sections """
