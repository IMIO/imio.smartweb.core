# -*- coding: utf-8 -*-

from imio.smartweb.common.adapters import BaseCroppingProvider
from plone.app.imagecropping.dx import CroppingUtilsDexterity
from plone.app.imagecropping.interfaces import IImageCroppingUtils
from plone.namedfile.interfaces import IImage
from plone.namedfile.interfaces import IImageScaleTraversable
from zope.component import adapter
from zope.interface import implementer


UNCROPPABLE_FIELDS = ["banner", "background_image"]


class SmartwebCroppingProvider(BaseCroppingProvider):
    def get_scales(self, fieldname, request=None):
        """Define default cropping scales for all common fields"""
        if fieldname in UNCROPPABLE_FIELDS:
            return []
        elif fieldname == "image":
            # scales used for lead_image fields
            return ["portrait_affiche", "paysage_affiche"]
        else:
            return super(SmartwebCroppingProvider, self).get_scales(fieldname, request)


@implementer(IImageCroppingUtils)
@adapter(IImageScaleTraversable)
class SmartwebCroppingUtilsDexterity(CroppingUtilsDexterity):
    def _image_field_values(self):
        """Remove banner field from cropping editor"""
        for fieldname, field in self._all_fields():
            value = getattr(self.context, fieldname, None)
            if (
                value
                and IImage.providedBy(value)
                and fieldname not in UNCROPPABLE_FIELDS
            ):
                yield (fieldname, value)
