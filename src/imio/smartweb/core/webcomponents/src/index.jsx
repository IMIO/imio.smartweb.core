import React from "react";
import ReactWebComponent from "react-web-component";
import Annuaire from "./components/Annuaire";

/*
  Register exposed web components here
  Note: if your webcomponent depends on external css, disable shadow root
*/
ReactWebComponent.create(<Annuaire />, "smartweb-annuaire", false);

if (module.hot) {
    // Accept hot module replacement (HMR) while live-reloading
    module.hot.accept();
}
