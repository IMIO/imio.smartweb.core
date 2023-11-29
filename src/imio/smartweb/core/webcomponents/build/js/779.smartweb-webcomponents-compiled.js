"use strict";(self.webpackChunkimio_smartweb_core_webcomponents=self.webpackChunkimio_smartweb_core_webcomponents||[]).push([[779],{63779:function(e,t,r){r.r(t),r.d(t,{default:function(){return B}});var n=r(78709),a=r(12707),l=r(51031),c=r(7751),o=r(14844),i=r(93580);function u(e){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},u(e)}function s(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}function m(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function f(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?m(Object(r),!0).forEach((function(t){p(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):m(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function p(e,t,r){return(t=v(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function v(e){var t=function(e,t){if("object"!==u(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==u(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===u(t)?t:String(t)}function b(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,c,o=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(o.push(n.value),o.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(c=r.return(),Object(c)!==c))return}finally{if(u)throw a}}return o}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return y(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return y(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var d=function(e){var t=(0,l.k6)(),a=r(31296),u=b((0,n.useState)(e.activeFilter),2),m=u[0],y=u[1],d=b((0,n.useState)(null),2),g=d[0],h=d[1],E=b((0,n.useState)(null),2),w=E[0],O=E[1],S=(0,o.Z)({method:"get",url:"",baseURL:e.url,headers:{Accept:"application/json"},params:m}),j=S.response;S.error,S.isLoading,(0,n.useEffect)((function(){if(null!==j){var e=j.topics.map((function(e){return{value:e.token,label:e.title}})),t=j.category?j.category.map((function(e){return{value:e.token,label:e.title}})):"";h(e),O(t)}}),[j]);var N=(0,n.useCallback)((function(e){var t=e.target,r=t.name,n=t.value;n.length>2?y((function(e){return f(f({},e),{},p({},r,n))}),[]):y((function(e){var t=f({},e);t[r];return s(t,[r].map(v))}))})),x=(0,n.useCallback)((function(e,t){var r=t.name;e?y((function(t){return f(f({},t),{},p({},r,e.value))}),[]):y((function(e){var t=f({},e);t[r];return s(t,[r].map(v))}))})),A=(0,n.useRef)(!0);(0,n.useEffect)((function(){A.current?A.current=!1:(t.push({pathname:"./",search:a.stringify(m)}),e.onChange(m))}),[m]);var P=g&&g.filter((function(t){return t.value===e.activeFilter.topics})),_=w&&w.filter((function(t){return t.value===e.activeFilter.category})),k={control:function(e){return f(f({},e),{},{backgroundColor:"white",borderRadius:"0",height:"50px"})},placeholder:function(e){return f(f({},e),{},{color:"000",fontWeight:"bold",fontSize:"12px",textTransform:"uppercase",letterSpacing:"1.2px"})},option:function(e,t){t.data,t.isDisabled,t.isFocused,t.isSelected;return f({},e)}};return n.createElement(n.Fragment,null,n.createElement("form",{className:"r-filter",onSubmit:function(t){t.preventDefault(),e.onChange(m)}},n.createElement("div",{className:"r-filter-search"},n.createElement(i.$H,null,(function(e){var t=e.translate;return n.createElement("input",{className:"input-custom-class",name:"SearchableText",type:"text",value:m.SearchableText,onChange:N,placeholder:t({text:"Recherche"})})})),n.createElement("button",{type:"submit"}))),n.createElement("div",{className:"r-filter topics-Filter"},n.createElement(i.$H,null,(function(e){var t=e.translate;return n.createElement(c.ZP,{styles:k,name:"topics",className:"select-custom-class library-topics",isClearable:!0,onChange:x,options:g&&g,placeholder:t({text:"Thématiques"}),value:P&&P[0]})}))),n.createElement("div",{className:"r-filter  facilities-Filter"},n.createElement(i.$H,null,(function(e){var t=e.translate;return n.createElement(c.ZP,{styles:k,name:"category",className:"select-custom-class library-facilities",isClearable:!0,onChange:x,options:w&&w,placeholder:t({text:"Catégories"}),value:_&&_[0]})}))))},g=r(6489),h=r(78279),E=r.n(h),w=(r(8047),r(61584));r(17110);function O(e){return O="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},O(e)}function S(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,c,o=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(o.push(n.value),o.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(c=r.return(),Object(c)!==c))return}finally{if(u)throw a}}return o}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return j(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return j(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function j(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function N(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function x(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?N(Object(r),!0).forEach((function(t){A(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):N(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function A(e,t,r){return(t=function(e){var t=function(e,t){if("object"!==O(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==O(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===O(t)?t:String(t)}(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var P=function(e){var t=e.queryUrl,a=e.onChange,c=(0,l.k6)(),u=r(31296).parse((0,g.Z)().toString()),s=x(x({},u),{},{UID:u.u,fullobjects:1}),m=S((0,n.useState)(s),2),f=m[0],p=(m[1],S((0,n.useState)({}),2)),v=p[0],b=p[1],y=S((0,n.useState)(0),2),d=y[0],h=y[1],O=S((0,n.useState)(0),2),j=O[0],N=O[1],A=(0,o.Z)({method:"get",url:"",baseURL:t,headers:{Accept:"application/json"},params:f},[]),P=A.response;A.error,A.isLoading;(0,n.useEffect)((function(){null!==P&&b(P.items[0]),window.scrollTo(0,0)}),[P]),(0,n.useEffect)((function(){v.items&&v.items.length>0&&(h(v.items.filter((function(e){return"File"===e["@type"]}))),N(v.items.filter((function(e){return"Image"===e["@type"]}))))}),[v]),E().locale("fr");var _=E()(v.created).startOf("minute").fromNow(),k=E()(v.modified).startOf("minute").fromNow();return n.createElement("div",{className:"new-content r-content"},n.createElement("button",{type:"button",onClick:function(){c.push("./"),a(null)}},n.createElement(i.vN,{text:"Retour"})),n.createElement("article",null,n.createElement("header",null,n.createElement("h2",{className:"r-content-title"},v.title),n.createElement("div",{className:"r-content-description"},n.createElement(w.D,null,v.description))),n.createElement("figure",null,n.createElement("div",{className:"r-content-img",style:{backgroundImage:v.image_affiche_scale?"url("+v.image_affiche_scale+")":""}})),n.createElement("div",{className:"r-content-news-info"},n.createElement("div",{className:"r-content-news-info-container"},n.createElement("div",{className:"r-content-news-info-schedul"},n.createElement("div",{className:"icon-baseline"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",preserveAspectRatio:"xMinYMin",viewBox:"0 0 19.41 19.41"},n.createElement("path",{d:"M16.09,2.74H14.35V.85a.44.44,0,0,0-.43-.44H12.47A.44.44,0,0,0,12,.85V2.74H7.38V.85A.44.44,0,0,0,7,.41H5.5a.44.44,0,0,0-.44.44V2.74H3.32A1.74,1.74,0,0,0,1.58,4.48V17.26A1.74,1.74,0,0,0,3.32,19H16.09a1.74,1.74,0,0,0,1.75-1.74V4.48A1.74,1.74,0,0,0,16.09,2.74Zm-.21,14.52H3.54A.22.22,0,0,1,3.32,17h0V6.22H16.09V17a.21.21,0,0,1-.21.22Z"}))),n.createElement("div",{className:"dpinlb"},n.createElement("div",{className:"r-content-news-info--date"},n.createElement("div",{className:"r-content-date"},_===k?n.createElement("div",{className:"r-content-date-publish"},n.createElement("span",null,"Publié ",_)):n.createElement("div",null,n.createElement("div",{className:"r-content-date-publish"},n.createElement("span",null,"Publié ",_)),n.createElement("div",{className:"r-card-date-last"},n.createElement("span",null,"Actualisé ",k," "))))))),null===v.site_url&&null===v.video_url?"":n.createElement("div",{className:"r-content-news-info-link"},n.createElement("div",{className:"icon-baseline"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},n.createElement("path",{d:"M16.36,2.22H3.06a1.3,1.3,0,0,0-1.3,1.3h0v9a1.3,1.3,0,0,0,1.3,1.3H7.52v1.74h-.7a.8.8,0,0,0,0,1.6h5.79a.8.8,0,0,0,0-1.6h-.7V13.85h4.45a1.31,1.31,0,0,0,1.3-1.3v-9A1.3,1.3,0,0,0,16.36,2.22Zm-1.9,10.83a.37.37,0,1,1,.36-.37h0a.36.36,0,0,1-.36.36Zm1.6.08a.45.45,0,1,1,.44-.45h0a.44.44,0,0,1-.44.45h0Zm.53-1.35H2.82V3.52a.23.23,0,0,1,.23-.23H16.36a.23.23,0,0,1,.23.23h0v8.27Z"}))),n.createElement("div",{className:"dpinlb"},null===v.site_url?"":n.createElement("div",{className:"r-content-news-info-event_link"},n.createElement("a",{href:v.site_url},v.site_url)),null===v.video_url?"":n.createElement("div",{className:"r-content-news-info--video"},n.createElement("a",{href:v.video_url},"Lien vers la vidéo")))),null===v.facebook&&null===v.instagram&&null===v.twitter?"":n.createElement("div",{className:"r-content-news-info-social"},n.createElement("ul",null,v.facebook?n.createElement("li",null,n.createElement("a",{href:v.facebook,target:"_blank"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-204.79995 -341.33325 1774.9329 2047.9995"},n.createElement("path",{d:"M1365.333 682.667C1365.333 305.64 1059.693 0 682.667 0 305.64 0 0 305.64 0 682.667c0 340.738 249.641 623.16 576 674.373V880H402.667V682.667H576v-150.4c0-171.094 101.917-265.6 257.853-265.6 74.69 0 152.814 13.333 152.814 13.333v168h-86.083c-84.804 0-111.25 52.623-111.25 106.61v128.057h189.333L948.4 880H789.333v477.04c326.359-51.213 576-333.635 576-674.373",fill:"#100f0d"}),n.createElement("path",{d:"M948.4 880l30.267-197.333H789.333V554.609C789.333 500.623 815.78 448 900.584 448h86.083V280s-78.124-13.333-152.814-13.333c-155.936 0-257.853 94.506-257.853 265.6v150.4H402.667V880H576v477.04a687.805 687.805 0 00106.667 8.293c36.288 0 71.91-2.84 106.666-8.293V880H948.4",fill:"#fff"})))):"",v.instagram?n.createElement("li",null,n.createElement("a",{href:v.instagram,target:"_blank"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-100.7682 -167.947 873.3244 1007.682"},n.createElement("g",{fill:"#100f0d"},n.createElement("path",{d:"M335.895 0c-91.224 0-102.663.387-138.49 2.021-35.752 1.631-60.169 7.31-81.535 15.612-22.088 8.584-40.82 20.07-59.493 38.743-18.674 18.673-30.16 37.407-38.743 59.495C9.33 137.236 3.653 161.653 2.02 197.405.386 233.232 0 244.671 0 335.895c0 91.222.386 102.661 2.02 138.488 1.633 35.752 7.31 60.169 15.614 81.534 8.584 22.088 20.07 40.82 38.743 59.495 18.674 18.673 37.405 30.159 59.493 38.743 21.366 8.302 45.783 13.98 81.535 15.612 35.827 1.634 47.266 2.021 138.49 2.021 91.222 0 102.661-.387 138.488-2.021 35.752-1.631 60.169-7.31 81.534-15.612 22.088-8.584 40.82-20.07 59.495-38.743 18.673-18.675 30.159-37.407 38.743-59.495 8.302-21.365 13.981-45.782 15.612-81.534 1.634-35.827 2.021-47.266 2.021-138.488 0-91.224-.387-102.663-2.021-138.49-1.631-35.752-7.31-60.169-15.612-81.534-8.584-22.088-20.07-40.822-38.743-59.495-18.675-18.673-37.407-30.159-59.495-38.743-21.365-8.302-45.782-13.981-81.534-15.612C438.556.387 427.117 0 335.895 0zm0 60.521c89.686 0 100.31.343 135.729 1.959 32.75 1.493 50.535 6.965 62.37 11.565 15.68 6.094 26.869 13.372 38.622 25.126 11.755 11.754 19.033 22.944 25.127 38.622 4.6 11.836 10.072 29.622 11.565 62.371 1.616 35.419 1.959 46.043 1.959 135.73 0 89.687-.343 100.311-1.959 135.73-1.493 32.75-6.965 50.535-11.565 62.37-6.094 15.68-13.372 26.869-25.127 38.622-11.753 11.755-22.943 19.033-38.621 25.127-11.836 4.6-29.622 10.072-62.371 11.565-35.413 1.616-46.036 1.959-135.73 1.959-89.694 0-100.315-.343-135.73-1.96-32.75-1.492-50.535-6.964-62.37-11.564-15.68-6.094-26.869-13.372-38.622-25.127-11.754-11.753-19.033-22.943-25.127-38.621-4.6-11.836-10.071-29.622-11.565-62.371-1.616-35.419-1.959-46.043-1.959-135.73 0-89.687.343-100.311 1.959-135.73 1.494-32.75 6.965-50.535 11.565-62.37 6.094-15.68 13.373-26.869 25.126-38.622 11.754-11.755 22.944-19.033 38.622-25.127 11.836-4.6 29.622-10.072 62.371-11.565 35.419-1.616 46.043-1.959 135.73-1.959"}),n.createElement("path",{d:"M335.895 447.859c-61.838 0-111.966-50.128-111.966-111.964 0-61.838 50.128-111.966 111.966-111.966 61.836 0 111.964 50.128 111.964 111.966 0 61.836-50.128 111.964-111.964 111.964zm0-284.451c-95.263 0-172.487 77.224-172.487 172.487 0 95.261 77.224 172.485 172.487 172.485 95.261 0 172.485-77.224 172.485-172.485 0-95.263-77.224-172.487-172.485-172.487m219.608-6.815c0 22.262-18.047 40.307-40.308 40.307-22.26 0-40.307-18.045-40.307-40.307 0-22.261 18.047-40.308 40.307-40.308 22.261 0 40.308 18.047 40.308 40.308"}))))):"",v.twitter?n.createElement("li",null,n.createElement("a",{href:v.twitter,target:"_blank"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-44.7006 -60.54775 387.4052 363.2865"},n.createElement("path",{fill:"#000",d:"M93.719 242.19c112.46 0 173.96-93.168 173.96-173.96 0-2.646-.054-5.28-.173-7.903a124.338 124.338 0 0030.498-31.66c-10.955 4.87-22.744 8.148-35.11 9.626 12.622-7.57 22.313-19.543 26.885-33.817a122.62 122.62 0 01-38.824 14.841C239.798 7.433 223.915 0 206.326 0c-33.764 0-61.144 27.381-61.144 61.132 0 4.798.537 9.465 1.586 13.941-50.815-2.557-95.874-26.886-126.03-63.88a60.977 60.977 0 00-8.279 30.73c0 21.212 10.794 39.938 27.208 50.893a60.685 60.685 0 01-27.69-7.647c-.009.257-.009.507-.009.781 0 29.61 21.075 54.332 49.051 59.934a61.218 61.218 0 01-16.122 2.152 60.84 60.84 0 01-11.491-1.103c7.784 24.293 30.355 41.971 57.115 42.465-20.926 16.402-47.287 26.171-75.937 26.171-4.929 0-9.798-.28-14.584-.846 27.059 17.344 59.189 27.464 93.722 27.464"})))):"")))),n.createElement("div",{className:"r-content-text",dangerouslySetInnerHTML:{__html:v.text&&v.text.data}}),d?n.createElement("div",{className:"r-content-files"},d.map((function(e){return n.createElement("div",{className:"r-content-file"},n.createElement("a",{href:e.targetUrl,className:"r-content-file-link",rel:"nofollow"},n.createElement("span",{className:"r-content-file-title"},e.title),n.createElement("span",{className:"r-content-file-icon"},n.createElement("svg",{width:"21",height:"21",viewBox:"0 0 24 24",fill:"none",stroke:"#8899a4","stroke-width":"2","stroke-linecap":"square","stroke-linejoin":"arcs"},n.createElement("path",{d:"M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"}))," ")))}))):"",j?n.createElement("div",{className:"r-content-gallery"},n.createElement("div",{class:"spotlight-group flexbin r-content-gallery"},j.map((function(e){return n.createElement("a",{class:"spotlight",href:e.image_extralarge_scale},n.createElement("img",{src:e.image_preview_scale}))})))):""))},_=r(29924),k=r.n(_);function C(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,c,o=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(o.push(n.value),o.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(c=r.return(),Object(c)!==c))return}finally{if(u)throw a}}return o}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return I(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return I(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function I(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var U=function(e){var t=e.contactItem,r=C((0,n.useState)(),2),l=r[0],c=r[1],o=t.title&&t.title,i=t.description&&t.description,u=t.taxonomy_contact_category?t.taxonomy_contact_category[0].title:"";(0,n.useEffect)((function(){i.length>=150?c(i.substring(0,150)+"..."):c(i)}),[t]),E().locale("fr");var s=E()(t.created).startOf("minute").fromNow(),m=E()(t.modified).startOf("minute").fromNow();return n.createElement("div",{className:"r-list-item"},n.createElement("div",{className:t.image_preview_scale?"r-item-img":"r-item-img r-item-img-placeholder",style:{backgroundImage:t.image_preview_scale?"url("+t.image_preview_scale+")":""}}),n.createElement("div",{className:"r-item-text"},u?n.createElement("span",{className:"r-item-categorie"},u):"",n.createElement("span",{className:"r-item-title"},o),i?n.createElement(w.D,{className:"r-item-description"},l):"",n.createElement(a.rU,{className:"r-item-read-more",style:{textDecoration:"none"},to:{pathname:k()(t.title.replace(/\s/g,"-").toLowerCase()),search:"?u=".concat(t.UID),state:{idItem:t.UID}}},s===m?n.createElement("div",{className:"r-card-date-last"},n.createElement("span",null,"Publié "),n.createElement("span",null,s)):n.createElement("div",{className:"r-card-date-last"},n.createElement("span",null,"Actualisé "),n.createElement("span",null,m)))),n.createElement("div",{className:"r-item-arrow-more"}))},D=function(e){var t=e.contactArray,r=e.onChange;e.parentCallback;return n.createElement(n.Fragment,null,n.createElement("ul",{className:"r-result-list actu-result-list"},t.map((function(e,t){return n.createElement("li",{key:t,className:"r-list-item-group",onClick:function(){return t=e.UID,void r(t);var t}},n.createElement(a.rU,{className:"r-news-list-item-link",style:{textDecoration:"none"},to:{pathname:k()(e.title).replace(/[^a-zA-Z ]/g,"").replace(/\s/g,"-").toLowerCase(),search:"?u=".concat(e.UID),state:{idItem:e.UID}}},n.createElement(U,{contactItem:e,key:e.created})))}))))},H=r(38401);function M(e){return M="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},M(e)}var V=["u"];function T(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function Z(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?T(Object(r),!0).forEach((function(t){F(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):T(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function F(e,t,r){return(t=function(e){var t=function(e,t){if("object"!==M(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==M(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===M(t)?t:String(t)}(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function L(e){return function(e){if(Array.isArray(e))return R(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||z(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function q(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,c,o=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(o.push(n.value),o.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(c=r.return(),Object(c)!==c))return}finally{if(u)throw a}}return o}}(e,t)||z(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function z(e,t){if(e){if("string"==typeof e)return R(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?R(e,t):void 0}}function R(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function $(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}function B(e){return n.createElement(a.UT,null,n.createElement(i.zt,{language:e.currentLanguage,translation:H.Z},n.createElement(W,{queryFilterUrl:e.queryFilterUrl,queryUrl:e.queryUrl,proposeUrl:e.proposeUrl,batchSize:e.batchSize})))}var W=function(e){var t=r(31296),c=Object.assign({b_start:0,fullobjects:1},t.parse((0,g.Z)().toString())),u=(c.u,$(c,V)),s=q((0,n.useState)([]),2),m=s[0],f=s[1],p=q((0,n.useState)([]),2),v=p[0],b=p[1],y=q((0,n.useState)(null),2),h=(y[0],y[1]),E=q((0,n.useState)(u),2),w=E[0],O=E[1],S=q((0,n.useState)(0),2),j=S[0],N=S[1],x=q((0,n.useState)(!1),2),A=x[0],_=x[1],k=(0,o.Z)({method:"get",url:"",baseURL:e.queryUrl,headers:{Accept:"application/json"},params:w,load:A},[]),C=k.response,I=(k.error,k.isLoading),U=k.isMore;(0,n.useEffect)((function(){null!==C&&(f(U?function(e){return[].concat(L(e),L(C.items))}:C.items),b(C.items_total))}),[C]);var H,M=function(e){h(e)},T=function(e){_(!1),N((function(e){return 0})),O(e)};(0,n.useEffect)((function(){O((function(e){return Z(Z({},e),{},{b_start:j})}))}),[j]),m&&m.length>0?H=n.createElement(D,{onChange:M,contactArray:m}):I||(H=n.createElement("p",null,n.createElement(i.vN,{text:"Aucune actualité n'a été trouvée"})));var F=n.createElement("div",{className:"lds-roller-container"},n.createElement("div",{className:"lds-roller"},n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null)));return n.createElement("div",null,n.createElement(a.UT,null,n.createElement("div",{className:"r-wrapper r-actu-wrapper"},n.createElement("div",{className:"r-result r-annuaire-result"},n.createElement(l.rs,null,n.createElement(l.AW,{path:"/:name"},n.createElement(P,{onChange:M,onReturn:T,queryUrl:e.queryUrl})),n.createElement(l.AW,{exact:!0,path:"*"},n.createElement("div",{className:"r-result-filter actu-result-filter"},n.createElement(d,{url:e.queryFilterUrl,activeFilter:w,onChange:T}),e.proposeUrl&&n.createElement("div",{className:"r-add-news"},n.createElement("a",{target:"_blank",href:e.proposeUrl},n.createElement(i.vN,{text:"Proposer une actualité"}))),v>0?n.createElement("p",{className:"r-results-numbers"},n.createElement("span",null,v)," ",v>1?n.createElement(i.vN,{text:"Actualités trouvées"}):n.createElement(i.vN,{text:"Actualité trouvée"})):n.createElement("p",{className:"r-results-numbers"},n.createElement(i.vN,{text:"Aucun résultat"}))),n.createElement("div",null,H),n.createElement("div",{className:"r-load-more"},v-e.batchSize>j?n.createElement("div",null,n.createElement("span",{className:"no-more-result"},I?F:""),n.createElement("button",{onClick:function(){N((function(t){return t+parseInt(e.batchSize)})),_(!0)},className:"btn-grad"},I?n.createElement(i.vN,{text:"Chargement..."}):n.createElement(i.vN,{text:"Plus de résultats"}))):n.createElement("span",{className:"no-more-result"},I?F:""))))))))}}}]);