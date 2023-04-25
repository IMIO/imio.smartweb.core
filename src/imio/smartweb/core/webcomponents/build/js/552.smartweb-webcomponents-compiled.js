"use strict";(self.webpackChunkimio_smartweb_core_webcomponents=self.webpackChunkimio_smartweb_core_webcomponents||[]).push([[552],{67676:function(e,t,r){r(78709);t.Z=r.p+"assets/pin-react-active.07d154037a15be5525b823fdc626cf29.svg"},59834:function(e,t,r){r(78709);t.Z=r.p+"assets/pin-react.fda934b5daf26dd4da2a71a7e7e44431.svg"},90552:function(e,t,r){r.r(t),r.d(t,{default:function(){return Y}});var n=r(78709),a=r(12707),l=r(51031),c=r(71775),o=r(14844),i=r(93580);function u(e){return u="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},u(e)}function s(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}function m(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function f(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?m(Object(r),!0).forEach((function(t){p(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):m(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function p(e,t,r){return(t=y(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function y(e){var t=function(e,t){if("object"!==u(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==u(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===u(t)?t:String(t)}function v(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,c,o=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(o.push(n.value),o.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(c=r.return(),Object(c)!==c))return}finally{if(u)throw a}}return o}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return d(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return d(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function d(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}var g=function(e){var t=(0,l.k6)(),a=r(31296),u=v((0,n.useState)(e.activeFilter),2),m=u[0],d=u[1],g=v((0,n.useState)(null),2),h=g[0],b=g[1],E=v((0,n.useState)(null),2),w=E[0],S=E[1],O=v((0,n.useState)(null),2),N=O[0],j=O[1],x=(0,o.Z)({method:"get",url:"",baseURL:e.url,headers:{Accept:"application/json"},params:m}),I=x.response;x.error,x.isLoading,(0,n.useEffect)((function(){if(null!==I){var e=I.topics&&I.topics.map((function(e){return{value:e.token,label:e.title}})),t=I.taxonomy_contact_category&&I.taxonomy_contact_category.map((function(e){return{value:e.token,label:e.title}})),r=I.facilities&&I.facilities.map((function(e){return{value:e.token,label:e.title}}));b(e),S(t),j(r)}}),[I]);var k=(0,n.useCallback)((function(e){var t=e.target,r=t.name,n=t.value;n.length>2?d((function(e){return f(f({},e),{},p({},r,n))}),[]):d((function(e){var t=f({},e);t[r];return s(t,[r].map(y))}))})),_=(0,n.useCallback)((function(e,t){var r=t.name;e?d((function(t){return f(f({},t),{},p({},r,e.value))}),[]):d((function(e){var t=f({},e);t[r];return s(t,[r].map(y))}))})),A=(0,n.useRef)(!0);(0,n.useEffect)((function(){A.current?A.current=!1:(t.push({pathname:"./",search:a.stringify(m)}),e.onChange(m))}),[m]);var U=h&&h.filter((function(t){return t.value===e.activeFilter.topics})),C=w&&w.filter((function(t){return t.value===e.activeFilter.taxonomy_contact_category})),P=N&&N.filter((function(t){return t.value===e.activeFilter.facilities})),D={control:function(e){return f(f({},e),{},{backgroundColor:"white",borderRadius:"0",height:"50px"})},placeholder:function(e){return f(f({},e),{},{color:"000",fontWeight:"bold",fontSize:"12px",textTransform:"uppercase",letterSpacing:"1.2px"})},option:function(e,t){t.data,t.isDisabled,t.isFocused,t.isSelected;return f({},e)}};return n.createElement(n.Fragment,null,n.createElement("form",{className:"r-filter",onSubmit:function(t){t.preventDefault(),e.onChange(m)}},n.createElement("div",{className:"r-filter-search"},n.createElement(i.$H,null,(function(e){var t=e.translate;return n.createElement("input",{className:"input-custom-class",name:"SearchableText",type:"text",value:m.SearchableText,onChange:k,placeholder:t({text:"Recherche"})})})),n.createElement("button",{type:"submit"}))),n.createElement("div",{className:"r-filter topics-Filter"},n.createElement(i.$H,null,(function(e){var t=e.translate;return n.createElement(c.ZP,{styles:D,name:"topics",className:"select-custom-class library-topics",isClearable:!0,onChange:_,options:h&&h,placeholder:t({text:"Thématiques"}),value:U&&U[0]})}))),n.createElement("div",{className:"r-filter  facilities-Filter"},n.createElement(i.$H,null,(function(e){var t=e.translate;return n.createElement(c.ZP,{styles:D,name:"taxonomy_contact_category_for_filtering",className:"select-custom-class library-facilities",isClearable:!0,onChange:_,options:w&&w,placeholder:t({text:"Catégories"}),value:C&&C[0]})}))),n.createElement("div",{className:"r-filter  facilities-Filter"},n.createElement(i.$H,null,(function(e){var t=e.translate;return n.createElement(c.ZP,{styles:D,name:"facilities",className:"select-custom-class library-facilities",isClearable:!0,onChange:_,options:N&&N,placeholder:t({text:"Facilités"}),value:P&&P[0]})}))))},h=r(6489),b=r(2241),E=(r(17110),["u"]);function w(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,c,o=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(o.push(n.value),o.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(c=r.return(),Object(c)!==c))return}finally{if(u)throw a}}return o}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return S(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return S(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function S(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function O(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}var N=function(e){var t=e.queryUrl,a=e.onChange,c=(0,l.k6)(),u=r(31296),s=Object.assign({UID:u.parse((0,h.Z)().toString()).u,fullobjects:1}),m=(s.u,O(s,E)),f=w((0,n.useState)(m),2),p=f[0],y=f[1],v=w((0,n.useState)({}),2),d=v[0],g=v[1],S=w((0,n.useState)(0),2),N=S[0],j=S[1],x=w((0,n.useState)(0),2),I=x[0],k=x[1],_=(0,o.Z)({method:"get",url:"",baseURL:t,headers:{Accept:"application/json"},params:p},[]),A=_.response;_.error,_.isLoading;(0,n.useEffect)((function(){y(m)}),[u.parse((0,h.Z)().toString()).u]),(0,n.useEffect)((function(){null!==A&&g(A.items[0]),window.scrollTo(0,0)}),[A]),(0,n.useEffect)((function(){d.items&&d.items.length>0&&(j(d.items.filter((function(e){return"File"===e["@type"]}))),k(d.items.filter((function(e){return"Image"===e["@type"]}))))}),[d]);var U=d.country&&d.country.title,C="https://www.google.com/maps/dir/?api=1&destination="+d.street+"+"+d.number+"+"+d.complement+"+"+d.zipcode+"+"+d.city+"+"+U;return C=C.replaceAll("+null",""),n.createElement("div",{className:"annuaire-content r-content"},n.createElement("button",{type:"button",onClick:function(){c.push("./"),a(null)}},n.createElement(i.vN,{text:"Retour"})),n.createElement("article",null,n.createElement("header",null,n.createElement("h2",{className:"r-content-title"},d.title),d.subtitle?n.createElement("h3",{className:"r-content-subtitle"},d.subtitle):""),d.logo?n.createElement("figure",null,n.createElement("img",{className:"r-content-img",src:d.logo_thumb_scale,alt:d.logo.filename})):""),n.createElement("div",{className:"contactCard"},n.createElement("div",{className:"contactText"},n.createElement("div",{className:"r-content-description"},n.createElement(b.D,null,d.description)),n.createElement("div",{className:"contactTextAll"},d.category?n.createElement("span",null,d.category):"",n.createElement("div",{className:"adresse"},d.number?n.createElement("span",null,d.number+" "):"",d.street?n.createElement("span",null,d.street+", "):"",d.complement?n.createElement("span",null,d.complement+", "):"",d.zipcode?n.createElement("span",null,d.zipcode+" "):"",d.city?n.createElement("span",null,d.city):""),n.createElement("div",{className:"itineraty"},d.street?n.createElement("a",{href:C,target:"_blank"},"Itinéraire"):""),n.createElement("div",{className:"phones"},d.phones?d.phones.map((function(e){return n.createElement("span",null,n.createElement("a",{href:"tel:"+e.number},e.number))})):""),n.createElement("div",{className:"mails"},d.mails?d.mails.map((function(e){return n.createElement("span",null,n.createElement("a",{href:"mailto:"+e.mail_address},e.mail_address))})):""),n.createElement("div",{className:"urls"},d.urls?d.urls.map((function(e){return n.createElement(n.Fragment,null,n.createElement("span",null,n.createElement("a",{href:e.url,target:"_blank"},"facebook"===e.type?n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"40",width:"60",viewBox:"-204.79995 -341.33325 1774.9329 2047.9995"},n.createElement("path",{d:"M1365.333 682.667C1365.333 305.64 1059.693 0 682.667 0 305.64 0 0 305.64 0 682.667c0 340.738 249.641 623.16 576 674.373V880H402.667V682.667H576v-150.4c0-171.094 101.917-265.6 257.853-265.6 74.69 0 152.814 13.333 152.814 13.333v168h-86.083c-84.804 0-111.25 52.623-111.25 106.61v128.057h189.333L948.4 880H789.333v477.04c326.359-51.213 576-333.635 576-674.373",fill:"#100f0d"}),n.createElement("path",{d:"M948.4 880l30.267-197.333H789.333V554.609C789.333 500.623 815.78 448 900.584 448h86.083V280s-78.124-13.333-152.814-13.333c-155.936 0-257.853 94.506-257.853 265.6v150.4H402.667V880H576v477.04a687.805 687.805 0 00106.667 8.293c36.288 0 71.91-2.84 106.666-8.293V880H948.4",fill:"#fff"})):"instagram"===e.type?n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"40",width:"60",viewBox:"-100.7682 -167.947 873.3244 1007.682"},n.createElement("g",{fill:"#100f0d"},n.createElement("path",{d:"M335.895 0c-91.224 0-102.663.387-138.49 2.021-35.752 1.631-60.169 7.31-81.535 15.612-22.088 8.584-40.82 20.07-59.493 38.743-18.674 18.673-30.16 37.407-38.743 59.495C9.33 137.236 3.653 161.653 2.02 197.405.386 233.232 0 244.671 0 335.895c0 91.222.386 102.661 2.02 138.488 1.633 35.752 7.31 60.169 15.614 81.534 8.584 22.088 20.07 40.82 38.743 59.495 18.674 18.673 37.405 30.159 59.493 38.743 21.366 8.302 45.783 13.98 81.535 15.612 35.827 1.634 47.266 2.021 138.49 2.021 91.222 0 102.661-.387 138.488-2.021 35.752-1.631 60.169-7.31 81.534-15.612 22.088-8.584 40.82-20.07 59.495-38.743 18.673-18.675 30.159-37.407 38.743-59.495 8.302-21.365 13.981-45.782 15.612-81.534 1.634-35.827 2.021-47.266 2.021-138.488 0-91.224-.387-102.663-2.021-138.49-1.631-35.752-7.31-60.169-15.612-81.534-8.584-22.088-20.07-40.822-38.743-59.495-18.675-18.673-37.407-30.159-59.495-38.743-21.365-8.302-45.782-13.981-81.534-15.612C438.556.387 427.117 0 335.895 0zm0 60.521c89.686 0 100.31.343 135.729 1.959 32.75 1.493 50.535 6.965 62.37 11.565 15.68 6.094 26.869 13.372 38.622 25.126 11.755 11.754 19.033 22.944 25.127 38.622 4.6 11.836 10.072 29.622 11.565 62.371 1.616 35.419 1.959 46.043 1.959 135.73 0 89.687-.343 100.311-1.959 135.73-1.493 32.75-6.965 50.535-11.565 62.37-6.094 15.68-13.372 26.869-25.127 38.622-11.753 11.755-22.943 19.033-38.621 25.127-11.836 4.6-29.622 10.072-62.371 11.565-35.413 1.616-46.036 1.959-135.73 1.959-89.694 0-100.315-.343-135.73-1.96-32.75-1.492-50.535-6.964-62.37-11.564-15.68-6.094-26.869-13.372-38.622-25.127-11.754-11.753-19.033-22.943-25.127-38.621-4.6-11.836-10.071-29.622-11.565-62.371-1.616-35.419-1.959-46.043-1.959-135.73 0-89.687.343-100.311 1.959-135.73 1.494-32.75 6.965-50.535 11.565-62.37 6.094-15.68 13.373-26.869 25.126-38.622 11.754-11.755 22.944-19.033 38.622-25.127 11.836-4.6 29.622-10.072 62.371-11.565 35.419-1.616 46.043-1.959 135.73-1.959"}),n.createElement("path",{d:"M335.895 447.859c-61.838 0-111.966-50.128-111.966-111.964 0-61.838 50.128-111.966 111.966-111.966 61.836 0 111.964 50.128 111.964 111.966 0 61.836-50.128 111.964-111.964 111.964zm0-284.451c-95.263 0-172.487 77.224-172.487 172.487 0 95.261 77.224 172.485 172.487 172.485 95.261 0 172.485-77.224 172.485-172.485 0-95.263-77.224-172.487-172.485-172.487m219.608-6.815c0 22.262-18.047 40.307-40.308 40.307-22.26 0-40.307-18.045-40.307-40.307 0-22.261 18.047-40.308 40.307-40.308 22.261 0 40.308 18.047 40.308 40.308"}))):"twitter"===e.type?n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"40",width:"60",viewBox:"-44.7006 -60.54775 387.4052 363.2865"},n.createElement("path",{fill:"#000",d:"M93.719 242.19c112.46 0 173.96-93.168 173.96-173.96 0-2.646-.054-5.28-.173-7.903a124.338 124.338 0 0030.498-31.66c-10.955 4.87-22.744 8.148-35.11 9.626 12.622-7.57 22.313-19.543 26.885-33.817a122.62 122.62 0 01-38.824 14.841C239.798 7.433 223.915 0 206.326 0c-33.764 0-61.144 27.381-61.144 61.132 0 4.798.537 9.465 1.586 13.941-50.815-2.557-95.874-26.886-126.03-63.88a60.977 60.977 0 00-8.279 30.73c0 21.212 10.794 39.938 27.208 50.893a60.685 60.685 0 01-27.69-7.647c-.009.257-.009.507-.009.781 0 29.61 21.075 54.332 49.051 59.934a61.218 61.218 0 01-16.122 2.152 60.84 60.84 0 01-11.491-1.103c7.784 24.293 30.355 41.971 57.115 42.465-20.926 16.402-47.287 26.171-75.937 26.171-4.929 0-9.798-.28-14.584-.846 27.059 17.344 59.189 27.464 93.722 27.464"})):"youtube"===e.type?n.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"40",width:"60",viewBox:"-18 -8 60 40"},n.createElement("path",{fill:"#000",d:"M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"})):e.type)))})):""),n.createElement("div",{className:"topics"},d.topics?d.topics.map((function(e){return n.createElement("span",null,e.title)})):""))),N?n.createElement("div",{className:"r-content-files"},N.map((function(e){return n.createElement("div",{className:"r-content-file"},n.createElement("a",{href:e.targetUrl,className:"r-content-file-link",rel:"nofollow"},n.createElement("span",{className:"r-content-file-title"},e.title),n.createElement("span",{className:"r-content-file-icon"},n.createElement("svg",{width:"21",height:"21",viewBox:"0 0 24 24",fill:"none",stroke:"#8899a4","stroke-width":"2","stroke-linecap":"square","stroke-linejoin":"arcs"},n.createElement("path",{d:"M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"}))," ")))}))):"",I?n.createElement("div",{className:"r-content-gallery"},n.createElement("div",{className:"spotlight-group flexbin r-content-gallery"},I.map((function(e){return n.createElement("a",{className:"spotlight",href:e.image_extralarge_scale},n.createElement("img",{src:e.image_preview_scale}))})))):""))},j=(r(54570),function(e){var t=e.contactItem,r=t.title&&t.title,a=t.taxonomy_contact_category&&t.taxonomy_contact_category[0],l=t.number?t.number:"",c=t.street?t.street:"",o=t.complement?t.complement:"",i=t.zipcode?t.zipcode:"",u=t.city?t.city:"",s=(t.country&&t.country,t.phones?t.phones:""),m=t.mails?t.mails:"",f=t.topics?t.topics:"",p=t.country&&t.country.title,y="https://www.google.com/maps/dir/?api=1&destination="+t.street+"+"+t.number+"+"+t.complement+"+"+t.zipcode+"+"+t.city+"+"+p;return y=y.replaceAll("+null",""),n.createElement("div",{className:"r-list-item"},n.createElement("div",{className:t.image?"r-item-img":"r-item-img r-item-img-placeholder",style:{backgroundImage:t.image_preview_scale?"url("+t.image_preview_scale+")":""}}),n.createElement("div",{className:"r-item-text"},n.createElement("span",{className:"r-item-title"},r),a?n.createElement("span",{className:"r-item-categorie"},a.title):"",n.createElement("div",{className:"r-item-all"},c?n.createElement("div",{className:"r-item-adresse"},l?n.createElement("span",null,l+" "):"",c?n.createElement("span",null,c+", "):"",o?n.createElement("span",null,o+", "):"",n.createElement("br",null),i?n.createElement("span",null,i+" "):"",u?n.createElement("span",null,u):"",n.createElement("div",{className:"itineraty"},n.createElement("a",{href:y,target:"_blank"},"Itinéraire"))):"",n.createElement("div",{className:"r-item-contact"},n.createElement("div",{className:"phones"},s?s.map((function(e,t){return n.createElement("span",{key:t},e.number)})):""),n.createElement("div",{className:"mails"},m?m.map((function(e,t){return n.createElement("span",{key:t},e.mail_address)})):""),n.createElement("div",{className:"topics"},f?f.map((function(e,t){return n.createElement("span",{key:t},e.title)})):"")))))}),x=r(29924),I=r.n(x),k=function(e){var t=e.contactArray,r=e.onChange,l=e.onHover;e.parentCallback;function c(e){l(e)}return n.createElement(n.Fragment,null,n.createElement("ul",{className:"r-result-list annuaire-result-list"},t.map((function(e,t){return n.createElement("li",{key:t,className:"r-list-item-group",onMouseEnter:function(){return c(e.UID)},onMouseLeave:function(){return c(null)},onClick:function(){return t=e.UID,void r(t);var t}},n.createElement(a.rU,{className:"r-list-item-link",style:{textDecoration:"none"},to:{pathname:I()(e.title).replace(/[^a-zA-Z ]/g,"").replace(/\s/g,"-").toLowerCase(),search:"?u=".concat(e.UID),state:{idItem:e.UID}}}),n.createElement(j,{contactItem:e,key:e.created}))}))))},_=r(38458),A=r(35108),U=r(16683),C=r(22948),P=r(79221),D=r(48818),z=r.n(D),H=r(59834),F=r(67676);function L(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,c,o=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(o.push(n.value),o.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(c=r.return(),Object(c)!==c))return}finally{if(u)throw a}}return o}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return M(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);"Object"===r&&e.constructor&&(r=e.constructor.name);if("Map"===r||"Set"===r)return Array.from(e);if("Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))return M(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function M(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function T(e){var t=e.activeItem,r=e.arrayOfLatLngs,n=(0,_.Sx)();if(t){var a=[];a.push(t.geolocation.latitude),a.push(t.geolocation.longitude),n.setView(a,15)}else{var l=new(z().LatLngBounds)(r);n.fitBounds(l)}return null}var Z=function(e){var t=L((0,n.useState)(null),2),r=t[0],l=t[1],c=L((0,n.useState)(null),2),o=(c[0],c[1]),i=L((0,n.useState)([]),2),u=i[0],s=i[1],m=L((0,n.useState)(null),2),f=m[0],p=m[1];function y(e){return new(z().Icon)({iconUrl:e,iconSize:[29,37]})}(0,n.useEffect)((function(){var t=e.items.filter((function(e){return e.geolocation.latitude&&50.4989185!==e.geolocation.latitude&&4.7184485!==e.geolocation.longitude}));s(t)}),[e]);var v=function(t){return t===e.clickId||t===e.hoverId?999:1};return(0,n.useEffect)((function(){if(null!==e.clickId){var t=u&&u.filter((function(t){return t.UID===e.clickId}));l(t[0])}else l(null)}),[e.clickId]),(0,n.useEffect)((function(){if(e.hoverId){var t=u&&u.filter((function(t){return t.UID===e.hoverId}));o(t[0])}else o(null)}),[e.hoverId]),(0,n.useEffect)((function(){if(u.length>0){var e=[];u.map((function(t,r){var n=t.geolocation.latitude,a=t.geolocation.longitude;e.push([n,a])})),p(e)}}),[u]),n.createElement("div",null,n.createElement(A.h,{style:{height:"calc(100vh - ".concat(e.headerHeight,"px)"),minHeight:"600px"},center:[50.85034,4.35171],zoom:15},n.createElement(U.I,{attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',url:"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"}),null!=f?n.createElement(T,{activeItem:r,arrayOfLatLngs:f&&f}):"",u&&u.map((function(t){return n.createElement(C.J,{key:t.UID,icon:(r=t.UID,r===e.clickId||r===e.hoverId?y(F.Z):y(H.Z)),zIndexOffset:v(t.UID),position:[t.geolocation?t.geolocation.latitude:"",t.geolocation?t.geolocation.longitude:""],eventHandlers:{mouseover:function(e){}}},n.createElement(P.G,{closeButton:!1},n.createElement(a.rU,{className:"r-map-popup",style:{textDecoration:"none"},to:{pathname:I()(t.title.replace(/\s/g,"-").toLowerCase()),search:"?u=".concat(t.UID),state:{idItem:t.UID}}},n.createElement("span",{className:"r-map-popup-title"},t.title),n.createElement("p",{className:"r-map-popup-category"},t.taxonomy_contact_category&&t.taxonomy_contact_category[0].title))));var r}))))},q=r(38401);function B(e){return B="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},B(e)}var R=["u"];function V(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,n)}return r}function $(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?V(Object(r),!0).forEach((function(t){W(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):V(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function W(e,t,r){return(t=function(e){var t=function(e,t){if("object"!==B(e)||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var n=r.call(e,t||"default");if("object"!==B(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===B(t)?t:String(t)}(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function G(e){return function(e){if(Array.isArray(e))return Q(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||K(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function J(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var r=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=r){var n,a,l,c,o=[],i=!0,u=!1;try{if(l=(r=r.call(e)).next,0===t){if(Object(r)!==r)return;i=!1}else for(;!(i=(n=l.call(r)).done)&&(o.push(n.value),o.length!==t);i=!0);}catch(e){u=!0,a=e}finally{try{if(!i&&null!=r.return&&(c=r.return(),Object(c)!==c))return}finally{if(u)throw a}}return o}}(e,t)||K(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function K(e,t){if(e){if("string"==typeof e)return Q(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?Q(e,t):void 0}}function Q(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,n=new Array(t);r<t;r++)n[r]=e[r];return n}function X(e,t){if(null==e)return{};var r,n,a=function(e,t){if(null==e)return{};var r,n,a={},l=Object.keys(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||(a[r]=e[r]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(n=0;n<l.length;n++)r=l[n],t.indexOf(r)>=0||Object.prototype.propertyIsEnumerable.call(e,r)&&(a[r]=e[r])}return a}function Y(e){return n.createElement(a.UT,null,n.createElement(i.zt,{language:e.currentLanguage,translation:q.Z},n.createElement(ee,{queryFilterUrl:e.queryFilterUrl,queryUrl:e.queryUrl,proposeUrl:e.proposeUrl,batchSize:e.batchSize})))}function ee(e){var t=r(31296),c=Object.assign({b_start:0,fullobjects:1},t.parse((0,h.Z)().toString())),u=(c.u,X(c,R)),s=J((0,n.useState)([]),2),m=s[0],f=s[1],p=J((0,n.useState)([]),2),y=p[0],v=p[1],d=J((0,n.useState)(null),2),b=d[0],E=d[1],w=J((0,n.useState)(null),2),S=w[0],O=w[1],j=J((0,n.useState)(u),2),x=j[0],I=j[1],_=J((0,n.useState)(0),2),A=_[0],U=_[1],C=J((0,n.useState)(!1),2),P=C[0],D=C[1],z=(0,o.Z)({method:"get",url:"",baseURL:e.queryUrl,headers:{Accept:"application/json"},params:x,load:P},[]),H=z.response,F=(z.error,z.isLoading),L=z.isMore;(0,n.useEffect)((function(){null!==H&&(f(L?function(e){return[].concat(G(e),G(H.items))}:H.items),v(H.items_total))}),[H]);var M=function(e){E(e)};(0,n.useEffect)((function(){I((function(e){return $($({},e),{},{b_start:A})}))}),[A]);var T,q,B=document.getElementById("portal-header").offsetHeight,V=(0,n.useRef)(),W=J(n.useState({height:0}),2),K=W[0],Q=W[1];(0,n.useEffect)((function(){Q({height:V.current.clientHeight})}),[V.current]),m&&m.length>0?(T=n.createElement(k,{onChange:M,contactArray:m,onHover:function(e){O(e)}}),q=n.createElement(Z,{headerHeight:K.height+B,clickId:b,hoverId:S,items:m})):F||(T=n.createElement("p",null,n.createElement(i.vN,{text:"Aucun contact n'a été trouvé"})));var Y=n.createElement("div",{className:"lds-roller-container"},n.createElement("div",{className:"lds-roller"},n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null),n.createElement("div",null)));return n.createElement(a.UT,null,n.createElement("div",{className:"ref"},n.createElement("div",{className:"r-result-filter-container",ref:V,style:{top:B}},n.createElement("div",{id:"r-result-filter",className:"r-result-filter container annuaire-result-filter"},n.createElement(g,{url:e.queryFilterUrl,activeFilter:x,onChange:function(e){D(!1),U((function(e){return 0})),I(e),window.scrollTo(0,0)}}),e.proposeUrl&&n.createElement("div",{className:"r-add-contact"},n.createElement("a",{target:"_blank",href:e.proposeUrl},n.createElement(i.vN,{text:"Proposer un contact"}))),y>0?n.createElement("p",{className:"r-results-numbers"},n.createElement("span",null,y),y>1?n.createElement(i.vN,{text:"contacts trouvés"}):n.createElement(i.vN,{text:"contact trouvé"})):n.createElement("p",{className:"r-results-numbers"},n.createElement(i.vN,{text:"Aucun résultat"})))),n.createElement(l.rs,null,n.createElement(l.AW,{path:"/:name"},n.createElement("div",{className:"r-wrapper container r-annuaire-wrapper"},n.createElement("div",{className:"r-result r-annuaire-result"},n.createElement(N,{queryUrl:e.queryUrl,onChange:M})),n.createElement("div",{className:"r-map annuaire-map",style:{top:K.height+B,height:"calc(100vh-"+K.height+B}},q))),n.createElement(l.AW,{exact:!0,path:"*"},n.createElement("div",{className:"r-wrapper container r-annuaire-wrapper"},n.createElement("div",{className:"r-result r-annuaire-result"},n.createElement("div",null,T),n.createElement("div",{className:"r-load-more"},y-e.batchSize>A?n.createElement("div",null,n.createElement("span",{className:"no-more-result"},F?Y:""),n.createElement("button",{onClick:function(){U((function(t){return t+e.batchSize})),D(!0)},className:"btn-grad"},F?n.createElement(i.vN,{text:"Chargement..."}):n.createElement(i.vN,{text:"Plus de résultats"}))):n.createElement("span",{className:"no-more-result"},F?Y:""))),n.createElement("div",{className:"r-map annuaire-map",style:{top:K.height+B,height:"calc(100vh-"+K.height+B}},q))))))}}}]);