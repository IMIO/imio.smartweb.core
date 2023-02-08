# -*- coding: utf-8 -*-

from imio.smartweb.core.testing import IMIO_SMARTWEB_CORE_INTEGRATION_TESTING
from imio.smartweb.core.testing import ImioSmartwebTestCase
from imio.smartweb.core.viewlets.chatbot import ChatbotViewlet
from unittest import mock

import os


class TestChatbot(ImioSmartwebTestCase):
    layer = IMIO_SMARTWEB_CORE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests"""
        self.request = self.layer["request"]
        self.portal = self.layer["portal"]

    @mock.patch.dict(os.environ, {"CHATBOT_URL": "", "CHATBOT_ID": ""})
    def test_nochatbot(self):
        viewlet = ChatbotViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertFalse(viewlet.available)

    @mock.patch.dict(
        os.environ, {"CHATBOT_URL": "https://testurl", "CHATBOT_ID": "test-id"}
    )
    def test_chatbot(self):
        viewlet = ChatbotViewlet(self.portal, self.request, None, None)
        viewlet.update()
        self.assertTrue(viewlet.available)
        self.assertEqual(viewlet.chatbot_url, "https://testurl")
        self.assertEqual(viewlet.chatbot_id, "test-id")
