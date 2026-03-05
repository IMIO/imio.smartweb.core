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
        brains = api.content.find(portal_type="imio.smartweb.Folder")
        cpt_default_pages = 0
        cpt = 0
        cpt_break_link_integrity = 0
        break_link_integrity_links = []
        not_default_pages = []
        for brain_folder in brains:
            children = api.content.find(
                path={"query": brain_folder.getPath(), "depth": 1}
            )
            if len(children) == 1 and children[0].portal_type == "imio.smartweb.Page":
                cpt = cpt + 1
                brain_page = children[0]
                obj = brain_folder.getObject()
                if obj.defaultView() == "element_view":
                    # 1 seule page et page par défaut, on est typiquement dans le cas d'une remontée de page !
                    print(brain_page.getPath())
                    alsoProvides(self.request, IDisableCSRFProtection)
                    page_obj = brain_page.getObject()
                    parent = obj.aq_parent
                    new_id = page_obj.id
                    if new_id.endswith("-1"):
                        new_id = new_id[:-2]
                    print(
                        f"Moving {brain_page.getPath()} -> {'/'.join(parent.getPhysicalPath())}/{new_id}"
                    )
                    if page_obj.id == obj.id:
                        # Temporarily rename the folder to avoid id collision during move
                        api.content.rename(obj=obj, new_id=obj.id + "-old")
                    api.content.move(source=page_obj, target=parent)
                    try:
                        api.content.delete(obj=obj)
                    except LinkIntegrityNotificationException:
                        cpt_break_link_integrity += 1
                        break_link_integrity_links.append(
                            "/".join(obj.getPhysicalPath())
                        )
                        print(
                            f"  Link integrity breach — orphan folder left: {'/'.join(obj.getPhysicalPath())}"
                        )
                        try:
                            api.content.transition(obj=obj, transition="retract")
                        except Exception:
                            pass  # already private or no valid transition
                        continue
                    # Re-fetch page_obj: after move+delete the old acquisition context is stale
                    page_obj = parent[page_obj.id]
                    if new_id != page_obj.id:
                        api.content.rename(obj=page_obj, new_id=new_id)
                    cpt_default_pages = cpt_default_pages + 1
                else:
                    not_default_pages.append("/".join(obj.getPhysicalPath()))

        print(f"Nombre de pages par défaut à remonter == {cpt_default_pages}")
        print(f"Nombre de dossiers ne contenant qu'une seule page == {cpt}")
        print(f"Nombre de liens cassés == {cpt_break_link_integrity}")
        display_links = "\r\n".join(break_link_integrity_links)
        print(f"Liens non traités car peuvent cassés l'intégrité : {display_links}")
        display_not_default_pages = "\r\n".join(not_default_pages)
        print(
            f"Liens non traités car pas la page par défaut : {display_not_default_pages}"
        )


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
