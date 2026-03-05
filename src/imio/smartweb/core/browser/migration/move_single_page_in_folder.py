# -*- coding: utf-8 -*-

from imio.smartweb.core.behaviors.subsite import IImioSmartwebSubsite
from imio.smartweb.core.contents import IFolder
from imio.smartweb.locales import SmartwebMessageFactory as _
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces.constrains import DISABLED
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.Five.browser import BrowserView
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


# /Plone/fr/vie-communale/services-communaux/urbanisme/publications/prix-architecture-et-urbanisme/prix-de-larchitecture-et-de-lurbanisme-1/laureats-des-prix-de-larchitecture-et-de-lurbanisme-2015/laureats-du-prix-de-lurbanisme-2015
# ici, on a une page par défaut, sur un dossier presque du même nom
# Bonne nouvelle, la page et le folder on la même leadimage
# et donc, le dossier "prix-de-larchitecture-et-de-lurbanisme-1"
# affichage blocs avec images va rester ok.


class MoveSinglePageView(BrowserView):

    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        brains = api.content.find(portal_type="imio.smartweb.Folder")
        self.cpt_default_pages = 0
        self.cpt_single_page_folders = 0
        self.break_link_integrity_links = []
        self.not_default_pages = []
        self.moved_pages = []

        for brain_folder in brains:
            children = api.content.find(
                path={"query": brain_folder.getPath(), "depth": 1}
            )
            if len(children) == 1 and children[0].portal_type == "imio.smartweb.Page":
                self.cpt_single_page_folders += 1
                brain_page = children[0]
                obj = brain_folder.getObject()
                if obj.defaultView() == "element_view":
                    # 1 seule page et page par défaut, on est typiquement dans le cas d'une remontée de page !
                    original_page_path = brain_page.getPath()
                    page_obj = brain_page.getObject()
                    parent = obj.aq_parent
                    new_id = page_obj.id
                    if new_id.endswith("-1"):
                        new_id = new_id[:-2]
                    if page_obj.id == obj.id:
                        # Temporarily rename the folder to avoid id collision during move
                        api.content.rename(obj=obj, new_id=obj.id + "-old")
                    api.content.move(source=page_obj, target=parent)
                    try:
                        api.content.delete(obj=obj)
                    except LinkIntegrityNotificationException:
                        self.break_link_integrity_links.append(
                            "/".join(obj.getPhysicalPath())
                        )
                        try:
                            api.content.transition(obj=obj, transition="retract")
                        except Exception:
                            pass  # already private or no valid transition
                        continue
                    # Re-fetch page_obj: after move+delete the old acquisition context is stale
                    page_obj = parent[page_obj.id]
                    if new_id != page_obj.id and new_id not in parent:
                        api.content.rename(obj=page_obj, new_id=new_id)
                    else:
                        new_id = page_obj.id
                    destination = f"{'/'.join(parent.getPhysicalPath())}/{new_id}"
                    self.moved_pages.append(
                        {"from": original_page_path, "to": destination}
                    )
                    self.cpt_default_pages += 1
                else:
                    self.not_default_pages.append("/".join(obj.getPhysicalPath()))

        return self.index()


# if brain_folder.id == "images" and brain_page.id == "medias":
#     # à remonter d'un niveau
#     # exemple : /Plone/fr/cpas-minisite/les-services/enfance/images/medias
#     # print(brain_page.getPath())
#     continue
# elif brain_folder.id != "images" and brain_page.id == "medias":
#     # à laisser en place ?
#     continue
# elif brain_page.id == "images":
#     # à laisser en place
#     # exemple : /Plone/fr/vie-communale/services-communaux/gestion-documentaire-et-archives/actualites/images
#     continue
# else:
#     # /Plone/fr/vie-communale/services-communaux/enfance/accueils-durgence/accueils-urgence
#     # /Plone/fr/vivre-a-liege/mobilite/en-train" in brain_folder.getPath():
