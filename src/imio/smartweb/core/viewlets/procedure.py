# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import common
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class ProcedureViewlet(common.ViewletBase):
    def get_selected_procedure_title(self):
        if self.context.procedure_ts is None:
            return
        factory = getUtility(
            IVocabularyFactory, "imio.smartweb.vocabulary.PublikProcedures"
        )
        vocabulary = factory()
        term = vocabulary.getTerm(self.context.procedure_ts)
        return term

    @property
    def is_anonymous(self):
        return self.portal_state.anonymous()

    def get_button_label(self):
        if self.context.button_ts_label is None:
            return "Complete this procedure online"
        factory = getUtility(
            IVocabularyFactory, "imio.smartweb.vocabulary.ProcedureButtonLabels"
        )
        vocabulary = factory()
        try:
            term = vocabulary.getTerm(self.context.button_ts_label)
        except LookupError:
            # If the term is not found, return a default label
            return "Complete this procedure online"
        return term.title
