import React from 'react';
import ReactWebComponent from 'react-web-component';
import ExampleWebComponent from './components/ExampleWebComponent/ExampleWebComponent.jsx'

ReactWebComponent.create(<ExampleWebComponent />, 'smartweb-example-component');


if (module.hot) {  // Accept hot module replacement (HMR) while live-reloading
  module.hot.accept();
}
