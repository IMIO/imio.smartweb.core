# -*- coding: utf-8 -*-

from App.Undo import decode64
from App.Undo import encode64
from DateTime import DateTime
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.memoize.instance import memoize
from plone.protect import CheckAuthenticator
from Products.Five.browser import BrowserView
from urllib.parse import urlencode

import logging
import transaction

logger = logging.getLogger("imio.smartweb.core")

PAGE_SIZES = (20, 50, 100, 500)
DEFAULT_PAGE_SIZE = PAGE_SIZES[0]


class UndoTransactionsView(BrowserView):
    """Undo ZODB transactions from the Plone site.

    Zope only offers undo on Control_Panel/Database, which is restricted to
    Zope root Managers. This view gives the same feature to Plone Managers.
    """

    @property
    def db(self):
        return self.context._p_jar.db()

    @property
    def b_start(self):
        try:
            return max(int(self.request.form.get("b_start", 0)), 0)
        except (TypeError, ValueError):
            return 0

    @property
    def b_size(self):
        try:
            size = int(self.request.form.get("b_size", DEFAULT_PAGE_SIZE))
        except (TypeError, ValueError):
            return DEFAULT_PAGE_SIZE
        return size if size in PAGE_SIZES else DEFAULT_PAGE_SIZE

    def _url(self, **params):
        url = f"{self.context.absolute_url()}/@@undo-transactions"
        return f"{url}?{urlencode(params)}" if params else url

    def supports_undo(self):
        return self.db.supportsUndo()

    @memoize
    def transactions(self):
        first = self.b_start
        infos = self.db.undoInfo(first, first + self.b_size)
        transactions = [
            {
                "id": encode64(info["id"]).strip(),
                "time": DateTime(info["time"]),
                "user_name": info["user_name"],
                "description": info["description"],
                "checked": False,
            }
            for info in infos
        ]
        # "Select this and newer": check rows from the newest one down to the
        # requested transaction (identified by id, as new commits shift rows)
        select_until = self.request.form.get("select_until")
        ids = [txn["id"] for txn in transactions]
        if select_until in ids:
            for txn in transactions[: ids.index(select_until) + 1]:
                txn["checked"] = True
        return transactions

    def range_not_found(self):
        select_until = self.request.form.get("select_until")
        if not select_until:
            return False
        return select_until not in [txn["id"] for txn in self.transactions()]

    def select_range_url(self, index):
        position = self.b_start + index
        if position >= PAGE_SIZES[-1]:
            return None
        size = min(s for s in PAGE_SIZES if s >= max(position + 1, self.b_size))
        tid = self.transactions()[index]["id"]
        return self._url(b_start=0, b_size=size, select_until=tid)

    def page_sizes(self):
        return [
            {
                "size": size,
                "url": self._url(b_size=size),
                "current": size == self.b_size,
            }
            for size in PAGE_SIZES
        ]

    def previous_url(self):
        if self.b_start == 0:
            return None
        start = max(self.b_start - self.b_size, 0)
        return self._url(b_start=start, b_size=self.b_size)

    def next_url(self, transactions):
        if len(transactions) < self.b_size:
            return None
        return self._url(b_start=self.b_start + self.b_size, b_size=self.b_size)

    def __call__(self):
        if self.request.method == "POST" and "form.buttons.undo" in self.request.form:
            self.undo()
            self.request.response.redirect(self._url(b_size=self.b_size))
            return ""
        return self.index()

    def undo(self):
        CheckAuthenticator(self.request)
        ids = self.request.form.get("transaction_ids", [])
        if isinstance(ids, str):
            ids = [ids]
        if not ids:
            api.portal.show_message(
                _("No transaction selected."), self.request, type="warning"
            )
            return
        tids = [decode64(tid) for tid in ids]
        txn = transaction.get()
        txn.note(f"Undo {len(tids)} transaction(s)")
        self.db.undoMultiple(tids)
        try:
            txn.commit()
        except Exception as exc:
            txn.abort()
            logger.warning("Undo failed: %s", exc)
            api.portal.show_message(
                _(
                    "Undo failed: ${error}",
                    mapping={"error": f"{exc.__class__.__name__}: {exc}"},
                ),
                self.request,
                type="error",
            )
            return
        user = api.user.get_current().getUserName()
        logger.info("%s undid %s transaction(s)", user, len(tids))
        api.portal.show_message(_("Transactions undone."), self.request)
