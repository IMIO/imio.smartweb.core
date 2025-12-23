import logging
import os

log = logging.getLogger(__name__)

if os.environ.get("PROJECT_ID", "") == "liege_smartweb":
    from plone.namedfile.file import NamedBlobImage
    from plone.namedfile.file import MAX_INFO_BYTES
    from plone.namedfile.file import NamedBlobFile  # Import du parent
    from plone.namedfile.utils import getImageInfo

    def patched_setData(self, data):
        # 1. On appelle le parent direct (NamedBlobFile) pour stocker les données
        NamedBlobFile._setData(self, data)
        # 2. On récupère les premiers bytes pour l'analyse
        firstbytes = self.getFirstBytes()

        # 3. Analyse initiale
        res = getImageInfo(data)

        if (
            res == ("image/jpeg", -1, -1)
            or res == ("image/tiff", -1, -1)
            or res == ("image/svg+xml", -1, -1)
        ):
            # header was longer than firstbytes
            start = len(firstbytes)
            length = max(0, MAX_INFO_BYTES - start)
            firstbytes += self.getFirstBytes(start, length)
            res = getImageInfo(firstbytes)

        contentType, self._width, self._height = res
        if contentType:
            self.contentType = contentType

        log.info("Patch NamedBlobImage._setData exécuté pour %s", self.filename)

    # Application du patch
    NamedBlobImage._setData = patched_setData
else:
    log.info("Monkeypatch NamedBlobImage._setData NOT activated")
