# -*- coding: utf-8 -*-

from imio.smartweb.core.utils import get_ts_api_url
from imio.smartweb.core.utils import get_value_from_registry
from plone import api
from plone.restapi.services import Service

import os

# Role that pas.plugins.kimug gives to users authenticated with a SSO token.
KIMUG_AUTHENTICATED_ROLE = "Kimug Authenticated Users"
ALLOWED_ROLES = {"Manager", KIMUG_AUTHENTICATED_ROLE}


class EguichetApiSettingsGet(Service):
    """Give the e-guichet (Publik w.c.s.) API settings of this site.
    Authentic sources (ex: imio.events.core) use them to post cards.
    The response holds a password: only Managers and SSO technical users
    can read it."""

    def reply(self):
        roles = set(api.user.get_roles())
        if not roles & ALLOWED_ROLES:
            self.request.response.setStatus(401)
            return {"error": {"type": "Unauthorized", "message": "Access denied"}}
        return {
            "url_ts": get_value_from_registry("smartweb.url_ts"),
            "wcs_api_url": get_ts_api_url("wcs"),
            "username": os.environ.get("RESTAPI_USER_USERNAME", ""),
            "password": os.environ.get("RESTAPI_USER_PASSWORD", ""),
        }
