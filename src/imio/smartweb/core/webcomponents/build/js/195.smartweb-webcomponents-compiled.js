(self.webpackChunkimio_smartweb_core_webcomponents=self.webpackChunkimio_smartweb_core_webcomponents||[]).push([[195],{67676:function(e,t,n){"use strict";n(78709);t.Z=n.p+"assets/pin-react-active.07d154037a15be5525b823fdc626cf29.svg"},59834:function(e,t,n){"use strict";n(78709);t.Z=n.p+"assets/pin-react.fda934b5daf26dd4da2a71a7e7e44431.svg"},91267:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return re}});var r=n(78709),a=n(12707),l=n(51031),c=n(59927),i=n(14844),s=n(93580);function o(e){return o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},o(e)}function u(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},l=Object.keys(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}function m(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function f(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?m(Object(n),!0).forEach((function(t){p(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):m(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function p(e,t,n){return(t=v(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function v(e){var t=function(e,t){if("object"!==o(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==o(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===o(t)?t:String(t)}function d(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,l,c,i=[],s=!0,o=!1;try{if(l=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;s=!1}else for(;!(s=(r=l.call(n)).done)&&(i.push(r.value),i.length!==t);s=!0);}catch(e){o=!0,a=e}finally{try{if(!s&&null!=n.return&&(c=n.return(),Object(c)!==c))return}finally{if(o)throw a}}return i}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return h(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return h(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var g=function(e){var t=(0,l.k6)(),a=n(31296),o=d((0,r.useState)(e.activeFilter),2),m=o[0],h=o[1],g=d((0,r.useState)(null),2),y=g[0],b=g[1],E=d((0,r.useState)(null),2),j=E[0],w=E[1],N=(0,i.Z)({method:"get",url:"",baseURL:e.url,headers:{Accept:"application/json"},params:m}),O=N.response;N.error,N.isLoading,(0,r.useEffect)((function(){if(null!==O){var e=O.topics&&O.topics.map((function(e){return{value:e.token,label:e.title}})),t=O.category&&O.category.map((function(e){return{value:e.token,label:e.title}}));b(e),w(t)}}),[O]);var S=(0,r.useCallback)((function(e){var t=e.target,n=t.name,r=t.value;r.length>2?h((function(e){return f(f({},e),{},p({},n,r))}),[]):h((function(e){var t=f({},e);t[n];return u(t,[n].map(v))}))})),k=(0,r.useCallback)((function(e,t){var n=t.name;e?h((function(t){return f(f({},t),{},p({},n,e.value))}),[]):h((function(e){var t=f({},e);t[n];return u(t,[n].map(v))}))})),x=(0,r.useRef)(!0);(0,r.useEffect)((function(){x.current?x.current=!1:(t.push({pathname:"./",search:a.stringify(m)}),e.onChange(m))}),[m]);var I=y&&y.filter((function(t){return t.value===e.activeFilter.topics})),_=j&&j.filter((function(t){return t.value===e.activeFilter.category})),A={control:function(e){return f(f({},e),{},{backgroundColor:"white",borderRadius:"0",height:"50px"})},placeholder:function(e){return f(f({},e),{},{color:"000",fontWeight:"bold",fontSize:"12px",textTransform:"uppercase",letterSpacing:"1.2px"})},option:function(e,t){t.data,t.isDisabled,t.isFocused,t.isSelected;return f({},e)}};return r.createElement(r.Fragment,null,r.createElement("form",{className:"r-filter",onSubmit:function(t){t.preventDefault(),e.onChange(m)}},r.createElement("div",{className:"r-filter-search"},r.createElement(s.$H,null,(function(e){var t=e.translate;return r.createElement("input",{className:"input-custom-class",name:"SearchableText",type:"text",value:m.SearchableText,onChange:S,placeholder:t({text:"Recherche"})})})),r.createElement("button",{type:"submit"}))),r.createElement("div",{className:"r-filter topics-Filter"},r.createElement(s.$H,null,(function(e){var t=e.translate;return r.createElement(c.ZP,{styles:A,name:"topics",className:"select-custom-class library-topics",isClearable:!0,onChange:k,options:y&&y,placeholder:t({text:"Thématiques"}),value:I&&I[0]})}))),r.createElement("div",{className:"r-filter  facilities-Filter"},r.createElement(s.$H,null,(function(e){var t=e.translate;return r.createElement(c.ZP,{styles:A,name:"category",className:"select-custom-class library-facilities",isClearable:!0,onChange:k,options:j&&j,placeholder:t({text:"Catégories"}),value:_&&_[0]})}))))},y=n(6489),b=n(78279),E=n.n(b),j=n(8047),w=n.n(j),N=n(61584),O=(n(17110),["u"]);function S(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,l,c,i=[],s=!0,o=!1;try{if(l=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;s=!1}else for(;!(s=(r=l.call(n)).done)&&(i.push(r.value),i.length!==t);s=!0);}catch(e){o=!0,a=e}finally{try{if(!s&&null!=n.return&&(c=n.return(),Object(c)!==c))return}finally{if(o)throw a}}return i}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return k(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return k(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function k(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function x(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},l=Object.keys(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var I=function(e){var t=e.queryUrl,a=e.onChange,c=(0,l.k6)(),o=n(31296),u=Object.assign({UID:o.parse((0,y.Z)().toString()).u,fullobjects:1}),m=(u.u,x(u,O)),f=S((0,r.useState)(m),2),p=f[0],v=f[1],d=S((0,r.useState)({}),2),h=d[0],g=d[1],b=S((0,r.useState)(0),2),j=b[0],w=b[1],k=S((0,r.useState)(0),2),I=k[0],_=k[1],A=(0,i.Z)({method:"get",url:"",baseURL:t,headers:{Accept:"application/json"},params:p},[]),z=A.response;A.error,A.isLoading;(0,r.useEffect)((function(){v(m)}),[o.parse((0,y.Z)().toString()).u]),(0,r.useEffect)((function(){null!==z&&g(z.items[0]),window.scrollTo(0,0)}),[z]),(0,r.useEffect)((function(){h.items&&h.items.length>0&&(w(h.items.filter((function(e){return"File"===e["@type"]}))),_(h.items.filter((function(e){return"Image"===e["@type"]}))))}),[h]),E().locale("be");var U=E().utc(h.start).format("DD-MM-YYYY"),H=E().utc(h.end).format("DD-MM-YYYY"),C=E().utc(h.start).format("LT"),D=E().utc(h.end).format("LT"),P="https://www.google.com/maps/dir/?api=1&destination="+h.street+"+"+h.number+"+"+h.complement+"+"+h.zipcode+"+"+h.city;return P=P.replaceAll("+null",""),r.createElement("div",{className:"envent-content r-content"},r.createElement("button",{type:"button",onClick:function(){c.push("./"),a(null)}},r.createElement(s.vN,{text:"Retour"})),r.createElement("article",null,r.createElement("header",null,r.createElement("h2",{className:"r-content-title"},h.title)),r.createElement("figure",null,r.createElement("div",{className:"r-content-img",style:{backgroundImage:h.image_affiche_scale?"url("+h.image_affiche_scale+")":""}})),r.createElement("span",{className:"news-info-title"},r.createElement(s.vN,{text:"Infos pratiques"})),r.createElement("div",{className:"r-content-news-info"},r.createElement("div",{className:"r-content-news-info-container"},r.createElement("div",{className:"r-content-news-info-schedul"},r.createElement("div",{className:"icon-baseline"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",preserveAspectRatio:"xMinYMin",viewBox:"0 0 19.41 19.41"},r.createElement("path",{d:"M16.09,2.74H14.35V.85a.44.44,0,0,0-.43-.44H12.47A.44.44,0,0,0,12,.85V2.74H7.38V.85A.44.44,0,0,0,7,.41H5.5a.44.44,0,0,0-.44.44V2.74H3.32A1.74,1.74,0,0,0,1.58,4.48V17.26A1.74,1.74,0,0,0,3.32,19H16.09a1.74,1.74,0,0,0,1.75-1.74V4.48A1.74,1.74,0,0,0,16.09,2.74Zm-.21,14.52H3.54A.22.22,0,0,1,3.32,17h0V6.22H16.09V17a.21.21,0,0,1-.21.22Z"}))),r.createElement("div",{className:"dpinlb"},r.createElement("div",{className:"r-content-news-info--date"},U===H?r.createElement("div",null,h.whole_day?r.createElement("div",{className:"r-content-date-start"},r.createElement("span",null,"Le "),r.createElement("div",{className:"r-time"},U)):r.createElement("div",{className:"r-content-date-one-day"},r.createElement("div",{className:"r-content-date-start"},r.createElement("span",null,"Le "),r.createElement("div",{className:"r-time"},U)),r.createElement("div",{className:"r-content-date-start-hours"},r.createElement("span",null,"de "),r.createElement("div",{className:"r-time-hours"},C),r.createElement("span",null," à "),r.createElement("div",{className:"r-time-hours"},D)))):r.createElement("div",{className:"r-content-date-du-au"},r.createElement("div",{className:"r-content-date-start"},r.createElement("span",null,"Du "),r.createElement("div",{className:"r-time"},U)),r.createElement("div",{className:"r-content-date-end"},r.createElement("span",null," au "),r.createElement("div",{className:"r-time"},H)))))),r.createElement("div",{className:"r-content-news-info-aera"},h.street?r.createElement("div",{className:"icon-baseline"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},r.createElement("path",{d:"M9,18.34C3.9,10.94,3,10.18,3,7.45a6.75,6.75,0,0,1,13.49,0c0,2.73-.94,3.49-6,10.89a.85.85,0,0,1-1.17.22A.77.77,0,0,1,9,18.34Zm.7-8.07A2.82,2.82,0,1,0,6.89,7.45a2.83,2.83,0,0,0,2.82,2.82Z"}))):"",r.createElement("div",{className:"dpinlb"},r.createElement("div",{className:"r-content-news-info--itinirary"},h.street?r.createElement("a",{href:P,target:"_blank"},r.createElement("span",null,"Itinéraire")):""),!0===h.reduced_mobility_facilities?r.createElement("div",{className:"r-content-news-info--reduced"},r.createElement("span",null,r.createElement(s.vN,{text:"Accessible aux PMR"}))):"")),r.createElement("div",{className:"r-content-news-info-contact"},r.createElement("div",{className:"icon-baseline"}),r.createElement("div",{className:"dpinlb"},r.createElement("div",{className:"r-content-news-info--name"},r.createElement("span",null,h.contact_name)),r.createElement("div",{className:"r-content-news-info--phone"},r.createElement("span",null,r.createElement("a",{href:"tel:".concat(h.contact_phone)},h.contact_phone))),r.createElement("div",{className:"r-content-news-info--email"},r.createElement("a",{href:"tel:".concat(h.contact_email)},h.contact_email)))),null===h.event_url&&null===h.online_participation&&null===h.video_url?"":r.createElement("div",{className:"r-content-news-info-link"},r.createElement("div",{className:"icon-baseline"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},r.createElement("path",{d:"M16.36,2.22H3.06a1.3,1.3,0,0,0-1.3,1.3h0v9a1.3,1.3,0,0,0,1.3,1.3H7.52v1.74h-.7a.8.8,0,0,0,0,1.6h5.79a.8.8,0,0,0,0-1.6h-.7V13.85h4.45a1.31,1.31,0,0,0,1.3-1.3v-9A1.3,1.3,0,0,0,16.36,2.22Zm-1.9,10.83a.37.37,0,1,1,.36-.37h0a.36.36,0,0,1-.36.36Zm1.6.08a.45.45,0,1,1,.44-.45h0a.44.44,0,0,1-.44.45h0Zm.53-1.35H2.82V3.52a.23.23,0,0,1,.23-.23H16.36a.23.23,0,0,1,.23.23h0v8.27Z"}))),r.createElement("div",{className:"dpinlb"},null===h.event_url?"":r.createElement("div",{className:"r-content-news-info-event_link"},r.createElement("a",{href:h.event_url},r.createElement(s.vN,{text:"Lien de l'événement"}))),null===h.online_participation?"":r.createElement("div",{className:"r-content-news-info--online_participation"},r.createElement("a",{href:h.online_participation},r.createElement(s.vN,{text:"Participation en ligne"}))),null===h.video_url?"":r.createElement("div",{className:"r-content-news-info--video"},r.createElement("a",{href:h.video_url},r.createElement(s.vN,{text:"Lien vers la vidéo"}))))),null===h.facebook&&null===h.instagram&&null===h.twitter?"":r.createElement("div",{className:"r-content-news-info-social"},r.createElement("ul",null,h.facebook?r.createElement("li",null,r.createElement("a",{href:h.facebook,target:"_blank"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-204.79995 -341.33325 1774.9329 2047.9995"},r.createElement("path",{d:"M1365.333 682.667C1365.333 305.64 1059.693 0 682.667 0 305.64 0 0 305.64 0 682.667c0 340.738 249.641 623.16 576 674.373V880H402.667V682.667H576v-150.4c0-171.094 101.917-265.6 257.853-265.6 74.69 0 152.814 13.333 152.814 13.333v168h-86.083c-84.804 0-111.25 52.623-111.25 106.61v128.057h189.333L948.4 880H789.333v477.04c326.359-51.213 576-333.635 576-674.373",fill:"#100f0d"}),r.createElement("path",{d:"M948.4 880l30.267-197.333H789.333V554.609C789.333 500.623 815.78 448 900.584 448h86.083V280s-78.124-13.333-152.814-13.333c-155.936 0-257.853 94.506-257.853 265.6v150.4H402.667V880H576v477.04a687.805 687.805 0 00106.667 8.293c36.288 0 71.91-2.84 106.666-8.293V880H948.4",fill:"#fff"})))):"",h.instagram?r.createElement("li",null,r.createElement("a",{href:h.instagram,target:"_blank"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-100.7682 -167.947 873.3244 1007.682"},r.createElement("g",{fill:"#100f0d"},r.createElement("path",{d:"M335.895 0c-91.224 0-102.663.387-138.49 2.021-35.752 1.631-60.169 7.31-81.535 15.612-22.088 8.584-40.82 20.07-59.493 38.743-18.674 18.673-30.16 37.407-38.743 59.495C9.33 137.236 3.653 161.653 2.02 197.405.386 233.232 0 244.671 0 335.895c0 91.222.386 102.661 2.02 138.488 1.633 35.752 7.31 60.169 15.614 81.534 8.584 22.088 20.07 40.82 38.743 59.495 18.674 18.673 37.405 30.159 59.493 38.743 21.366 8.302 45.783 13.98 81.535 15.612 35.827 1.634 47.266 2.021 138.49 2.021 91.222 0 102.661-.387 138.488-2.021 35.752-1.631 60.169-7.31 81.534-15.612 22.088-8.584 40.82-20.07 59.495-38.743 18.673-18.675 30.159-37.407 38.743-59.495 8.302-21.365 13.981-45.782 15.612-81.534 1.634-35.827 2.021-47.266 2.021-138.488 0-91.224-.387-102.663-2.021-138.49-1.631-35.752-7.31-60.169-15.612-81.534-8.584-22.088-20.07-40.822-38.743-59.495-18.675-18.673-37.407-30.159-59.495-38.743-21.365-8.302-45.782-13.981-81.534-15.612C438.556.387 427.117 0 335.895 0zm0 60.521c89.686 0 100.31.343 135.729 1.959 32.75 1.493 50.535 6.965 62.37 11.565 15.68 6.094 26.869 13.372 38.622 25.126 11.755 11.754 19.033 22.944 25.127 38.622 4.6 11.836 10.072 29.622 11.565 62.371 1.616 35.419 1.959 46.043 1.959 135.73 0 89.687-.343 100.311-1.959 135.73-1.493 32.75-6.965 50.535-11.565 62.37-6.094 15.68-13.372 26.869-25.127 38.622-11.753 11.755-22.943 19.033-38.621 25.127-11.836 4.6-29.622 10.072-62.371 11.565-35.413 1.616-46.036 1.959-135.73 1.959-89.694 0-100.315-.343-135.73-1.96-32.75-1.492-50.535-6.964-62.37-11.564-15.68-6.094-26.869-13.372-38.622-25.127-11.754-11.753-19.033-22.943-25.127-38.621-4.6-11.836-10.071-29.622-11.565-62.371-1.616-35.419-1.959-46.043-1.959-135.73 0-89.687.343-100.311 1.959-135.73 1.494-32.75 6.965-50.535 11.565-62.37 6.094-15.68 13.373-26.869 25.126-38.622 11.754-11.755 22.944-19.033 38.622-25.127 11.836-4.6 29.622-10.072 62.371-11.565 35.419-1.616 46.043-1.959 135.73-1.959"}),r.createElement("path",{d:"M335.895 447.859c-61.838 0-111.966-50.128-111.966-111.964 0-61.838 50.128-111.966 111.966-111.966 61.836 0 111.964 50.128 111.964 111.966 0 61.836-50.128 111.964-111.964 111.964zm0-284.451c-95.263 0-172.487 77.224-172.487 172.487 0 95.261 77.224 172.485 172.487 172.485 95.261 0 172.485-77.224 172.485-172.485 0-95.263-77.224-172.487-172.485-172.487m219.608-6.815c0 22.262-18.047 40.307-40.308 40.307-22.26 0-40.307-18.045-40.307-40.307 0-22.261 18.047-40.308 40.307-40.308 22.261 0 40.308 18.047 40.308 40.308"}))))):"",h.twitter?r.createElement("li",null,r.createElement("a",{href:h.twitter,target:"_blank"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-44.7006 -60.54775 387.4052 363.2865"},r.createElement("path",{fill:"#000",d:"M93.719 242.19c112.46 0 173.96-93.168 173.96-173.96 0-2.646-.054-5.28-.173-7.903a124.338 124.338 0 0030.498-31.66c-10.955 4.87-22.744 8.148-35.11 9.626 12.622-7.57 22.313-19.543 26.885-33.817a122.62 122.62 0 01-38.824 14.841C239.798 7.433 223.915 0 206.326 0c-33.764 0-61.144 27.381-61.144 61.132 0 4.798.537 9.465 1.586 13.941-50.815-2.557-95.874-26.886-126.03-63.88a60.977 60.977 0 00-8.279 30.73c0 21.212 10.794 39.938 27.208 50.893a60.685 60.685 0 01-27.69-7.647c-.009.257-.009.507-.009.781 0 29.61 21.075 54.332 49.051 59.934a61.218 61.218 0 01-16.122 2.152 60.84 60.84 0 01-11.491-1.103c7.784 24.293 30.355 41.971 57.115 42.465-20.926 16.402-47.287 26.171-75.937 26.171-4.929 0-9.798-.28-14.584-.846 27.059 17.344 59.189 27.464 93.722 27.464"})))):""))),r.createElement("div",{className:"r-content-news-info-action"},h.ticket_url?r.createElement("div",{className:"r-content-booking"},r.createElement("a",{href:h.ticket_url},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},r.createElement("circle",{cx:"13.03",cy:"14.61",r:"0.63",fill:"fill:#fff"}),r.createElement("circle",{cx:"11.59",cy:"6.52",r:"0.63",fill:"fill:#fff"}),r.createElement("path",{d:"M17.11,11.47h.62V7.71h-1.6a1.25,1.25,0,0,1-1.25-1.25,1.27,1.27,0,0,1,.67-1.12l.54-.28-1.6-3.39-12.8,6h0v3.76h.63a1.26,1.26,0,0,1,0,2.51H1.68v3.76H17.73V14h-.62a1.26,1.26,0,1,1,0-2.51Zm-6.9-6.4a.63.63,0,0,0,1.14-.53l2.54-1.2.58,1.23A2.52,2.52,0,0,0,14,7.71H4.63Zm6.27,10.08v1.34H13.66a.63.63,0,1,0-1.26,0H2.93V15.16a2.51,2.51,0,0,0,0-4.86V9H12.4a.63.63,0,0,0,1.26,0h2.82V10.3a2.51,2.51,0,0,0,0,4.86Z",fill:"fill:#fff"}),r.createElement("circle",{cx:"13.03",cy:"10.85",r:"0.63",fill:"fill:#fff"}),r.createElement("circle",{cx:"13.03",cy:"12.73",r:"0.63",fill:"fill:#fff"})),r.createElement(s.vN,{text:"Billetterie"}))):"")),r.createElement("div",{className:"r-content-description"},r.createElement(N.D,null,h.description)),r.createElement("div",{className:"r-content-text",dangerouslySetInnerHTML:{__html:h.text&&h.text.data}}),j?r.createElement("div",{className:"r-content-files"},j.map((function(e){return r.createElement("div",{className:"r-content-file"},r.createElement("a",{href:e.targetUrl,className:"r-content-file-link",rel:"nofollow"},r.createElement("span",{className:"r-content-file-title"},e.title),r.createElement("span",{className:"r-content-file-icon"},r.createElement("svg",{width:"21",height:"21",viewBox:"0 0 24 24",fill:"none",stroke:"#8899a4","stroke-width":"2","stroke-linecap":"square","stroke-linejoin":"arcs"},r.createElement("path",{d:"M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"}))," ")))}))):"",I?r.createElement("div",{className:"r-content-gallery"},r.createElement("div",{className:"spotlight-group flexbin r-content-gallery"},I.map((function(e){return r.createElement("a",{className:"spotlight",href:e.image_extralarge_scale},r.createElement("img",{src:e.image_preview_scale}))})))):""))},_=function(e){var t=e.contactItem,n=t.title&&t.title,a=(t.taxonomy_contact_category&&t.taxonomy_contact_category[0],E()(t.start&&t.start));t.number&&t.number,t.street&&t.street,t.complement&&t.complement,t.zipcode&&t.zipcode,t.city&&t.city,t.country&&t.country,t.phones&&t.phones,t.mails&&t.mails,t.topics&&t.topics;return r.createElement("div",{className:"r-list-item"},r.createElement("div",{className:t.image_preview_scale?"r-item-img":"r-item-img r-item-img-placeholder",style:{backgroundImage:t.image_preview_scale?"url("+t.image_preview_scale+")":""}}),r.createElement("div",{className:"r-item-text"},t.category?r.createElement("span",{className:"r-item-categorie"},t.category.title):"",r.createElement("span",{className:"r-item-title"},n),a?r.createElement("span",{className:"r-item-date"},r.createElement(w(),{format:"DD-MM-YYYY"},a)):""))},A=n(29924),z=n.n(A),U=function(e){var t=e.contactArray,n=e.onChange,l=e.onHover;e.parentCallback;function c(e){l(e)}return r.createElement(r.Fragment,null,r.createElement("ul",{className:"r-result-list event-result-list"},t.map((function(e,t){return r.createElement("li",{key:t,className:"r-list-item-group",onMouseEnter:function(){return c(e.UID)},onMouseLeave:function(){return c(null)},onClick:function(){return t=e.UID,void n(t);var t}},r.createElement(a.rU,{className:"r-list-item-link",style:{textDecoration:"none"},to:{pathname:z()(e.title).replace(/[^a-zA-Z ]/g,"").replace(/\s/g,"-").toLowerCase(),search:"?u=".concat(e.UID),state:{idItem:e.UID}}}),r.createElement(_,{contactItem:e,key:e.created}))}))))},H=n(38458),C=n(35108),D=n(16683),P=n(22948),M=n(79221),L=n(48818),Z=n.n(L),V=n(59834),T=n(67676);function q(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,l,c,i=[],s=!0,o=!1;try{if(l=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;s=!1}else for(;!(s=(r=l.call(n)).done)&&(i.push(r.value),i.length!==t);s=!0);}catch(e){o=!0,a=e}finally{try{if(!s&&null!=n.return&&(c=n.return(),Object(c)!==c))return}finally{if(o)throw a}}return i}}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return F(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return F(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function F(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function B(e){var t=e.activeItem,n=e.arrayOfLatLngs,r=(0,H.Sx)();if(t){var a=[];a.push(t.geolocation.latitude),a.push(t.geolocation.longitude),r.setView(a,15)}else{var l=new(Z().LatLngBounds)(n);r.fitBounds(l)}return null}var Y=function(e){var t=q((0,r.useState)(null),2),n=t[0],l=t[1],c=q((0,r.useState)(null),2),i=(c[0],c[1]),s=q((0,r.useState)([]),2),o=s[0],u=s[1],m=q((0,r.useState)(null),2),f=m[0],p=m[1];function v(e){return new(Z().Icon)({iconUrl:e,iconSize:[29,37]})}(0,r.useEffect)((function(){var t=e.items.filter((function(e){return e.geolocation.latitude&&50.4989185!==e.geolocation.latitude&&4.7184485!==e.geolocation.longitude}));u(t)}),[e]);var d=function(t){return t===e.clickId||t===e.hoverId?999:1};return(0,r.useEffect)((function(){if(null!==e.clickId){var t=o&&o.filter((function(t){return t.UID===e.clickId}));l(t[0])}else l(null)}),[e.clickId]),(0,r.useEffect)((function(){if(e.hoverId){var t=o&&o.filter((function(t){return t.UID===e.hoverId}));i(t[0])}else i(null)}),[e.hoverId]),(0,r.useEffect)((function(){if(o.length>0){var e=[];o.map((function(t,n){var r=t.geolocation.latitude,a=t.geolocation.longitude;e.push([r,a])})),p(e)}}),[o]),r.createElement("div",null,r.createElement(C.h,{style:{height:"calc(100vh - ".concat(e.headerHeight,"px)"),minHeight:"600px"},center:[50.85034,4.35171],zoom:15},r.createElement(D.I,{attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',url:"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"}),null!=f?r.createElement(B,{activeItem:n,arrayOfLatLngs:f&&f}):"",o&&o.map((function(t){return r.createElement(P.J,{key:t.UID,icon:(n=t.UID,n===e.clickId||n===e.hoverId?v(T.Z):v(V.Z)),zIndexOffset:d(t.UID),position:[t.geolocation?t.geolocation.latitude:"",t.geolocation?t.geolocation.longitude:""],eventHandlers:{mouseover:function(e){}}},r.createElement(M.G,{closeButton:!1},r.createElement(a.rU,{className:"r-map-popup",style:{textDecoration:"none"},to:{pathname:z()(t.title.replace(/\s/g,"-").toLowerCase()),search:"?u=".concat(t.UID),state:{idItem:t.UID}}},r.createElement("span",{className:"r-map-popup-title"},t.title),r.createElement("p",{className:"r-map-popup-category"},t.category&&t.category.title))));var n}))))},R=n(38401);function $(e){return $="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},$(e)}var W=["u"];function G(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function J(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?G(Object(n),!0).forEach((function(t){K(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):G(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function K(e,t,n){return(t=function(e){var t=function(e,t){if("object"!==$(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==$(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===$(t)?t:String(t)}(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function Q(e){return function(e){if(Array.isArray(e))return te(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||ee(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function X(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,l,c,i=[],s=!0,o=!1;try{if(l=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;s=!1}else for(;!(s=(r=l.call(n)).done)&&(i.push(r.value),i.length!==t);s=!0);}catch(e){o=!0,a=e}finally{try{if(!s&&null!=n.return&&(c=n.return(),Object(c)!==c))return}finally{if(o)throw a}}return i}}(e,t)||ee(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function ee(e,t){if(e){if("string"==typeof e)return te(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?te(e,t):void 0}}function te(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function ne(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},l=Object.keys(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}function re(e){return r.createElement(a.UT,null,r.createElement(s.zt,{language:e.currentLanguage,translation:R.Z},r.createElement(ae,{queryFilterUrl:e.queryFilterUrl,queryUrl:e.queryUrl,proposeUrl:e.proposeUrl,batchSize:e.batchSize})))}function ae(e){var t=n(31296),c=Object.assign({b_start:0,fullobjects:1},t.parse((0,y.Z)().toString())),o=(c.u,ne(c,W)),u=X((0,r.useState)([]),2),m=u[0],f=u[1],p=X((0,r.useState)([]),2),v=p[0],d=p[1],h=X((0,r.useState)(null),2),b=h[0],E=h[1],j=X((0,r.useState)(null),2),w=j[0],N=j[1],O=X((0,r.useState)(o),2),S=O[0],k=O[1],x=X((0,r.useState)(0),2),_=x[0],A=x[1],z=X((0,r.useState)(!1),2),H=z[0],C=z[1],D=(0,i.Z)({method:"get",url:"",baseURL:e.queryUrl,headers:{Accept:"application/json"},params:S,load:H},[]),P=D.response,M=(D.error,D.isLoading),L=D.isMore;(0,r.useEffect)((function(){null!==P&&(f(L?function(e){return[].concat(Q(e),Q(P.items))}:P.items),d(P.items_total))}),[P]);var Z=function(e){E(e)};(0,r.useEffect)((function(){k((function(e){return J(J({},e),{},{b_start:_})}))}),[_]);var V,T,q=document.getElementById("portal-header").offsetHeight,F=(0,r.useRef)(),B=X(r.useState({height:0}),2),R=B[0],$=B[1];(0,r.useEffect)((function(){$({height:F.current.clientHeight})}),[F.current]),m&&m.length>0?(V=r.createElement(U,{onChange:Z,contactArray:m,onHover:function(e){N(e)}}),T=r.createElement(Y,{headerHeight:R.height+q,clickId:b,hoverId:w,items:m})):M||(V=r.createElement("p",null,r.createElement(s.vN,{text:"Aucun événement n'a été trouvé"})));var G=r.createElement("div",{className:"lds-roller-container"},r.createElement("div",{className:"lds-roller"},r.createElement("div",null),r.createElement("div",null),r.createElement("div",null),r.createElement("div",null),r.createElement("div",null),r.createElement("div",null),r.createElement("div",null),r.createElement("div",null)));return r.createElement(a.UT,null,r.createElement("div",{className:"ref"},r.createElement("div",{className:"r-result-filter-container",ref:F,style:{top:q}},r.createElement("div",{id:"r-result-filter",className:"r-result-filter container annuaire-result-filter"},r.createElement(g,{url:e.queryFilterUrl,activeFilter:S,onChange:function(e){C(!1),A((function(e){return 0})),k(e),window.scrollTo(0,0)}}),e.proposeUrl&&r.createElement("div",{className:"r-add-event"},r.createElement("a",{target:"_blank",href:e.proposeUrl},r.createElement(s.vN,{text:"Proposer un événement"}))),v>0?r.createElement("p",{className:"r-results-numbers"},r.createElement("span",null,v),v>1?r.createElement(s.vN,{text:"événements trouvés"}):r.createElement(s.vN,{text:"événement trouvé"})):r.createElement("p",{className:"r-results-numbers"},r.createElement(s.vN,{text:"Aucun résultat"})))),r.createElement(l.rs,null,r.createElement(l.AW,{path:"/:name"},r.createElement("div",{className:"r-wrapper container r-annuaire-wrapper"},r.createElement("div",{className:"r-result r-annuaire-result"},r.createElement(I,{queryUrl:e.queryUrl,onChange:Z})),r.createElement("div",{className:"r-map annuaire-map",style:{top:R.height+q,height:"calc(100vh-"+R.height+q}},T))),r.createElement(l.AW,{exact:!0,path:"*"},r.createElement("div",{className:"r-wrapper container r-annuaire-wrapper"},r.createElement("div",{className:"r-result r-annuaire-result"},r.createElement("div",null,V),r.createElement("div",{className:"r-load-more"},v-e.batchSize>_?r.createElement("div",null,r.createElement("span",{className:"no-more-result"},M?G:""),r.createElement("button",{onClick:function(){A((function(t){return t+e.batchSize})),C(!0)},className:"btn-grad"},M?r.createElement(s.vN,{text:"Chargement..."}):r.createElement(s.vN,{text:"Plus de résultats"}))):r.createElement("span",{className:"no-more-result"},M?G:""))),r.createElement("div",{className:"r-map annuaire-map",style:{top:R.height+q,height:"calc(100vh-"+R.height+q}},T))))))}},46700:function(e,t,n){var r={"./af":68435,"./af.js":68435,"./ar":99673,"./ar-dz":85296,"./ar-dz.js":85296,"./ar-kw":12855,"./ar-kw.js":12855,"./ar-ly":57896,"./ar-ly.js":57896,"./ar-ma":72309,"./ar-ma.js":72309,"./ar-sa":23097,"./ar-sa.js":23097,"./ar-tn":47728,"./ar-tn.js":47728,"./ar.js":99673,"./az":40336,"./az.js":40336,"./be":71140,"./be.js":71140,"./bg":94950,"./bg.js":94950,"./bm":46947,"./bm.js":46947,"./bn":81515,"./bn-bd":54062,"./bn-bd.js":54062,"./bn.js":81515,"./bo":28753,"./bo.js":28753,"./br":53423,"./br.js":53423,"./bs":94516,"./bs.js":94516,"./ca":87672,"./ca.js":87672,"./cs":31139,"./cs.js":31139,"./cv":84713,"./cv.js":84713,"./cy":25820,"./cy.js":25820,"./da":54131,"./da.js":54131,"./de":96647,"./de-at":53422,"./de-at.js":53422,"./de-ch":66246,"./de-ch.js":66246,"./de.js":96647,"./dv":68049,"./dv.js":68049,"./el":35006,"./el.js":35006,"./en-au":18006,"./en-au.js":18006,"./en-ca":59706,"./en-ca.js":59706,"./en-gb":67157,"./en-gb.js":67157,"./en-ie":16906,"./en-ie.js":16906,"./en-il":5089,"./en-il.js":5089,"./en-in":55304,"./en-in.js":55304,"./en-nz":22483,"./en-nz.js":22483,"./en-sg":98469,"./en-sg.js":98469,"./eo":41754,"./eo.js":41754,"./es":91488,"./es-do":98387,"./es-do.js":98387,"./es-mx":32657,"./es-mx.js":32657,"./es-us":99099,"./es-us.js":99099,"./es.js":91488,"./et":5318,"./et.js":5318,"./eu":74175,"./eu.js":74175,"./fa":9383,"./fa.js":9383,"./fi":71382,"./fi.js":71382,"./fil":18959,"./fil.js":18959,"./fo":77535,"./fo.js":77535,"./fr":80219,"./fr-ca":5886,"./fr-ca.js":5886,"./fr-ch":71967,"./fr-ch.js":71967,"./fr.js":80219,"./fy":76993,"./fy.js":76993,"./ga":18891,"./ga.js":18891,"./gd":29554,"./gd.js":29554,"./gl":11865,"./gl.js":11865,"./gom-deva":29485,"./gom-deva.js":29485,"./gom-latn":8869,"./gom-latn.js":8869,"./gu":54998,"./gu.js":54998,"./he":61248,"./he.js":61248,"./hi":91500,"./hi.js":91500,"./hr":56654,"./hr.js":56654,"./hu":34864,"./hu.js":34864,"./hy-am":36060,"./hy-am.js":36060,"./id":95942,"./id.js":95942,"./is":19921,"./is.js":19921,"./it":36781,"./it-ch":29378,"./it-ch.js":29378,"./it.js":36781,"./ja":72719,"./ja.js":72719,"./jv":86269,"./jv.js":86269,"./ka":70007,"./ka.js":70007,"./kk":91952,"./kk.js":91952,"./km":13540,"./km.js":13540,"./kn":67479,"./kn.js":67479,"./ko":99481,"./ko.js":99481,"./ku":19697,"./ku.js":19697,"./ky":640,"./ky.js":640,"./lb":94242,"./lb.js":94242,"./lo":75889,"./lo.js":75889,"./lt":72138,"./lt.js":72138,"./lv":69541,"./lv.js":69541,"./me":73972,"./me.js":73972,"./mi":18626,"./mi.js":18626,"./mk":14352,"./mk.js":14352,"./ml":6485,"./ml.js":6485,"./mn":6238,"./mn.js":6238,"./mr":61296,"./mr.js":61296,"./ms":47048,"./ms-my":95081,"./ms-my.js":95081,"./ms.js":47048,"./mt":7814,"./mt.js":7814,"./my":34059,"./my.js":34059,"./nb":16824,"./nb.js":16824,"./ne":74997,"./ne.js":74997,"./nl":421,"./nl-be":4341,"./nl-be.js":4341,"./nl.js":421,"./nn":38112,"./nn.js":38112,"./oc-lnc":63356,"./oc-lnc.js":63356,"./pa-in":29583,"./pa-in.js":29583,"./pl":86800,"./pl.js":86800,"./pt":90037,"./pt-br":79912,"./pt-br.js":79912,"./pt.js":90037,"./ro":88235,"./ro.js":88235,"./ru":8561,"./ru.js":8561,"./sd":32414,"./sd.js":32414,"./se":60947,"./se.js":60947,"./si":97081,"./si.js":97081,"./sk":5315,"./sk.js":5315,"./sl":59345,"./sl.js":59345,"./sq":1899,"./sq.js":1899,"./sr":4277,"./sr-cyrl":26466,"./sr-cyrl.js":26466,"./sr.js":4277,"./ss":59250,"./ss.js":59250,"./sv":55272,"./sv.js":55272,"./sw":40214,"./sw.js":40214,"./ta":86121,"./ta.js":86121,"./te":4182,"./te.js":4182,"./tet":14116,"./tet.js":14116,"./tg":63250,"./tg.js":63250,"./th":83111,"./th.js":83111,"./tk":12527,"./tk.js":12527,"./tl-ph":98104,"./tl-ph.js":98104,"./tlh":11751,"./tlh.js":11751,"./tr":67554,"./tr.js":67554,"./tzl":46061,"./tzl.js":46061,"./tzm":49236,"./tzm-latn":18447,"./tzm-latn.js":18447,"./tzm.js":49236,"./ug-cn":77693,"./ug-cn.js":77693,"./uk":35636,"./uk.js":35636,"./ur":10807,"./ur.js":10807,"./uz":28429,"./uz-latn":88105,"./uz-latn.js":88105,"./uz.js":28429,"./vi":59489,"./vi.js":59489,"./x-pseudo":30860,"./x-pseudo.js":30860,"./yo":26520,"./yo.js":26520,"./zh-cn":9599,"./zh-cn.js":9599,"./zh-hk":86433,"./zh-hk.js":86433,"./zh-mo":40381,"./zh-mo.js":40381,"./zh-tw":25759,"./zh-tw.js":25759};function a(e){var t=l(e);return n(t)}function l(e){if(!n.o(r,e)){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}return r[e]}a.keys=function(){return Object.keys(r)},a.resolve=l,e.exports=a,a.id=46700}}]);