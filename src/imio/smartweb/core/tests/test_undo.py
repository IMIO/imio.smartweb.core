# -*- coding: utf-8 -*-

from AccessControl.unauthorized import Unauthorized
from App.Undo import encode64
from imio.smartweb.core.browser.undo import UndoTransactionsView
from imio.smartweb.core.interfaces import IImioSmartwebCoreLayer
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.protect.authenticator import createToken
from Products.statusmessages.interfaces import IStatusMessage
from urllib.parse import urlencode
from zExceptions import Forbidden
from ZODB.POSException import UndoError
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

import mock


def transaction_info(index):
    return {
        "id": f"tid-{index}".encode(),
        "time": 1700000000.0 + index,
        "user_name": "/Plone admin",
        "description": f"/Plone/page-{index}/edit",
    }


class TestUndoTransactionsView(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        alsoProvides(self.request, IImioSmartwebCoreLayer)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.db = mock.Mock()
        self.db.supportsUndo.return_value = True
        self.db.undoInfo.return_value = [transaction_info(1)]
        patcher = mock.patch.object(
            UndoTransactionsView, "db", new_callable=mock.PropertyMock
        )
        patcher.start().return_value = self.db
        self.addCleanup(patcher.stop)

    def get_view(self):
        return getMultiAdapter((self.portal, self.request), name="undo-transactions")

    def post_undo(self, ids, token=True):
        self.request.method = "POST"
        self.request.form["form.buttons.undo"] = "Undo"
        self.request.form["transaction_ids"] = ids
        if token:
            self.request.form["_authenticator"] = createToken()
        return self.get_view()()

    def messages(self):
        return [(str(m.message), m.type) for m in IStatusMessage(self.request).show()]

    def test_view_is_restricted_to_managers(self):
        self.assertIsNotNone(self.portal.restrictedTraverse("@@undo-transactions"))
        setRoles(self.portal, TEST_USER_ID, ["Site Administrator"])
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse("@@undo-transactions")
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse("@@undo-transactions")

    def test_undo_not_supported(self):
        self.db.supportsUndo.return_value = False
        html = self.get_view()()
        self.assertIn("This database does not support undo.", html)
        self.assertNotIn("form.buttons.undo", html)

    def test_list_transactions(self):
        html = self.get_view()()
        self.assertIn("/Plone/page-1/edit", html)
        self.assertIn("/Plone admin", html)
        self.assertIn(encode64(b"tid-1").strip(), html)
        self.assertIn("form.buttons.undo", html)
        self.assertIn("pat-checklist", html)
        self.assertIn("toggle-all", html)
        self.db.undoInfo.assert_called_once_with(0, 20)

    def test_batching(self):
        url = f"{self.portal.absolute_url()}/@@undo-transactions"
        view = self.get_view()
        self.assertIsNone(view.previous_url())
        self.assertIsNone(view.next_url(view.transactions()))
        transactions = [{"id": str(i)} for i in range(20)]
        self.assertEqual(view.next_url(transactions), f"{url}?b_start=20&b_size=20")

        self.request.form["b_start"] = "40"
        view = self.get_view()
        view.transactions()
        self.db.undoInfo.assert_called_with(40, 60)
        self.assertEqual(view.previous_url(), f"{url}?b_start=20&b_size=20")

        self.request.form["b_start"] = "not-a-number"
        self.assertEqual(self.get_view().b_start, 0)

    def test_page_size(self):
        url = f"{self.portal.absolute_url()}/@@undo-transactions"
        self.request.form["b_size"] = "50"
        view = self.get_view()
        self.assertEqual(view.b_size, 50)
        view.transactions()
        self.db.undoInfo.assert_called_with(0, 50)
        self.request.form["b_start"] = "100"
        self.assertEqual(self.get_view().previous_url(), f"{url}?b_start=50&b_size=50")
        for invalid in ("1000", "abc", "0"):
            self.request.form["b_size"] = invalid
            self.assertEqual(self.get_view().b_size, 20)

    def test_page_size_links(self):
        self.request.form["b_size"] = "100"
        view = self.get_view()
        self.assertEqual(
            [(p["size"], p["current"]) for p in view.page_sizes()],
            [(20, False), (50, False), (100, True), (500, False)],
        )
        html = view()
        url = f"{self.portal.absolute_url()}/@@undo-transactions"
        for size in (20, 50, 100, 500):
            self.assertIn(f'href="{url}?b_size={size}"', html)
        self.assertEqual(html.count('aria-current="true"'), 1)
        self.assertIn('name="b_size" value="100"', html)

    def test_select_range_url(self):
        url = f"{self.portal.absolute_url()}/@@undo-transactions"
        self.db.undoInfo.return_value = [transaction_info(i) for i in range(20)]
        self.request.form["b_start"] = "20"
        view = self.get_view()
        tid = view.transactions()[5]["id"]
        self.assertEqual(
            view.select_range_url(5),
            f"{url}?{urlencode(dict(b_start=0, b_size=50, select_until=tid))}",
        )

        self.request.form["b_start"] = "0"
        self.request.form["b_size"] = "100"
        view = self.get_view()
        self.assertIn("b_size=100&", view.select_range_url(3))

        self.request.form["b_start"] = "500"
        self.request.form["b_size"] = "500"
        self.assertIsNone(self.get_view().select_range_url(0))

    def test_select_until_preselects_newer_transactions(self):
        self.db.undoInfo.return_value = [transaction_info(i) for i in range(5)]
        self.request.form["select_until"] = encode64(b"tid-2").strip()
        view = self.get_view()
        self.assertEqual(
            [txn["checked"] for txn in view.transactions()],
            [True, True, True, False, False],
        )
        self.assertFalse(view.range_not_found())
        html = view()
        self.assertEqual(html.count('checked="checked"'), 3)
        self.assertNotIn("no longer in the list", html)

    def test_select_until_not_found(self):
        self.db.undoInfo.return_value = [transaction_info(i) for i in range(5)]
        self.request.form["select_until"] = encode64(b"unknown").strip()
        view = self.get_view()
        self.assertTrue(view.range_not_found())
        self.assertFalse(any(txn["checked"] for txn in view.transactions()))
        html = view()
        self.assertIn("The selected transaction is no longer in the list.", html)
        self.assertNotIn('checked="checked"', html)

    @mock.patch("imio.smartweb.core.browser.undo.transaction")
    def test_undo_transactions(self, transaction):
        txn = transaction.get.return_value
        self.post_undo([encode64(b"tid-1"), encode64(b"tid-2")])
        self.db.undoMultiple.assert_called_once_with([b"tid-1", b"tid-2"])
        txn.note.assert_called_once_with("Undo 2 transaction(s)")
        txn.commit.assert_called_once_with()
        txn.abort.assert_not_called()
        self.assertEqual(self.messages(), [("Transactions undone.", "info")])
        self.assertEqual(
            self.request.response.getHeader("Location"),
            f"{self.portal.absolute_url()}/@@undo-transactions?b_size=20",
        )

    @mock.patch("imio.smartweb.core.browser.undo.transaction")
    def test_undo_keeps_page_size(self, transaction):
        self.request.form["b_size"] = "500"
        self.post_undo([encode64(b"tid-1")])
        self.assertEqual(
            self.request.response.getHeader("Location"),
            f"{self.portal.absolute_url()}/@@undo-transactions?b_size=500",
        )

    @mock.patch("imio.smartweb.core.browser.undo.transaction")
    def test_undo_single_transaction(self, transaction):
        self.post_undo(encode64(b"tid-1"))
        self.db.undoMultiple.assert_called_once_with([b"tid-1"])

    @mock.patch("imio.smartweb.core.browser.undo.transaction")
    def test_undo_error(self, transaction):
        txn = transaction.get.return_value
        txn.commit.side_effect = UndoError("Data modified by a later transaction")
        self.post_undo([encode64(b"tid-1")])
        txn.abort.assert_called_once_with()
        messages = self.messages()
        self.assertEqual(len(messages), 1)
        self.assertTrue(messages[0][0].startswith("Undo failed: UndoError:"))
        self.assertIn("Data modified by a later transaction", messages[0][0])
        self.assertEqual(messages[0][1], "error")

    @mock.patch("imio.smartweb.core.browser.undo.transaction")
    def test_undo_nothing_selected(self, transaction):
        self.post_undo([])
        self.db.undoMultiple.assert_not_called()
        self.assertEqual(self.messages(), [("No transaction selected.", "warning")])

    def test_undo_requires_authenticator(self):
        with self.assertRaises(Forbidden):
            self.post_undo([encode64(b"tid-1")], token=False)
        self.db.undoMultiple.assert_not_called()
