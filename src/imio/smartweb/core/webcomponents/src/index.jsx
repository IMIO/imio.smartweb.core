import React from "react";
import ReactWebComponent from "react-web-component";
import Annuaire from "./components/Annuaire";
import Campaign from "./components/Campaign";
import News from "./components/News";
import Events from "./components/Events";
import Search from "./components/Search";
import "./index.scss";

/*
  Register exposed web components here
  Note: if your webcomponent depends on external css, disable shadow root
*/
ReactWebComponent.create(<Annuaire />, "smartweb-annuaire", false);
ReactWebComponent.create(<Campaign />, "smartweb-campaign", false);
ReactWebComponent.create(<News />, "smartweb-news", false);
ReactWebComponent.create(<Events />, "smartweb-events", false);
ReactWebComponent.create(<Search />, "smartweb-search", false);

if (module.hot) {
    // Accept hot module replacement (HMR) while live-reloading
    module.hot.accept();
}
