from collective.exportimport.import_content import ImportContent
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisiteSettings
from imio.smartweb.core.contents.pages.pages import IDefaultPages
from plone.dexterity.interfaces import IDexterityFTI
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import urlparse
from zExceptions import NotFound
from zope.component import getUtility
from zope.interface import alsoProvides
from plone import api

import logging

logger = logging.getLogger(__name__)
from Products.CMFCore.utils import getToolByName


class CustomImportContent(ImportContent):

    def cleanup_broken_brains(self, context, root_path, depth=3):
        catalog = getToolByName(context, "portal_catalog")
        brains = catalog(path={"query": root_path, "depth": depth})
        removed = 0
        for b in brains:
            try:
                b._unrestrictedGetObject()
            except (NotFound, KeyError, AttributeError):
                catalog.uncatalog_object(b.getPath())
                removed += 1
        return removed

    def create_container(self, item):
        """Create container for item.
        See remarks in get_parent_as_container for some corner cases.
        """
        folder = self.context
        parent_url = unquote(item["parent"]["@id"])
        parent_url_parsed = urlparse(parent_url)
        # Get the path part, split it, remove the always empty first element.
        parent_path = parent_url_parsed.path.split("/")[1:]
        if (
            len(parent_url_parsed.netloc.split(":")) > 1
            or parent_url_parsed.netloc == "nohost"
        ):
            # For example localhost:8080, or nohost when running tests.
            # First element will then be a Plone Site id.
            # Get rid of it.
            parent_path = parent_path[1:]

        # Handle folderish Documents provided by plone.volto
        fti = getUtility(IDexterityFTI, name="Document")
        # if "fr/la-boverie/album/section-gallery/logo-laboverie.jpg" in item["@id"]:
        #     import pdb;pdb.set_trace()
        parent_type = (
            "Document"
            if fti.klass.endswith("FolderishDocument")
            else item["parent"]["@type"]
        )
        # parent_type = (
        #    "Document" if fti.klass.endswith("FolderishDocument") else "Folder"
        # )
        # create original structure for imported content
        try:
            for element in parent_path:
                if element in folder:
                    folder = folder[element]
                    continue

                try:
                    new_folder = api.content.create(
                        container=folder,
                        type=parent_type,
                        id=element,
                        title=element,
                    )
                    folder = new_folder

                except NotFound:
                    # L'objet peut avoir été ajouté dans le BTree du folder
                    # mais l'exception vient souvent d'un event/reindex ensuite.
                    if element in folder:
                        root_path = "/".join(
                            folder.getPhysicalPath()
                        )  # le container courant
                        removed = self.cleanup_broken_brains(folder, root_path, depth=5)
                        logger.warning(
                            "Removed %s broken catalog entries under %s",
                            removed,
                            root_path,
                        )

                        folder = folder[element]
                        continue

                    # Si l'objet n'est même pas là, c'est un vrai échec
                    logger.error(
                        "NotFound during create and %s was NOT created in %s",
                        element,
                        folder.absolute_url(),
                    )
                    raise
        except:
            logger.error(
                f"ERREUR SUR :{element} -- {folder} -- {folder.absolute_url()}"
            )
        return folder

    def global_obj_hook(self, obj, item):
        """Inspect the content item before serialization data."""
        logger.info("imio.smartweb.core : global_obj_hook")
        # if (
        #     "vie-communale/projet-de-ville/liege-2030/projet-de-ville-liege-2030"
        #     in item["@id"]
        # ):
        #     # il faut regarder pourquoi l'image ne va faire que 1ko lors de l'importation
        #     import pdb;pdb.set_trace()
        if "cpskin.minisite.interfaces.IMinisiteRoot" in item.get(
            "_cpskin_interfaces", []
        ):
            alsoProvides(obj, IImioSmartwebMinisite)
            alsoProvides(obj, IImioSmartwebMinisiteSettings)
            setattr(obj, "logo", None)
            setattr(obj, "logo_display_mode", "title")
            logger.info(f"Set minisite to {obj.absolute_url()} ")

        if "imio.smartweb.core.contents.pages.pages.IDefaultPages" in item.get(
            "_smartweb_interfaces", []
        ):
            alsoProvides(obj, IDefaultPages)
            obj.aq_parent.set_default_item(new_default_item=obj)
            logger.info(
                f"Set INTERFACE 'cause I'm a default page : ({obj.absolute_url()}) "
            )
        # layout = item.get("layout")
        # if "fr/decouvrir/plein-air/art-public/la-fontaine-de-la-tradition-1" in item["@id"]:
        #     import pdb; pdb.set_trace()
        # if layout:
        #     try:
        #         obj.setLayout(layout)
        #         logger.info(f"  {layout} to {obj.absolute_url()} ")
        #         # print(f"setLayout {layout} TO {obj.absolute_url()}")
        #     except AttributeError:
        #         pass
        # if item.get("_cpskin_default_page", None):
        #     obj.setDefaultPage(item.get("_cpskin_default_page"))
        #     logger.info(f"Set default page to {obj.absolute_url()} ")
        obj.reindexObject()
        return obj

    # !!! by default, this method remove item layout
    def global_dict_hook(self, item):
        return item
