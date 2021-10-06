# -*- coding: utf-8 -*-

from imio.smartweb.core.contents.sections.base import ISection
from imio.smartweb.core.contents.sections.base import Section
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer


class ISectionNews(ISection):
    """Marker interface and Dexterity Python Schema for SectionNews"""

    description = schema.Text(
        title=_(u"Description"),
        description=_(
            u"Use **text** to set text in bold and *text* to set text in italic."
        ),
        required=False,
    )

    directives.widget(related_news=SelectFieldWidget)
    related_news = schema.Choice(
        title=_(u"Related news"),
        description=_(
            u"Select a news. If you can't find the news you want, make sure "
            u"""it exists in the directory and that its "state" is published."""
        ),
        source="imio.smartweb.vocabulary.RemoteNewsFolders",
        required=True,
    )

    max_nb_results = schema.Int(
        title=_(u"Maximal number of items to display"), default=9, required=True
    )

    nb_results_by_batch = schema.Int(
        title=_(u"Number of items by batch"), default=3, required=True
    )


@implementer(ISectionNews)
class SectionNews(Section):
    """SectionNews class"""
