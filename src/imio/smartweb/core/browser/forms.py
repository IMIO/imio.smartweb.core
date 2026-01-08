# -*- coding: utf-8 -*-

from imio.smartweb.common.browser.forms import CustomEditForm
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.contents import ISectionEvents
from imio.smartweb.core.contents import ISectionNews
from imio.smartweb.core.contents import ISectionTimestampedPublications
from imio.smartweb.core.contents import IDefaultPages
from plone.z3cform import layout
from z3c.form.interfaces import DISPLAY_MODE
from zope.schema.vocabulary import getVocabularyRegistry


class SmartwebCustomEditForm(CustomEditForm):
    def updateFields(self):
        super(SmartwebCustomEditForm, self).updateFields()
        if IDefaultPages.providedBy(self.context) or IImioSmartwebMinisite.providedBy(
            self.context
        ):
            # We need to make exclude_from_nav field read only as it is used
            # for default pages to exclude them from sitemap / navigation / ...
            # and for minisites to exclude them as well.
            for group in self.groups:
                if "IExcludeFromNavigation.exclude_from_nav" in group.fields:
                    group.fields["IExcludeFromNavigation.exclude_from_nav"].mode = (
                        DISPLAY_MODE
                    )


SmartwebCustomEditView = layout.wrap_form(SmartwebCustomEditForm)


class SectionBaseCustomEditForm(CustomEditForm):
    """Base form that can clean outdated values in specific_related_events."""

    _interface = None
    _field_name = None

    def _get_adapter(self):
        if self._interface is None:
            return None
        return self._interface(self.context, None)

    def _clean_specific_related_events(self, obj):
        """WEB-4338: Clean missing (outdated) events/news/publications in field : self._field_name."""
        values = list(getattr(obj, self._field_name, None) or [])
        if not values:
            return

        field = self.fields[self._field_name].field
        vt = field.value_type
        vocab = getVocabularyRegistry().get(self.context, vt.vocabularyName)
        kept = []
        for uid in values:
            try:
                vocab.getTerm(uid)
                kept.append(uid)
            except LookupError:
                getattr(obj, self._field_name, None).remove(uid)

    def updateFields(self):
        super(SectionBaseCustomEditForm, self).updateFields()
        obj = self._get_adapter()
        if obj is None:
            return
        self._clean_specific_related_events(obj)


class SectionEventsCustomEditForm(SectionBaseCustomEditForm):
    _interface = ISectionEvents
    _field_name = "specific_related_events"


SectionEventsCustomEditView = layout.wrap_form(SectionEventsCustomEditForm)


class SectionNewsCustomEditForm(SectionBaseCustomEditForm):
    _interface = ISectionNews
    _field_name = "specific_related_newsitems"


SectionNewsCustomEditView = layout.wrap_form(SectionNewsCustomEditForm)


class SectionPublicationsCustomEditForm(SectionBaseCustomEditForm):
    _interface = ISectionTimestampedPublications
    _field_name = "related_timestamped_publications"


SectionPublicationsCustomEditView = layout.wrap_form(SectionPublicationsCustomEditForm)
