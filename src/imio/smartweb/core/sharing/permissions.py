# -*- coding: utf-8 -*-
from AccessControl import ModuleSecurityInfo
from AccessControl.Permission import addPermission

security = ModuleSecurityInfo("imio.smartweb.core.sharing.permissions")

# Control the individual roles
security.declarePublic("DelegateLocalManagerRole")
DelegateLocalManagerRole = "Sharing page: Delegate Local Manager role"
addPermission(
    DelegateLocalManagerRole,
    ("Manager", "Site Administrator"),
)
