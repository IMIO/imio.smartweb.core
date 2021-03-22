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
