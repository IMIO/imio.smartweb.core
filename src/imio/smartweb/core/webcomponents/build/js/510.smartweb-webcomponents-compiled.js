(self.webpackChunkimio_smartweb_core_webcomponents=self.webpackChunkimio_smartweb_core_webcomponents||[]).push([[510],{63779:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return R}});var n=r(78709),a=r(12707),l=r(55110),s=r(84106),c=r(14844),o=r(93580);function i(e){return i="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},i(e)}function u(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}function m(e){var t=function(e,t){if("object"!==i(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==i(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===i(t)?t:String(t)}function f(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function p(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?f(Object(r),!0).forEach((function(t){d(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):f(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function d(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function v(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,a,l=[],s=!0,c=!1;try{for(r=r.call(e);!(s=(n=r.next()).done)&&(l.push(n.value),!t||l.length!==t);s=!0);}catch(e){c=!0,a=e}finally{try{s||null==r.return||r.return()}finally{if(c)throw a}}return l}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return b(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return b(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function b(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var j=function(e){var t=(0,l.k6)(),a=r(31296),i=v((0,n.useState)(e.activeFilter),2),f=i[0],b=i[1],j=v((0,n.useState)(null),2),h=j[0],y=j[1],g=v((0,n.useState)(null),2),E=g[0],w=g[1],O=(0,c.Z)({method:"get",url:"",baseURL:e.url,headers:{Accept:"application/json"},params:f}),N=O.response;O.error,O.isLoading,(0,n.useEffect)((function(){if(null!==N){var e=N.topics.map((function(e){return{value:e.token,label:e.title}})),t=N.category?N.category.map((function(e){return{value:e.token,label:e.title}})):"";y(e),w(t)}}),[N]);var k=(0,n.useCallback)((function(e){var t=e.target,r=t.name,n=t.value;n.length>2?b((function(e){return p(p({},e),{},d({},r,n))}),[]):b((function(e){var t=p({},e);t[r];return u(t,[r].map(m))}))})),S=(0,n.useCallback)((function(e,t){var r=t.name;e?b((function(t){return p(p({},t),{},d({},r,e.value))}),[]):b((function(e){var t=p({},e);t[r];return u(t,[r].map(m))}))})),x=(0,n.useRef)(!0);(0,n.useEffect)((function(){x.current?x.current=!1:(t.push({pathname:"./",search:a.stringify(f)}),e.onChange(f))}),[f]);var A=h&&h.filter((function(t){return t.value===e.activeFilter.topics})),P=E&&E.filter((function(t){return t.value===e.activeFilter.category})),C={control:function(e){return p(p({},e),{},{backgroundColor:"white",borderRadius:"0",height:"50px"})},placeholder:function(e){return p(p({},e),{},{color:"000",fontWeight:"bold",fontSize:"12px",textTransform:"uppercase",letterSpacing:"1.2px"})},option:function(e,t){t.data,t.isDisabled,t.isFocused,t.isSelected;return p({},e)}};return n.createElement(n.Fragment,null,n.createElement("form",{className:"r-filter",onSubmit:function(t){t.preventDefault(),e.onChange(f)}},n.createElement("div",{className:"r-filter-search"},n.createElement(o.$H,null,(function(e){var t=e.translate;return n.createElement("input",{className:"input-custom-class",name:"SearchableText",type:"text",value:f.SearchableText,onChange:k,placeholder:t({text:"Recherche"})})})),n.createElement("button",{type:"submit"}))),n.createElement("div",{className:"r-filter topics-Filter"},n.createElement(o.$H,null,(function(e){var t=e.translate;return n.createElement(s.ZP,{styles:C,name:"topics",className:"select-custom-class library-topics",isClearable:!0,onChange:S,options:h&&h,placeholder:t({text:"Thématiques"}),value:A&&A[0]})}))),n.createElement("div",{className:"r-filter  facilities-Filter"},n.createElement(o.$H,null,(function(e){var t=e.translate;return n.createElement(s.ZP,{styles:C,name:"category",className:"select-custom-class library-facilities",isClearable:!0,onChange:S,options:E&&E,placeholder:t({text:"Catégories"}),value:P&&P[0]})}))))},h=r(6489),y=r(78279),g=r.n(y),E=(r(8047),r(78478));r(17110);function w(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,a,l=[],s=!0,c=!1;try{for(r=r.call(e);!(s=(n=r.next()).done)&&(l.push(n.value),!t||l.length!==t);s=!0);}catch(e){c=!0,a=e}finally{try{s||null==r.return||r.return()}finally{if(c)throw a}}return l}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return O(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return O(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function O(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function N(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function k(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?N(Object(r),!0).forEach((function(t){S(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):N(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function S(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}var x=function(e){var t=e.queryUrl,a=e.onChange,s=(0,l.k6)(),i=r(31296).parse((0,h.Z)().toString()),u=k(k({},i),{},{UID:i.u,fullobjects:1}),m=w((0,n.useState)(u),2),f=m[0],p=(m[1],w((0,n.useState)({}),2)),d=p[0],v=p[1],b=w((0,n.useState)(0),2),j=b[0],y=b[1],O=w((0,n.useState)(0),2),N=O[0],S=O[1],x=(0,c.Z)({method:"get",url:"",baseURL:t,headers:{Accept:"application/json"},params:f},[]),A=x.response;x.error,x.isLoading;(0,n.useEffect)((function(){null!==A&&v(A.items[0]),window.scrollTo(0,0)}),[A]),(0,n.useEffect)((function(){d.items&&d.items.length>0&&(y(d.items.filter((function(e){return"File"===e["@type"]}))),S(d.items.filter((function(e){return"Image"===e["@type"]}))))}),[d]),g().locale("fr");var P=g()(d.created).startOf("minute").fromNow(),C=g()(d.modified).startOf("minute").fromNow();return n.createElement("div",{className:"new-content r-content"},n.createElement("button",{type:"button",onClick:function(){s.push("./"),a(null)}},n.createElement(o.vN,{text:"Retour"})),n.createElement("article",null,n.createElement("header",null,n.createElement("h2",{className:"r-content-title"},d.title),n.createElement("div",{className:"r-content-description"},n.createElement(E.D,null,d.description))),n.createElement("figure",null,n.createElement("div",{className:"r-content-img",style:{backgroundImage:d.image?"url("+d.image.scales.affiche.download+")":""}})),n.createElement("div",{className:"r-content-news-info"},n.createElement("div",{className:"r-content-news-info-container"},n.createElement("div",{className:"r-content-news-info-schedul"},n.createElement("div",{className:"icon-baseline"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",preserveAspectRatio:"xMinYMin",viewBox:"0 0 19.41 19.41"},n.createElement("path",{d:"M16.09,2.74H14.35V.85a.44.44,0,0,0-.43-.44H12.47A.44.44,0,0,0,12,.85V2.74H7.38V.85A.44.44,0,0,0,7,.41H5.5a.44.44,0,0,0-.44.44V2.74H3.32A1.74,1.74,0,0,0,1.58,4.48V17.26A1.74,1.74,0,0,0,3.32,19H16.09a1.74,1.74,0,0,0,1.75-1.74V4.48A1.74,1.74,0,0,0,16.09,2.74Zm-.21,14.52H3.54A.22.22,0,0,1,3.32,17h0V6.22H16.09V17a.21.21,0,0,1-.21.22Z"}))),n.createElement("div",{className:"dpinlb"},n.createElement("div",{className:"r-content-news-info--date"},n.createElement("div",{className:"r-content-date"},P===C?n.createElement("div",{className:"r-content-date-publish"},n.createElement("span",null,"Publié ",P)):n.createElement("div",null,n.createElement("div",{className:"r-content-date-publish"},n.createElement("span",null,"Publié ",P)),n.createElement("div",{className:"r-card-date-last"},n.createElement("span",null,"Actualisé ",C," "))))))),null===d.site_url&&null===d.video_url?"":n.createElement("div",{className:"r-content-news-info-link"},n.createElement("div",{className:"icon-baseline"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},n.createElement("path",{d:"M16.36,2.22H3.06a1.3,1.3,0,0,0-1.3,1.3h0v9a1.3,1.3,0,0,0,1.3,1.3H7.52v1.74h-.7a.8.8,0,0,0,0,1.6h5.79a.8.8,0,0,0,0-1.6h-.7V13.85h4.45a1.31,1.31,0,0,0,1.3-1.3v-9A1.3,1.3,0,0,0,16.36,2.22Zm-1.9,10.83a.37.37,0,1,1,.36-.37h0a.36.36,0,0,1-.36.36Zm1.6.08a.45.45,0,1,1,.44-.45h0a.44.44,0,0,1-.44.45h0Zm.53-1.35H2.82V3.52a.23.23,0,0,1,.23-.23H16.36a.23.23,0,0,1,.23.23h0v8.27Z"}))),n.createElement("div",{className:"dpinlb"},null===d.site_url?"":n.createElement("div",{className:"r-content-news-info-event_link"},n.createElement("a",{href:d.site_url},d.site_url)),null===d.video_url?"":n.createElement("div",{className:"r-content-news-info--video"},n.createElement("a",{href:d.video_url},"Lien vers la vidéo")))),null===d.facebook&&null===d.instagram&&null===d.twitter?"":n.createElement("div",{className:"r-content-news-info-social"},n.createElement("ul",null,d.facebook?n.createElement("li",null,n.createElement("a",{href:d.facebook,target:"_blank"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-204.79995 -341.33325 1774.9329 2047.9995"},n.createElement("path",{d:"M1365.333 682.667C1365.333 305.64 1059.693 0 682.667 0 305.64 0 0 305.64 0 682.667c0 340.738 249.641 623.16 576 674.373V880H402.667V682.667H576v-150.4c0-171.094 101.917-265.6 257.853-265.6 74.69 0 152.814 13.333 152.814 13.333v168h-86.083c-84.804 0-111.25 52.623-111.25 106.61v128.057h189.333L948.4 880H789.333v477.04c326.359-51.213 576-333.635 576-674.373",fill:"#100f0d"}),n.createElement("path",{d:"M948.4 880l30.267-197.333H789.333V554.609C789.333 500.623 815.78 448 900.584 448h86.083V280s-78.124-13.333-152.814-13.333c-155.936 0-257.853 94.506-257.853 265.6v150.4H402.667V880H576v477.04a687.805 687.805 0 00106.667 8.293c36.288 0 71.91-2.84 106.666-8.293V880H948.4",fill:"#fff"})))):"",d.instagram?n.createElement("li",null,n.createElement("a",{href:d.instagram,target:"_blank"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-100.7682 -167.947 873.3244 1007.682"},n.createElement("g",{fill:"#100f0d"},n.createElement("path",{d:"M335.895 0c-91.224 0-102.663.387-138.49 2.021-35.752 1.631-60.169 7.31-81.535 15.612-22.088 8.584-40.82 20.07-59.493 38.743-18.674 18.673-30.16 37.407-38.743 59.495C9.33 137.236 3.653 161.653 2.02 197.405.386 233.232 0 244.671 0 335.895c0 91.222.386 102.661 2.02 138.488 1.633 35.752 7.31 60.169 15.614 81.534 8.584 22.088 20.07 40.82 38.743 59.495 18.674 18.673 37.405 30.159 59.493 38.743 21.366 8.302 45.783 13.98 81.535 15.612 35.827 1.634 47.266 2.021 138.49 2.021 91.222 0 102.661-.387 138.488-2.021 35.752-1.631 60.169-7.31 81.534-15.612 22.088-8.584 40.82-20.07 59.495-38.743 18.673-18.675 30.159-37.407 38.743-59.495 8.302-21.365 13.981-45.782 15.612-81.534 1.634-35.827 2.021-47.266 2.021-138.488 0-91.224-.387-102.663-2.021-138.49-1.631-35.752-7.31-60.169-15.612-81.534-8.584-22.088-20.07-40.822-38.743-59.495-18.675-18.673-37.407-30.159-59.495-38.743-21.365-8.302-45.782-13.981-81.534-15.612C438.556.387 427.117 0 335.895 0zm0 60.521c89.686 0 100.31.343 135.729 1.959 32.75 1.493 50.535 6.965 62.37 11.565 15.68 6.094 26.869 13.372 38.622 25.126 11.755 11.754 19.033 22.944 25.127 38.622 4.6 11.836 10.072 29.622 11.565 62.371 1.616 35.419 1.959 46.043 1.959 135.73 0 89.687-.343 100.311-1.959 135.73-1.493 32.75-6.965 50.535-11.565 62.37-6.094 15.68-13.372 26.869-25.127 38.622-11.753 11.755-22.943 19.033-38.621 25.127-11.836 4.6-29.622 10.072-62.371 11.565-35.413 1.616-46.036 1.959-135.73 1.959-89.694 0-100.315-.343-135.73-1.96-32.75-1.492-50.535-6.964-62.37-11.564-15.68-6.094-26.869-13.372-38.622-25.127-11.754-11.753-19.033-22.943-25.127-38.621-4.6-11.836-10.071-29.622-11.565-62.371-1.616-35.419-1.959-46.043-1.959-135.73 0-89.687.343-100.311 1.959-135.73 1.494-32.75 6.965-50.535 11.565-62.37 6.094-15.68 13.373-26.869 25.126-38.622 11.754-11.755 22.944-19.033 38.622-25.127 11.836-4.6 29.622-10.072 62.371-11.565 35.419-1.616 46.043-1.959 135.73-1.959"}),n.createElement("path",{d:"M335.895 447.859c-61.838 0-111.966-50.128-111.966-111.964 0-61.838 50.128-111.966 111.966-111.966 61.836 0 111.964 50.128 111.964 111.966 0 61.836-50.128 111.964-111.964 111.964zm0-284.451c-95.263 0-172.487 77.224-172.487 172.487 0 95.261 77.224 172.485 172.487 172.485 95.261 0 172.485-77.224 172.485-172.485 0-95.263-77.224-172.487-172.485-172.487m219.608-6.815c0 22.262-18.047 40.307-40.308 40.307-22.26 0-40.307-18.045-40.307-40.307 0-22.261 18.047-40.308 40.307-40.308 22.261 0 40.308 18.047 40.308 40.308"}))))):"",d.twitter?n.createElement("li",null,n.createElement("a",{href:d.twitter,target:"_blank"},n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-44.7006 -60.54775 387.4052 363.2865"},n.createElement("path",{fill:"#000",d:"M93.719 242.19c112.46 0 173.96-93.168 173.96-173.96 0-2.646-.054-5.28-.173-7.903a124.338 124.338 0 0030.498-31.66c-10.955 4.87-22.744 8.148-35.11 9.626 12.622-7.57 22.313-19.543 26.885-33.817a122.62 122.62 0 01-38.824 14.841C239.798 7.433 223.915 0 206.326 0c-33.764 0-61.144 27.381-61.144 61.132 0 4.798.537 9.465 1.586 13.941-50.815-2.557-95.874-26.886-126.03-63.88a60.977 60.977 0 00-8.279 30.73c0 21.212 10.794 39.938 27.208 50.893a60.685 60.685 0 01-27.69-7.647c-.009.257-.009.507-.009.781 0 29.61 21.075 54.332 49.051 59.934a61.218 61.218 0 01-16.122 2.152 60.84 60.84 0 01-11.491-1.103c7.784 24.293 30.355 41.971 57.115 42.465-20.926 16.402-47.287 26.171-75.937 26.171-4.929 0-9.798-.28-14.584-.846 27.059 17.344 59.189 27.464 93.722 27.464"})))):"")))),n.createElement("div",{className:"r-content-text",dangerouslySetInnerHTML:{__html:d.text&&d.text.data}}),j?n.createElement("div",{className:"r-content-files"},n.createElement("h2",{className:"r-content-files-title"},n.createElement(o.vN,{text:"Téléchargements"})),j.map((function(e){return n.createElement("div",{className:"r-content-file"},n.createElement("a",{href:e.targetUrl,className:"r-content-file-link",rel:"nofollow"},n.createElement("span",{className:"r-content-file-title"},e.title),n.createElement("span",{className:"r-content-file-icon"},n.createElement("svg",{width:"21",height:"21",viewBox:"0 0 24 24",fill:"none",stroke:"#8899a4","stroke-width":"2","stroke-linecap":"square","stroke-linejoin":"arcs"},n.createElement("path",{d:"M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"}))," ")))}))):"",N?n.createElement("div",{className:"r-content-gallery"},n.createElement("div",{class:"spotlight-group flexbin r-content-gallery"},N.map((function(e){return n.createElement("a",{class:"spotlight",href:e.image.scales.extralarge.download},n.createElement("img",{src:e.image.scales.preview.download}))})))):""))},A=(r(54570),r(29924)),P=r.n(A);function C(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,a,l=[],s=!0,c=!1;try{for(r=r.call(e);!(s=(n=r.next()).done)&&(l.push(n.value),!t||l.length!==t);s=!0);}catch(e){c=!0,a=e}finally{try{s||null==r.return||r.return()}finally{if(c)throw a}}return l}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return z(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return z(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function z(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var U=function(e){var t=e.contactItem,r=C((0,n.useState)(),2),l=r[0],s=r[1],c=t.title&&t.title,o=t.description&&t.description,i=t.taxonomy_contact_category?t.taxonomy_contact_category[0].title:"";(0,n.useEffect)((function(){o.length>=150?s(o.substring(0,150)+"..."):s(o)}),[t]),g().locale("fr");var u=g()(t.created).startOf("minute").fromNow(),m=g()(t.modified).startOf("minute").fromNow();return n.createElement("div",{className:"r-list-item"},n.createElement("div",{className:t.image?"r-item-img":"r-item-img r-item-img-placeholder",style:{backgroundImage:t.image?"url("+t.image.scales.preview.download+")":""}}),n.createElement("div",{className:"r-item-text"},i?n.createElement("span",{className:"r-item-categorie"},i):"",n.createElement("span",{className:"r-item-title"},c),o?n.createElement("p",{className:"r-item-description"},l):"",n.createElement(a.rU,{className:"r-item-read-more",style:{textDecoration:"none"},to:{pathname:P()(t.title.replace(/\s/g,"-").toLowerCase()),search:"?u=".concat(t.UID),state:{idItem:t.UID}}},u===m?n.createElement("div",{className:"r-card-date-last"},n.createElement("span",null,"Publié "),n.createElement("span",null,u)):n.createElement("div",{className:"r-card-date-last"},n.createElement("span",null,"Actualisé "),n.createElement("span",null,m)))),n.createElement("div",{className:"r-item-arrow-more"}))},I=function(e){var t=e.contactArray,r=e.onChange;e.parentCallback;return n.createElement(n.Fragment,null,n.createElement("ul",{className:"r-result-list actu-result-list"},t.map((function(e,t){return n.createElement("li",{key:t,className:"r-list-item-group",onClick:function(){return t=e.UID,void r(t);var t}},n.createElement(a.rU,{className:"r-news-list-item-link",style:{textDecoration:"none"},to:{pathname:P()(e.title).replace(/[^a-zA-Z ]/g,"").replace(/\s/g,"-").toLowerCase(),search:"?u=".concat(e.UID),state:{idItem:e.UID}}},n.createElement(U,{contactItem:e,key:e.created})))}))))},_=r(38401),D=["u"];function H(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function M(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?H(Object(r),!0).forEach((function(t){V(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):H(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function V(e,t,r){return t in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function T(e){return function(e){if(Array.isArray(e))return q(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||F(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function Z(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==r)return;var n,a,l=[],s=!0,c=!1;try{for(r=r.call(e);!(s=(n=r.next()).done)&&(l.push(n.value),!t||l.length!==t);s=!0);}catch(e){c=!0,a=e}finally{try{s||null==r.return||r.return()}finally{if(c)throw a}}return l}(e,t)||F(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function F(e,t){if(e){if("string"==typeof e)return q(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?q(e,t):void 0}}function q(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function L(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}function R(e){return n.createElement(a.UT,null,n.createElement(o.zt,{language:e.currentLanguage,translation:_.Z},n.createElement($,{queryFilterUrl:e.queryFilterUrl,queryUrl:e.queryUrl,proposeUrl:e.proposeUrl,batchSize:e.batchSize})))}var $=function(e){var t=r(31296),s=Object.assign({b_start:0,fullobjects:1},t.parse((0,h.Z)().toString())),i=(s.u,L(s,D)),u=Z((0,n.useState)([]),2),m=u[0],f=u[1],p=Z((0,n.useState)([]),2),d=p[0],v=p[1],b=Z((0,n.useState)(null),2),y=(b[0],b[1]),g=Z((0,n.useState)(i),2),E=g[0],w=g[1],O=Z((0,n.useState)(0),2),N=O[0],k=O[1],S=Z((0,n.useState)(!1),2),A=S[0],P=S[1],C=(0,c.Z)({method:"get",url:"",baseURL:e.queryUrl,headers:{Accept:"application/json"},params:E,load:A},[]),z=C.response,U=(C.error,C.isLoading),_=C.isMore;(0,n.useEffect)((function(){null!==z&&(f(_?function(e){return[].concat(T(e),T(z.items))}:z.items),v(z.items_total))}),[z]);var H,V=function(e){y(e)},F=function(e){P(!1),k((function(e){return 0})),w(e)};(0,n.useEffect)((function(){w((function(e){return M(M({},e),{},{b_start:N})}))}),[N]),m&&m.length>0?H=n.createElement(I,{onChange:V,contactArray:m}):U||(H=n.createElement("p",null,n.createElement(o.vN,{text:"Aucune actualité n'a été trouvée"})));var q=n.createElement("div",{className:"lds-roller-container"},n.createElement("div",{className:"lds-roller"},n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null)));return n.createElement("div",null,n.createElement(a.UT,null,n.createElement("div",{className:"r-wrapper r-actu-wrapper"},n.createElement("div",{className:"r-result r-annuaire-result"},n.createElement(l.rs,null,n.createElement(l.AW,{path:"/:name"},n.createElement(x,{onChange:V,onReturn:F,queryUrl:e.queryUrl})),n.createElement(l.AW,{exact:!0,path:"*"},n.createElement("div",{className:"r-result-filter actu-result-filter"},n.createElement(j,{url:e.queryFilterUrl,activeFilter:E,onChange:F}),e.proposeUrl&&n.createElement("div",{className:"r-add-news"},n.createElement("a",{target:"_blank",href:e.proposeUrl},n.createElement(o.vN,{text:"Proposer une actualité"}))),d>0?n.createElement("p",{className:"r-results-numbers"},n.createElement("span",null,d)," ",d>1?n.createElement(o.vN,{text:"Actualités trouvées"}):n.createElement(o.vN,{text:"Actualité trouvée"})):n.createElement("p",{className:"r-results-numbers"},n.createElement(o.vN,{text:"Aucun résultat"}))),n.createElement("div",null,H),n.createElement("div",{className:"r-load-more"},d-e.batchSize>N?n.createElement("div",null,n.createElement("span",{className:"no-more-result"},U?q:""),n.createElement("button",{onClick:function(){k((function(t){return t+e.batchSize})),P(!0)},className:"btn-grad"},U?n.createElement(o.vN,{text:"Chargement..."}):n.createElement(o.vN,{text:"Plus de résultats"}))):n.createElement("span",{className:"no-more-result"},U?q:""))))))))}},46700:function(e,t,r){var n={"./af":68435,"./af.js":68435,"./ar":99673,"./ar-dz":85296,"./ar-dz.js":85296,"./ar-kw":12855,"./ar-kw.js":12855,"./ar-ly":57896,"./ar-ly.js":57896,"./ar-ma":72309,"./ar-ma.js":72309,"./ar-sa":23097,"./ar-sa.js":23097,"./ar-tn":47728,"./ar-tn.js":47728,"./ar.js":99673,"./az":40336,"./az.js":40336,"./be":71140,"./be.js":71140,"./bg":94950,"./bg.js":94950,"./bm":46947,"./bm.js":46947,"./bn":81515,"./bn-bd":54062,"./bn-bd.js":54062,"./bn.js":81515,"./bo":28753,"./bo.js":28753,"./br":53423,"./br.js":53423,"./bs":94516,"./bs.js":94516,"./ca":87672,"./ca.js":87672,"./cs":31139,"./cs.js":31139,"./cv":84713,"./cv.js":84713,"./cy":25820,"./cy.js":25820,"./da":54131,"./da.js":54131,"./de":96647,"./de-at":53422,"./de-at.js":53422,"./de-ch":66246,"./de-ch.js":66246,"./de.js":96647,"./dv":68049,"./dv.js":68049,"./el":35006,"./el.js":35006,"./en-au":18006,"./en-au.js":18006,"./en-ca":59706,"./en-ca.js":59706,"./en-gb":67157,"./en-gb.js":67157,"./en-ie":16906,"./en-ie.js":16906,"./en-il":5089,"./en-il.js":5089,"./en-in":55304,"./en-in.js":55304,"./en-nz":22483,"./en-nz.js":22483,"./en-sg":98469,"./en-sg.js":98469,"./eo":41754,"./eo.js":41754,"./es":91488,"./es-do":98387,"./es-do.js":98387,"./es-mx":32657,"./es-mx.js":32657,"./es-us":99099,"./es-us.js":99099,"./es.js":91488,"./et":5318,"./et.js":5318,"./eu":74175,"./eu.js":74175,"./fa":9383,"./fa.js":9383,"./fi":71382,"./fi.js":71382,"./fil":18959,"./fil.js":18959,"./fo":77535,"./fo.js":77535,"./fr":80219,"./fr-ca":5886,"./fr-ca.js":5886,"./fr-ch":71967,"./fr-ch.js":71967,"./fr.js":80219,"./fy":76993,"./fy.js":76993,"./ga":18891,"./ga.js":18891,"./gd":29554,"./gd.js":29554,"./gl":11865,"./gl.js":11865,"./gom-deva":29485,"./gom-deva.js":29485,"./gom-latn":8869,"./gom-latn.js":8869,"./gu":54998,"./gu.js":54998,"./he":61248,"./he.js":61248,"./hi":91500,"./hi.js":91500,"./hr":56654,"./hr.js":56654,"./hu":34864,"./hu.js":34864,"./hy-am":36060,"./hy-am.js":36060,"./id":95942,"./id.js":95942,"./is":19921,"./is.js":19921,"./it":36781,"./it-ch":29378,"./it-ch.js":29378,"./it.js":36781,"./ja":72719,"./ja.js":72719,"./jv":86269,"./jv.js":86269,"./ka":70007,"./ka.js":70007,"./kk":91952,"./kk.js":91952,"./km":13540,"./km.js":13540,"./kn":67479,"./kn.js":67479,"./ko":99481,"./ko.js":99481,"./ku":19697,"./ku.js":19697,"./ky":640,"./ky.js":640,"./lb":94242,"./lb.js":94242,"./lo":75889,"./lo.js":75889,"./lt":72138,"./lt.js":72138,"./lv":69541,"./lv.js":69541,"./me":73972,"./me.js":73972,"./mi":18626,"./mi.js":18626,"./mk":14352,"./mk.js":14352,"./ml":6485,"./ml.js":6485,"./mn":6238,"./mn.js":6238,"./mr":61296,"./mr.js":61296,"./ms":47048,"./ms-my":95081,"./ms-my.js":95081,"./ms.js":47048,"./mt":7814,"./mt.js":7814,"./my":34059,"./my.js":34059,"./nb":16824,"./nb.js":16824,"./ne":74997,"./ne.js":74997,"./nl":421,"./nl-be":4341,"./nl-be.js":4341,"./nl.js":421,"./nn":38112,"./nn.js":38112,"./oc-lnc":63356,"./oc-lnc.js":63356,"./pa-in":29583,"./pa-in.js":29583,"./pl":86800,"./pl.js":86800,"./pt":90037,"./pt-br":79912,"./pt-br.js":79912,"./pt.js":90037,"./ro":88235,"./ro.js":88235,"./ru":8561,"./ru.js":8561,"./sd":32414,"./sd.js":32414,"./se":60947,"./se.js":60947,"./si":97081,"./si.js":97081,"./sk":5315,"./sk.js":5315,"./sl":59345,"./sl.js":59345,"./sq":1899,"./sq.js":1899,"./sr":4277,"./sr-cyrl":26466,"./sr-cyrl.js":26466,"./sr.js":4277,"./ss":59250,"./ss.js":59250,"./sv":55272,"./sv.js":55272,"./sw":40214,"./sw.js":40214,"./ta":86121,"./ta.js":86121,"./te":4182,"./te.js":4182,"./tet":14116,"./tet.js":14116,"./tg":63250,"./tg.js":63250,"./th":83111,"./th.js":83111,"./tk":12527,"./tk.js":12527,"./tl-ph":98104,"./tl-ph.js":98104,"./tlh":11751,"./tlh.js":11751,"./tr":67554,"./tr.js":67554,"./tzl":46061,"./tzl.js":46061,"./tzm":49236,"./tzm-latn":18447,"./tzm-latn.js":18447,"./tzm.js":49236,"./ug-cn":77693,"./ug-cn.js":77693,"./uk":35636,"./uk.js":35636,"./ur":10807,"./ur.js":10807,"./uz":28429,"./uz-latn":88105,"./uz-latn.js":88105,"./uz.js":28429,"./vi":59489,"./vi.js":59489,"./x-pseudo":30860,"./x-pseudo.js":30860,"./yo":26520,"./yo.js":26520,"./zh-cn":9599,"./zh-cn.js":9599,"./zh-hk":86433,"./zh-hk.js":86433,"./zh-mo":40381,"./zh-mo.js":40381,"./zh-tw":25759,"./zh-tw.js":25759};function a(e){var t=l(e);return r(t)}function l(e){if(!r.o(n,e)){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}return n[e]}a.keys=function(){return Object.keys(n)},a.resolve=l,e.exports=a,a.id=46700}}]);