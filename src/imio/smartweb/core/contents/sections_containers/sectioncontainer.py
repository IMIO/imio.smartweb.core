# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from zope.interface import Interface
from zope.interface import implementer


class ISectionContainer(Interface):
    """ Shared mecanism for sectioncontainers """


@implementer(ISectionContainer)
class SectionContainer(Container):
    """ Shared mecanism for sectioncontainers """
