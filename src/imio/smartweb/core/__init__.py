# -*- coding: utf-8 -*-
"""Init and utils."""

# collective.themefragments
from AccessControl import allow_module, allow_class, allow_type
from requests.models import Response

allow_module("requests")
allow_class(Response)
allow_type(type("requests.models.Response"))
