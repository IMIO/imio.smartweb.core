import React from 'react';
import ReactWebComponent from 'react-web-component';
import AnnuaireComponent from './components/AnnuaireComponent/AnnuaireComponent.js'

ReactWebComponent.create(<AnnuaireComponent />, 'smartweb-annuaire-component');


if (module.hot) {  // Accept hot module replacement (HMR) while live-reloading
  module.hot.accept();
}
