# -*- coding: utf-8 -*-

from imio.smartweb.common.browser.vocabulary import TranslatedVocabularyView
from plone.app.content.browser.vocabulary import _parseJSON
from plone.app.content.browser.vocabulary import MAX_BATCH_SIZE
from plone.app.content.browser.vocabulary import VocabLookupException
from plone.app.content.utils import json_dumps


# What we return when select2 asks for everything at once (no batch parameter).
# The pattern's default page size is 10, so this only bites a caller that opted
# out of batching.
DEFAULT_PAGE_SIZE = 50


class SmartwebVocabularyView(TranslatedVocabularyView):
    """Word-filtering for the remote vocabularies select2 queries by name.

    ``plone.app.content``'s own view can only filter a source that provides
    ``search()``; these three are plain ``SimpleVocabulary`` instances, so
    without this override a typed query returned the whole list unfiltered
    (SUP-36854).
    """

    filtered_vocabularies = [
        "imio.smartweb.vocabulary.RemoteContacts",
        "imio.smartweb.vocabulary.NewsItemsFromEntity",
        "imio.smartweb.vocabulary.EventsFromEntity",
    ]

    def _batch(self, terms):
        """One page of ``terms``, honoring the pattern's ``batch`` parameter.

        Same contract as ``plone.app.content``, which this view bypasses by
        overriding ``__call__``: select2 sends
        ``batch={"page": n, "size": pageSize}`` and asks for the next page while
        ``pageSize * page < total`` -- so the caller must be told the *unbatched*
        total, or it stops after the first page.
        """
        batch = _parseJSON(self.request.get("batch", ""))
        if not batch or "size" not in batch or "page" not in batch:
            return terms[:DEFAULT_PAGE_SIZE]
        size = min(int(batch["size"]), MAX_BATCH_SIZE)
        start = max(int(batch["page"]) - 1, 0) * size
        return terms[start : start + size]

    def __call__(self):
        form = self.request.form
        name = form.get("name")
        if name not in self.filtered_vocabularies:
            return super(SmartwebVocabularyView, self).__call__()

        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )

        try:
            vocabulary = self.get_vocabulary()
        except VocabLookupException as e:
            return json_dumps({"error": e.args[0]})

        query = form.get("query")
        if not query:
            terms = list(vocabulary)
        else:
            query = query.lower()
            terms = [term for term in vocabulary if query in term.title.lower()]

        # the total is what the whole query matches, not what this page carries
        total = len(terms)
        results = [
            {"id": term.value, "text": term.title} for term in self._batch(terms)
        ]

        return json_dumps({"results": results, "total": total})
