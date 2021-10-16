import React from "react";
import ReactWebComponent from "react-web-component";
import AnnuaireComponent from "./components/AnnuaireComponent/AnnuaireComponent.jsx";

/*
  Register exposed web components here
  Note: if your webcomponent depends on external css, disable shadow root
*/
ReactWebComponent.create(<AnnuaireComponent />, "smartweb-annuaire-component", false);

if (module.hot) {
    // Accept hot module replacement (HMR) while live-reloading
    module.hot.accept();
}
