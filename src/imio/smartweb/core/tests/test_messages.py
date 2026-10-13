# -*- coding: utf-8 -*-

from collective.messagesviewlet.utils import add_message
from imio.smartweb.core.behaviors.eguichet_message import IEguichetMessage
from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.restapi.testing import RelativeSession

import transaction


class TestMessagesGet(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_ACCEPTANCE_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        # anonymous session : messages must be exposed to everyone
        self.api_session = RelativeSession(self.portal.absolute_url())
        self.api_session.headers.update({"Accept": "application/json"})
        add_message(
            "visible",
            "Visible message",
            "<p>Hello</p>",
            msg_type="warning",
            activate=True,
        )
        add_message(
            "not-in-eguichet",
            "Message not displayed in e-guichet",
            "<p>Not in e-guichet</p>",
            activate=True,
        )
        add_message("inactive", "Inactive message", "<p>Inactive</p>")
        add_message(
            "with-roles",
            "Message with roles",
            "<p>Roles</p>",
            req_roles=["Manager"],
            activate=True,
        )
        add_message(
            "with-local-roles",
            "Message with local roles",
            "<p>Local roles</p>",
            use_local_roles=True,
            activate=True,
        )
        add_message(
            "with-tal",
            "Message with TAL condition",
            "<p>TAL</p>",
            tal_condition="python:True",
            activate=True,
        )
        folder = api.content.create(
            container=self.portal, type="imio.smartweb.Folder", title="Folder"
        )
        in_folder = add_message(
            "in-folder",
            "Message in folder",
            "<p>Folder</p>",
            location="fromhere",
            activate=True,
            container=folder,
        )
        # every message is marked for e-guichet, except one, so that each
        # exclusion is only due to the tested constraint
        for message in list(self.portal["messages-config"].objectValues()) + [
            in_folder
        ]:
            if message.getId() != "not-in-eguichet":
                IEguichetMessage(message).eguichet_display_message = True
        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    def test_reply(self):
        response = self.api_session.get("@messages")
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertEqual(json["items_total"], 1)
        message = json["items"][0]
        self.assertEqual(
            sorted(message.keys()), ["end", "msg_type", "start", "text", "title"]
        )
        self.assertEqual(message["title"], "Visible message")
        self.assertEqual(message["text"], "<p>Hello</p>")
        self.assertEqual(message["msg_type"], "warning")
        self.assertIsNotNone(message["start"])
        self.assertIsNone(message["end"])
