# -*- coding: utf-8 -*-

from collective.instancebehavior import disable_behaviors
from collective.instancebehavior import enable_behaviors
from collective.instancebehavior import instance_behaviors_of
from imio.smartweb.common.utils import get_vocabulary
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from plone.supermodel import model
from z3c.form import button
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema


class IInstanceBehaviors(model.Schema):

    directives.widget(instance_behaviors=CheckBoxFieldWidget)
    instance_behaviors = schema.List(
        title=_("Available taxonomies"),
        description=_(
            "Changes will only affect this content. They must be carried out with full knowledge. (No test)"
        ),
        value_type=schema.Choice(
            vocabulary="imio.smartweb.vocabulary.AvailableInstanceBehaviors"
        ),
    )


class InstanceBehaviors(AutoExtensibleForm, form.Form):

    schema = IInstanceBehaviors
    ignoreContext = True
    enable_autofocus = False
    label = _("Taxonomies choices form")
    description = _(
        "Be careful, adding or removing taxonomies must be a part of strategy implemented in collaboration with iMio"
    )

    def updateWidgets(self):
        super(InstanceBehaviors, self).updateWidgets()
        instance_behaviors_voc = get_vocabulary(
            "imio.smartweb.vocabulary.AvailableInstanceBehaviors"
        )
        instance_behaviors = [
            voc.value
            for voc in instance_behaviors_voc
            if voc.value in instance_behaviors_of(self.context)
        ]
        self.widgets["instance_behaviors"].value = instance_behaviors

    @button.buttonAndHandler("Ok")
    def handleApply(self, action):
        data, errors = self.extractData()
        selected_instance_behaviors = data.get("instance_behaviors")
        enable_behaviors(self.context, selected_instance_behaviors, [])
        instance_behaviors_voc = get_vocabulary(
            "imio.smartweb.vocabulary.AvailableInstanceBehaviors"
        )
        disable_instance_behaviors = [
            voc.value
            for voc in instance_behaviors_voc
            if voc.value not in selected_instance_behaviors
        ]
        disable_behaviors(self.context, disable_instance_behaviors, [])
        if hasattr(self.request, ASSIGNABLE_CACHE_KEY):
            delattr(self.request, ASSIGNABLE_CACHE_KEY)
        if errors:
            self.status = self.formErrorsMessage
            return
        api.portal.show_message(
            _("Taxonomies are correctly set on your object!"), self.request
        )
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler("Cancel")
    def handleCancel(self, action):
        self.request.response.redirect(self.context.absolute_url())
