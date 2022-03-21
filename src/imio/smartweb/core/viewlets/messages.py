# -*- coding: utf-8 -*-

from collective.messagesviewlet.utils import get_messages_to_show
from collective.messagesviewlet.browser.messagesviewlet import GlobalMessagesViewlet
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from plone import api


class MessagesViewlet(GlobalMessagesViewlet):
    def getAllMessages(self):
        context = self.context
        root = api.portal.get_navigation_root(context)
        if not IImioSmartwebMinisite.providedBy(root):
            return super(MessagesViewlet, self).getAllMessages()
        messages = get_messages_to_show(self.context)
        messages = [m for m in messages if m.location in self.location_filter]
        root_absolute_url = root.absolute_url()
        messages = [
            m for m in messages if m.absolute_url().startswith(root_absolute_url)
        ]
        return messages
