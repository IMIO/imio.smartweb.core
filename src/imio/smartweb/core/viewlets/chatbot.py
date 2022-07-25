# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import common

import os


class ChatbotViewlet(common.ViewletBase):
    def update(self):
        self.chatbot_url = os.environ.get("CHATBOT_URL", "")
        self.chatbot_id = os.environ.get("CHATBOT_ID", "")
        self.available = self.chatbot_url and self.chatbot_id
