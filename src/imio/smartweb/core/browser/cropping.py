# -*- coding: utf-8 -*-

from imio.smartweb.core.interfaces import ICropping
from operator import itemgetter
from plone.app.imagecropping.browser.editor import CroppingEditor
from plone.namedfile.interfaces import IAvailableSizes
from zope.component import getUtility

import six


class SmartwebCroppingEditor(CroppingEditor):
    def _scales(self, fieldname):
        adapter = ICropping(self.context, alternate=None)
        if adapter is None:
            yield from super(SmartwebCroppingEditor, self)._scales(fieldname)
            return
        allowed_sizes = getUtility(IAvailableSizes)() or []
        sizes_iterator = sorted(six.iteritems(allowed_sizes), key=itemgetter(1))
        context_scales = adapter.get_scales(fieldname, self.request)
        for scale_id, target_size in sizes_iterator:
            if scale_id not in context_scales:
                continue
            yield scale_id, target_size
