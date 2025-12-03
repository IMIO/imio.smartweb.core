from collective.exportimport.import_content import ImportContent
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisite
from imio.smartweb.core.behaviors.minisite import IImioSmartwebMinisiteSettings
from imio.smartweb.core.contents.pages.pages import IDefaultPages
from plone.dexterity.interfaces import IDexterityFTI
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import urlparse
from zope.component import getUtility
from zope.interface import alsoProvides
from plone import api

import logging

logger = logging.getLogger(__name__)


class CustomImportContent(ImportContent):

    def create_container(self, item):
        """Create container for item.

        See remarks in get_parent_as_container for some corner cases.
        """
        # if (
        #     item["@id"]
        #     == "http://localhost:8080/Plone/fr/je-suis/commercant/section-gallery/banner.jpg"
        # ):
        #     import pdb

        #     pdb.set_trace()
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
        # BOULCH
        # if "fr/la-boverie/album/section-gallery/logo-laboverie.jpg" in item["@id"]:
        #     import pdb

        #     pdb.set_trace()
        parent_type = (
            "Document"
            if fti.klass.endswith("FolderishDocument")
            else item["parent"]["@type"]
        )
        # parent_type = (
        #    "Document" if fti.klass.endswith("FolderishDocument") else "Folder"
        # )
        # create original structure for imported content
        for element in parent_path:
            try:
                if element not in folder:
                    folder = api.content.create(
                        container=folder,
                        type=parent_type,
                        id=element,
                        title=element,
                    )
                    logger.info(
                        "Created container %s to hold %s",
                        folder.absolute_url(),
                        item["@id"],
                    )
                else:
                    folder = folder[element]
            except:
                print(f"ERREUR SUR :{element} -- {folder} -- {folder.absolute_url()}")

        return folder

    def global_obj_hook(self, obj, item):
        """Inspect the content item before serialization data."""
        logger.info("imio.smartweb.core : global_obj_hook")
        if "cpskin.minisite.interfaces.IMinisiteRoot" in item.get(
            "_cpskin_interfaces", []
        ):
            alsoProvides(obj, IImioSmartwebMinisite)
            alsoProvides(obj, IImioSmartwebMinisiteSettings)
            logger.info(f"Set minisite to {obj.absolute_url()} ")

        if "imio.smartweb.core.contents.pages.pages.IDefaultPages" in item.get(
            "_smartweb_interfaces", []
        ):
            alsoProvides(obj, IDefaultPages)
            logger.info(f"Set default page to {obj.absolute_url()} ")
        layout = item.get("layout")
        if layout:
            try:
                obj.setLayout(layout)
                logger.info(f"Set layout : {layout} to {obj.absolute_url()} ")
                # print(f"setLayout {layout} TO {obj.absolute_url()}")
            except AttributeError:
                pass
        obj.reindexObject()
        return obj

    # !!! by default, this method remove item layout
    def global_dict_hook(self, item):
        return item
