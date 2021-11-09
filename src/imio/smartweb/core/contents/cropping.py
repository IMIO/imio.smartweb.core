# -*- coding: utf-8 -*-

from imio.smartweb.common.adapters import BaseCroppingProvider


class SmartwebCroppingProvider(BaseCroppingProvider):
    def get_scales(self, fieldname, request=None):
        """Define default cropping scales for all common fields"""
        if fieldname == "banner":
            # scale used for banner fields
            return ["banner"]
        elif fieldname == "background_image":
            # scales used for background_image fields
            return ["affiche"]
        elif fieldname == "image":
            # scales used for lead_image fields
            return ["liste", "vignette", "slide"]
        else:
            return super(SmartwebCroppingProvider, self).get_scales(fieldname, request)
