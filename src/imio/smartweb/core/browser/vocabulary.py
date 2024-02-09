# -*- coding: utf-8 -*-
from plone.app.content.browser.vocabulary import VocabularyView
from plone.app.content.browser.vocabulary import VocabLookupException
from plone.app.content.utils import json_dumps


class SmartwebVocabularyView(VocabularyView):

    def __call__(self):
        form = self.request.form
        name = form.get("name")
        if name != "imio.smartweb.vocabulary.RemoteContacts":
            return super(SmartwebVocabularyView, self).__call__()

        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )

        try:
            vocabulary = self.get_vocabulary()
        except VocabLookupException as e:
            return json_dumps({"error": e.args[0]})

        query = form.get("query")
        items = []
        if not query:
            items = vocabulary
        else:
            for term in vocabulary:
                if query.lower() in term.title.lower():
                    items.append(term)

        results = [{"id": item.value, "text": item.title} for item in items]

        return json_dumps({"results": results, "total": len(results)})
