# -*- coding: utf-8 -*-

from collective.sendinblue.browser.portlet import PortletSubscribeForm
from imio.smartweb.core.contents.sections.views import SectionView
from plone import api
from plone.z3cform.interfaces import IWrappedForm
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class SendinblueData(object):
    newsletter_list = None
    use_captcha = False


class SendinblueView(SectionView):
    """ """

    def get_subscription_form(self):
        data = SendinblueData()
        data.newsletter_list = self.context.newsletter_list
        form = PortletSubscribeForm(self.context, self.request, data)
        alsoProvides(form, IWrappedForm)
        form.enable_autofocus = False
        button_text = self.button_text
        if button_text is not None:
            button_text_fr = (
                row.get("text")
                for row in button_text
                if row.get("language") == self.language
            )
            for text in button_text_fr:
                form.buttons._data_values[0].title = text
        form.update()
        return form

    @property
    def button_position(self):
        return (
            api.portal.get_registry_record("smartweb.sendinblue_button_position")
            or "button_bottom"
        )

    @property
    def button_text(self):
        return (
            None
            if api.portal.get_registry_record("smartweb.sendinblue_button_text") == []
            else api.portal.get_registry_record("smartweb.sendinblue_button_text")
        )

    @property
    def language(self):
        context = self.context.aq_inner
        portal_state = getMultiAdapter(
            (context, self.request), name="plone_portal_state"
        )
        current_language = portal_state.language()
        return current_language
