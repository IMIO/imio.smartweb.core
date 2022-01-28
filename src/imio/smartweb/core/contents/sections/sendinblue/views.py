# -*- coding: utf-8 -*-

from collective.sendinblue.browser.portlet import PortletSubscribeForm
from imio.smartweb.core.contents.sections.views import SectionView
from plone.z3cform.interfaces import IWrappedForm
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
        form.update()
        return form
