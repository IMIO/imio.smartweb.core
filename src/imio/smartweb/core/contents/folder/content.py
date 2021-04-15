# -*- coding: utf-8 -*-

from collective.instancebehavior.interfaces import IInstanceBehaviorAssignableContent
from imio.smartweb.core.contents import IDefaultPages
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.interface import noLongerProvides


class IFolder(model.Schema):
    """Marker interface and Dexterity Python Schema for Folder"""

    directives.widget(default_page_uid=RadioFieldWidget)
    directives.mode(default_page_uid="hidden")
    default_page_uid = schema.Choice(
        title=_(u"Set Default page"),
        description=_(u"Choose an item as your default folder view"),
        required=False,
        vocabulary="imio.smartweb.vocabulary.CurrentFolderPages",
    )


@implementer(IFolder, IInstanceBehaviorAssignableContent)
class Folder(Container):
    """Folder class"""

    def canSetDefaultPage(self):
        return False

    def setLayout(self, layout):
        """Disable current default page when layout is changed on a folder"""
        super(Folder, self).setLayout(layout)
        current_default_page = self.get_default_item(object=True)
        if current_default_page is not None:
            noLongerProvides(current_default_page, IDefaultPages)
            current_default_page.exclude_from_nav = False
            current_default_page.reindexObject(
                idxs=("object_provides", "exclude_from_nav")
            )
            self.default_page_uid = None

    def get_default_item(self, object=False):
        if self.default_page_uid:
            brains = api.content.find(context=self, UID=self.default_page_uid)
            if brains:
                brain = brains[0]
                return object is True and brain.getObject() or brain
