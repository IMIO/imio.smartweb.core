# -*- coding: utf-8 -*-

from collective.sendinblue.browser.portlet import PortletSubscribeForm
from imio.smartweb.core.contents.sections.views import SectionView
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.z3cform.interfaces import IWrappedForm
from z3c.form import button
from zope.component import provideAdapter
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

        # Change 'subscribe' action title
        actions = button.ButtonActions(form, self.request, None)
        ApplyLabel = button.StaticButtonActionAttribute(
            self.button_text, button=form.buttons["subscribe"]
        )
        provideAdapter(ApplyLabel, name="title")
        actions.update()

        form.enable_autofocus = False
        form.update()
        return form

    @property
    def button_position(self):
        return api.portal.get_registry_record(
            "smartweb.sendinblue_button_position", default="button_bottom"
        )

    @property
    def button_text(self):
        current_lang = api.portal.get_current_language()[:2]
        button_texts = api.portal.get_registry_record(
            "smartweb.sendinblue_button_text", default=[]
        )
        for row in button_texts:
            if row.get("language") == current_lang:
                return row.get("text")
        return _("Subscribe")
