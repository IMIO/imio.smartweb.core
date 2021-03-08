# -*- coding: utf-8 -*-
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.component import getUtility
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def sections_all_values(context):
    factory = getUtility(
        IVocabularyFactory, "imio.smartweb.vocabulary.PageSections"
    )
    vocabulary = factory(context)
    return [t.value for t in vocabulary]


@provider(IFormFieldProvider)
class IPageSections(model.Schema):
    """"""

    visible_sections = schema.List(
        title=_(u"Visible sections"),
        description=_(u"Sections that will be displayed in page and listing view"),
        value_type=schema.Choice(vocabulary="imio.smartweb.vocabulary.PageSections"),
        defaultFactory=sections_all_values,
    )
