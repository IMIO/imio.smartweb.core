import React from "react";
import ReactWebComponent from "react-web-component";
import Annuaire from "./components/Annuaire";
import Campaign from "./components/Campaign";
import News from "./components/News";
import Events from "./components/Events";
import Search from "./components/Search";
import "./index.scss";
import "moment/locale/fr";
import "moment/locale/nl";
import "moment/locale/de";
/*
  Register exposed web components here
  Note: if your webcomponent depends on external css, disable shadow root
*/
ReactWebComponent.create(<Annuaire />, "smartweb-annuaire", false);
ReactWebComponent.create(<Campaign />, "smartweb-campaign", false);
ReactWebComponent.create(<News />, "smartweb-news", false);
ReactWebComponent.create(<Events />, "smartweb-events", false);
ReactWebComponent.create(<Search />, "smartweb-search", false);

if (import.meta.hot) {
    // Accept hot module replacement (HMR) while live-reloading
    import.meta.hot.accept();
}

// After a new production deploy, `emptyOutDir` wipes every previous build's
// content-hashed chunk/CSS files. A browser or intermediate cache (Varnish,
// CDN) that's still serving the previous build's entry script will keep
// trying to dynamically import()/preload those now-deleted files, which
// Vite's own runtime helper surfaces as this event. Reloading re-fetches the
// page (and this script tag) from scratch, picking up the current build.
// Guard against a reload loop if the failure isn't actually cache-related
// (e.g. a real outage) by only doing this once per tab.
window.addEventListener("vite:preloadError", () => {
    if (!window.sessionStorage.getItem("smartweb-preload-reloaded")) {
        window.sessionStorage.setItem("smartweb-preload-reloaded", "1");
        window.location.reload();
    }
});
