"use strict";(self.webpackChunkimio_smartweb_core_webcomponents=self.webpackChunkimio_smartweb_core_webcomponents||[]).push([[301],{88301:function(e,t,r){r.r(t),r.d(t,{default:function(){return z}});var n=r(78709),a=r(12707),l=r(51031);var o=r(71775),c=r(14844);function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function u(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}function s(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function m(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?s(Object(r),!0).forEach((function(t){f(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):s(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function f(e,t,r){return(t=p(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function p(e){var t=function(e,t){if("object"!==i(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==i(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===i(t)?t:String(t)}function b(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,o,c=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(c.push(n.value),c.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(o=r.return(),Object(o)!==o))return}finally{if(u)throw a}}return c}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return y(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var d=function(e){var t=(0,l.k6)(),a=r(31296),i=b((0,n.useState)(e.activeFilter),2),s=i[0],y=i[1],d=b((0,n.useState)(null),2),v=d[0],g=d[1],h=b((0,n.useState)(null),2),E=h[0],w=h[1],O=(0,c.Z)({method:"get",url:"",baseURL:e.url,headers:{Accept:"application/json"},params:s}),S=O.response;O.error,O.isLoading,(0,n.useEffect)((function(){if(null!==S){var e=S.topics.map((function(e){return{value:e.token,label:e.title}})),t=S.category?S.category.map((function(e){return{value:e.token,label:e.title}})):"";g(e),w(t)}}),[S]);var j=(0,n.useCallback)((function(e){var t=e.target,r=t.name,n=t.value;n.length>2?y((function(e){return m(m({},e),{},f({},r,n))}),[]):y((function(e){var t=m({},e);t[r];return u(t,[r].map(p))}))})),N=(0,n.useCallback)((function(e,t){var r=t.name;e?y((function(t){return m(m({},t),{},f({},r,e.value))}),[]):y((function(e){var t=m({},e);t[r];return u(t,[r].map(p))}))})),A=(0,n.useRef)(!0);(0,n.useEffect)((function(){A.current?A.current=!1:(t.push({pathname:"./",search:a.stringify(s)}),e.onChange(s))}),[s]);var P=v&&v.filter((function(t){return t.value===e.activeFilter.topics})),k=E&&E.filter((function(t){return t.value===e.activeFilter.category})),x={control:function(e){return m(m({},e),{},{backgroundColor:"white",borderRadius:"0",height:"50px"})},placeholder:function(e){return m(m({},e),{},{color:"000",fontWeight:"bold",fontSize:"12px",textTransform:"uppercase",letterSpacing:"1.2px"})},option:function(e,t){t.data,t.isDisabled,t.isFocused,t.isSelected;return m({},e)}};return n.createElement(n.Fragment,null,n.createElement("form",{className:"r-filter",onSubmit:function(t){t.preventDefault(),e.onChange(s)}},n.createElement("div",{className:"r-filter-search"},n.createElement("input",{className:"input-custom-class",name:"SearchableText",type:"text",value:s.SearchableText,onChange:j,placeholder:"Recherche"}),n.createElement("button",{type:"submit"}))),n.createElement("div",{className:"r-filter topics-Filter"},n.createElement(o.ZP,{styles:x,name:"topics",className:"select-custom-class library-topics",isClearable:!0,onChange:N,options:v&&v,placeholder:"Thématiques",value:P&&P[0]})),n.createElement("div",{className:"r-filter  facilities-Filter"},n.createElement(o.ZP,{styles:x,name:"category",className:"select-custom-class library-facilities",isClearable:!0,onChange:N,options:E&&E,placeholder:"Catégories",value:k&&k[0]})))},v=r(6489),g=r(78279),h=r.n(g),E=(r(8047),r(5620));r(17110);function w(e){return w="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},w(e)}function O(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,o,c=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(c.push(n.value),c.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(o=r.return(),Object(o)!==o))return}finally{if(u)throw a}}return c}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return S(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return S(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function S(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function j(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function N(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?j(Object(r),!0).forEach((function(t){A(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):j(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function A(e,t,r){return(t=function(e){var t=function(e,t){if("object"!==w(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==w(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===w(t)?t:String(t)}(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var P=function(e){var t=e.queryUrl,a=e.onChange,o=(0,l.k6)(),i=r(31296).parse((0,v.Z)().toString()),u=N(N({},i),{},{UID:i.u,fullobjects:1}),s=O((0,n.useState)(u),2),m=s[0],f=(s[1],O((0,n.useState)({}),2)),p=f[0],b=f[1],y=O((0,n.useState)(0),2),d=y[0],g=y[1],w=O((0,n.useState)(0),2),S=w[0],j=w[1],A=(0,c.Z)({method:"get",url:"",baseURL:t,headers:{Accept:"application/json"},params:m},[]),P=A.response;A.error,A.isLoading;(0,n.useEffect)((function(){null!==P&&b(P.items[0]),window.scrollTo(0,0)}),[P]),(0,n.useEffect)((function(){p.items&&p.items.length>0&&(g(p.items.filter((function(e){return"File"===e["@type"]}))),j(p.items.filter((function(e){return"Image"===e["@type"]}))))}),[p]),h().locale("fr");var k=h()(p.created).startOf("minute").fromNow(),x=h()(p.modified).startOf("minute").fromNow();return n.createElement("div",{className:"new-content r-content"},n.createElement("button",{type:"button",onClick:function(){o.push("./"),a(null)}},"Retour"),n.createElement("article",null,n.createElement("header",null,n.createElement("h2",{className:"r-content-title"},p.title),n.createElement("div",{className:"r-content-description"},n.createElement(E.D,null,p.description))),n.createElement("figure",null,n.createElement("div",{className:"r-content-img",style:{backgroundImage:p.image?"url("+p.image.scales.affiche.download+")":""}})),n.createElement("div",{className:"r-content-news-info"},n.createElement("div",{className:"r-content-news-info-container"},n.createElement("div",{className:"r-content-news-info-schedul"},n.createElement("div",{className:"icon-baseline"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",preserveAspectRatio:"xMinYMin",viewBox:"0 0 19.41 19.41"},n.createElement("path",{d:"M16.09,2.74H14.35V.85a.44.44,0,0,0-.43-.44H12.47A.44.44,0,0,0,12,.85V2.74H7.38V.85A.44.44,0,0,0,7,.41H5.5a.44.44,0,0,0-.44.44V2.74H3.32A1.74,1.74,0,0,0,1.58,4.48V17.26A1.74,1.74,0,0,0,3.32,19H16.09a1.74,1.74,0,0,0,1.75-1.74V4.48A1.74,1.74,0,0,0,16.09,2.74Zm-.21,14.52H3.54A.22.22,0,0,1,3.32,17h0V6.22H16.09V17a.21.21,0,0,1-.21.22Z"}))),n.createElement("div",{className:"dpinlb"},n.createElement("div",{className:"r-content-news-info--date"},n.createElement("div",{className:"r-content-date"},k===x?n.createElement("div",{className:"r-content-date-publish"},n.createElement("span",null,"Publié "),n.createElement("span",null,k)):n.createElement("div",null,n.createElement("div",{className:"r-content-date-publish"},n.createElement("span",null,"Publié "),n.createElement("span",null,k)),n.createElement("div",{className:"r-card-date-last"},n.createElement("span",null,"Actualisé "),n.createElement("span",null,x))))))),null===p.site_url&&null===p.video_url?"":n.createElement("div",{className:"r-content-news-info-link"},n.createElement("div",{className:"icon-baseline"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},n.createElement("path",{d:"M16.36,2.22H3.06a1.3,1.3,0,0,0-1.3,1.3h0v9a1.3,1.3,0,0,0,1.3,1.3H7.52v1.74h-.7a.8.8,0,0,0,0,1.6h5.79a.8.8,0,0,0,0-1.6h-.7V13.85h4.45a1.31,1.31,0,0,0,1.3-1.3v-9A1.3,1.3,0,0,0,16.36,2.22Zm-1.9,10.83a.37.37,0,1,1,.36-.37h0a.36.36,0,0,1-.36.36Zm1.6.08a.45.45,0,1,1,.44-.45h0a.44.44,0,0,1-.44.45h0Zm.53-1.35H2.82V3.52a.23.23,0,0,1,.23-.23H16.36a.23.23,0,0,1,.23.23h0v8.27Z"}))),n.createElement("div",{className:"dpinlb"},null===p.site_url?"":n.createElement("div",{className:"r-content-news-info-event_link"},n.createElement("a",{href:p.site_url},p.site_url)),null===p.video_url?"":n.createElement("div",{className:"r-content-news-info--video"},n.createElement("a",{href:p.video_url},"Lien vers la vidéo")))),null===p.facebook&&null===p.instagram&&null===p.twitter?"":n.createElement("div",{className:"r-content-news-info-social"},n.createElement("ul",null,p.facebook?n.createElement("li",null,n.createElement("a",{href:p.facebook,target:"_blank"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-204.79995 -341.33325 1774.9329 2047.9995"},n.createElement("path",{d:"M1365.333 682.667C1365.333 305.64 1059.693 0 682.667 0 305.64 0 0 305.64 0 682.667c0 340.738 249.641 623.16 576 674.373V880H402.667V682.667H576v-150.4c0-171.094 101.917-265.6 257.853-265.6 74.69 0 152.814 13.333 152.814 13.333v168h-86.083c-84.804 0-111.25 52.623-111.25 106.61v128.057h189.333L948.4 880H789.333v477.04c326.359-51.213 576-333.635 576-674.373",fill:"#100f0d"}),n.createElement("path",{d:"M948.4 880l30.267-197.333H789.333V554.609C789.333 500.623 815.78 448 900.584 448h86.083V280s-78.124-13.333-152.814-13.333c-155.936 0-257.853 94.506-257.853 265.6v150.4H402.667V880H576v477.04a687.805 687.805 0 00106.667 8.293c36.288 0 71.91-2.84 106.666-8.293V880H948.4",fill:"#fff"})))):"",p.instagram?n.createElement("li",null,n.createElement("a",{href:p.instagram,target:"_blank"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-100.7682 -167.947 873.3244 1007.682"},n.createElement("g",{fill:"#100f0d"},n.createElement("path",{d:"M335.895 0c-91.224 0-102.663.387-138.49 2.021-35.752 1.631-60.169 7.31-81.535 15.612-22.088 8.584-40.82 20.07-59.493 38.743-18.674 18.673-30.16 37.407-38.743 59.495C9.33 137.236 3.653 161.653 2.02 197.405.386 233.232 0 244.671 0 335.895c0 91.222.386 102.661 2.02 138.488 1.633 35.752 7.31 60.169 15.614 81.534 8.584 22.088 20.07 40.82 38.743 59.495 18.674 18.673 37.405 30.159 59.493 38.743 21.366 8.302 45.783 13.98 81.535 15.612 35.827 1.634 47.266 2.021 138.49 2.021 91.222 0 102.661-.387 138.488-2.021 35.752-1.631 60.169-7.31 81.534-15.612 22.088-8.584 40.82-20.07 59.495-38.743 18.673-18.675 30.159-37.407 38.743-59.495 8.302-21.365 13.981-45.782 15.612-81.534 1.634-35.827 2.021-47.266 2.021-138.488 0-91.224-.387-102.663-2.021-138.49-1.631-35.752-7.31-60.169-15.612-81.534-8.584-22.088-20.07-40.822-38.743-59.495-18.675-18.673-37.407-30.159-59.495-38.743-21.365-8.302-45.782-13.981-81.534-15.612C438.556.387 427.117 0 335.895 0zm0 60.521c89.686 0 100.31.343 135.729 1.959 32.75 1.493 50.535 6.965 62.37 11.565 15.68 6.094 26.869 13.372 38.622 25.126 11.755 11.754 19.033 22.944 25.127 38.622 4.6 11.836 10.072 29.622 11.565 62.371 1.616 35.419 1.959 46.043 1.959 135.73 0 89.687-.343 100.311-1.959 135.73-1.493 32.75-6.965 50.535-11.565 62.37-6.094 15.68-13.372 26.869-25.127 38.622-11.753 11.755-22.943 19.033-38.621 25.127-11.836 4.6-29.622 10.072-62.371 11.565-35.413 1.616-46.036 1.959-135.73 1.959-89.694 0-100.315-.343-135.73-1.96-32.75-1.492-50.535-6.964-62.37-11.564-15.68-6.094-26.869-13.372-38.622-25.127-11.754-11.753-19.033-22.943-25.127-38.621-4.6-11.836-10.071-29.622-11.565-62.371-1.616-35.419-1.959-46.043-1.959-135.73 0-89.687.343-100.311 1.959-135.73 1.494-32.75 6.965-50.535 11.565-62.37 6.094-15.68 13.373-26.869 25.126-38.622 11.754-11.755 22.944-19.033 38.622-25.127 11.836-4.6 29.622-10.072 62.371-11.565 35.419-1.616 46.043-1.959 135.73-1.959"}),n.createElement("path",{d:"M335.895 447.859c-61.838 0-111.966-50.128-111.966-111.964 0-61.838 50.128-111.966 111.966-111.966 61.836 0 111.964 50.128 111.964 111.966 0 61.836-50.128 111.964-111.964 111.964zm0-284.451c-95.263 0-172.487 77.224-172.487 172.487 0 95.261 77.224 172.485 172.487 172.485 95.261 0 172.485-77.224 172.485-172.485 0-95.263-77.224-172.487-172.485-172.487m219.608-6.815c0 22.262-18.047 40.307-40.308 40.307-22.26 0-40.307-18.045-40.307-40.307 0-22.261 18.047-40.308 40.307-40.308 22.261 0 40.308 18.047 40.308 40.308"}))))):"",p.twitter?n.createElement("li",null,n.createElement("a",{href:p.twitter,target:"_blank"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-44.7006 -60.54775 387.4052 363.2865"},n.createElement("path",{fill:"#000",d:"M93.719 242.19c112.46 0 173.96-93.168 173.96-173.96 0-2.646-.054-5.28-.173-7.903a124.338 124.338 0 0030.498-31.66c-10.955 4.87-22.744 8.148-35.11 9.626 12.622-7.57 22.313-19.543 26.885-33.817a122.62 122.62 0 01-38.824 14.841C239.798 7.433 223.915 0 206.326 0c-33.764 0-61.144 27.381-61.144 61.132 0 4.798.537 9.465 1.586 13.941-50.815-2.557-95.874-26.886-126.03-63.88a60.977 60.977 0 00-8.279 30.73c0 21.212 10.794 39.938 27.208 50.893a60.685 60.685 0 01-27.69-7.647c-.009.257-.009.507-.009.781 0 29.61 21.075 54.332 49.051 59.934a61.218 61.218 0 01-16.122 2.152 60.84 60.84 0 01-11.491-1.103c7.784 24.293 30.355 41.971 57.115 42.465-20.926 16.402-47.287 26.171-75.937 26.171-4.929 0-9.798-.28-14.584-.846 27.059 17.344 59.189 27.464 93.722 27.464"})))):"")))),n.createElement("div",{className:"r-content-text",dangerouslySetInnerHTML:{__html:p.text&&p.text.data}}),d?n.createElement("div",{className:"r-content-files"},n.createElement("h2",{className:"r-content-files-title"},"Téléchargements"),d.map((function(e){return n.createElement("div",{className:"r-content-file"},n.createElement("a",{href:e.targetUrl,className:"r-content-file-link",rel:"nofollow"},n.createElement("span",{className:"r-content-file-title"},e.title),n.createElement("span",{className:"r-content-file-icon"},n.createElement("svg",{width:"21",height:"21",viewBox:"0 0 24 24",fill:"none",stroke:"#8899a4","stroke-width":"2","stroke-linecap":"square","stroke-linejoin":"arcs"},n.createElement("path",{d:"M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"}))," ")))}))):"",S?n.createElement("div",{className:"r-content-gallery"},n.createElement("div",{class:"spotlight-group flexbin r-content-gallery"},S.map((function(e){return n.createElement("a",{class:"spotlight",href:e.image.scales.extralarge.download,"data-description":"Lorem ipsum dolor sit amet, consetetur sadipscing."},n.createElement("img",{src:e.image.scales.preview.download,alt:"Lorem ipsum dolor sit amet"}))})))):""))},k=(r(54570),r(29924)),x=r.n(k);function C(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,o,c=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(c.push(n.value),c.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(o=r.return(),Object(o)!==o))return}finally{if(u)throw a}}return c}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return U(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return U(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function U(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var I=function(e){var t=e.contactItem,r=C((0,n.useState)(),2),l=r[0],o=r[1],c=t.title&&t.title,i=t.description&&t.description,u=t.taxonomy_contact_category?t.taxonomy_contact_category[0].title:"";(0,n.useEffect)((function(){i.length>=150?o(i.substring(0,150)+"..."):o(i)}),[t]),h().locale("fr");var s=h()(t.created).startOf("minute").fromNow(),m=h()(t.modified).startOf("minute").fromNow();return n.createElement("div",{className:"r-list-item"},n.createElement("div",{className:t.image?"r-item-img":"r-item-img r-item-img-placeholder",style:{backgroundImage:t.image?"url("+t.image.scales.preview.download+")":""}}),n.createElement("div",{className:"r-item-text"},u?n.createElement("span",{className:"r-item-categorie"},u):"",n.createElement("span",{className:"r-item-title"},c),i?n.createElement("p",{className:"r-item-description"},l):"",n.createElement(a.rU,{className:"r-item-read-more",style:{textDecoration:"none"},to:{pathname:x()(t.title.replace(/\s/g,"-").toLowerCase()),search:"?u=".concat(t.UID),state:{idItem:t.UID}}},s===m?n.createElement("div",{className:"r-card-date-last"},n.createElement("span",null,"Publié "),n.createElement("span",null,s)):n.createElement("div",{className:"r-card-date-last"},n.createElement("span",null,"Actualisé "),n.createElement("span",null,m)))),n.createElement("div",{className:"r-item-arrow-more"}))},_=function(e){var t=e.contactArray,r=e.onChange;e.parentCallback;return n.createElement(n.Fragment,null,n.createElement("ul",{className:"r-result-list actu-result-list"},t.map((function(e,t){return n.createElement("li",{key:t,className:"r-list-item-group",onClick:function(){return t=e.UID,void r(t);var t}},n.createElement(a.rU,{className:"r-news-list-item-link",style:{textDecoration:"none"},to:{pathname:x()(e.title).replace(/[^a-zA-Z ]/g,"").replace(/\s/g,"-").toLowerCase(),search:"?u=".concat(e.UID),state:{idItem:e.UID}}},n.createElement(I,{contactItem:e,key:e.created})))}))))};function D(e){return D="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},D(e)}var H=["u"];function M(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function T(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?M(Object(r),!0).forEach((function(t){V(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):M(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function V(e,t,r){return(t=function(e){var t=function(e,t){if("object"!==D(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==D(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===D(t)?t:String(t)}(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function Z(e){return function(e){if(Array.isArray(e))return q(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||L(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function F(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,o,c=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(c.push(n.value),c.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(o=r.return(),Object(o)!==o))return}finally{if(u)throw a}}return c}}(e,t)||L(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function L(e,t){if(e){if("string"==typeof e)return q(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?q(e,t):void 0}}function q(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function R(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}function z(e){return n.createElement(a.UT,null,n.createElement(B,{queryFilterUrl:e.queryFilterUrl,queryUrl:e.queryUrl,proposeUrl:e.proposeUrl,batchSize:e.batchSize}))}var B=function(e){var t=r(31296),o=Object.assign({b_start:0,fullobjects:1},t.parse((0,v.Z)().toString())),i=(o.u,R(o,H)),u=F((0,n.useState)([]),2),s=u[0],m=u[1],f=F((0,n.useState)([]),2),p=f[0],b=f[1],y=F((0,n.useState)(null),2),g=(y[0],y[1]),h=F((0,n.useState)(i),2),E=h[0],w=h[1],O=F((0,n.useState)(0),2),S=O[0],j=O[1],N=F((0,n.useState)(!1),2),A=N[0],k=N[1],x=(0,c.Z)({method:"get",url:"",baseURL:e.queryUrl,headers:{Accept:"application/json"},params:E,load:A},[]),C=x.response,U=(x.error,x.isLoading),I=x.isMore;(0,n.useEffect)((function(){null!==C&&(m(I?function(e){return[].concat(Z(e),Z(C.items))}:C.items),b(C.items_total))}),[C]);var D,M=function(e){g(e)},V=function(e){k(!1),j((function(e){return 0})),w(e)};return(0,n.useEffect)((function(){w((function(e){return T(T({},e),{},{b_start:S})}))}),[S]),D=s&&s.length>0?n.createElement(_,{onChange:M,contactArray:s}):n.createElement("p",null,"Aucune actualité n'a été trouvée"),n.createElement("div",null,n.createElement(a.UT,null,n.createElement("div",{className:"r-wrapper r-actu-wrapper"},n.createElement("div",{className:"r-result r-annuaire-result"},n.createElement(l.rs,null,n.createElement(l.AW,{path:"/:name"},n.createElement(P,{onChange:M,onReturn:V,queryUrl:e.queryUrl})),n.createElement(l.AW,{exact:!0,path:"*"},n.createElement("div",{className:"r-result-filter actu-result-filter"},n.createElement(d,{url:e.queryFilterUrl,activeFilter:E,onChange:V}),e.proposeUrl&&n.createElement("div",{className:"r-add-news"},n.createElement("a",{target:"_blank",href:e.proposeUrl},"Proposer une actualité")),p>0?n.createElement("p",{className:"r-results-numbers"},n.createElement("span",null,p)," ",p>1?"Actualités trouvées":"Actualité trouvée"):n.createElement("p",{className:"r-results-numbers"},"Aucun résultat")),n.createElement("div",null,D),n.createElement("div",{className:"r-load-more"},p-e.batchSize>S?n.createElement("button",{onClick:function(){j((function(t){return t+e.batchSize})),k(!0)},className:"btn-grad"},U?"Chargement...":"Plus de résultats"):n.createElement("span",{className:"no-more-result"},U?"Chargement...":""))))))))}}}]);