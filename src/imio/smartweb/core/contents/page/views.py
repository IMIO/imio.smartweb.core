# -*- coding: utf-8 -*-

from plone.dexterity.browser.view import DefaultView


class PageView(DefaultView):
    """Page view"""

    def available_section(self, section):
        """
        Check if specified section must be shown
        """
        return section in self.context.visible_sections
