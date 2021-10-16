export const getPath = () => {
    return document.location.pathname;
};

export function getPortalUrl() {
    return window.PORTAL_URL;
}

export function getBundleUrl() {
    return getPortalUrl() + "/++plone++imio.smartweb.webcomponents";
}
