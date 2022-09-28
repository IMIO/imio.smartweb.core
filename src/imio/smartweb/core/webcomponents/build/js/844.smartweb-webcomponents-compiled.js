"use strict";(self.webpackChunkimio_smartweb_core_webcomponents=self.webpackChunkimio_smartweb_core_webcomponents||[]).push([[844],{67676:function(e,t,n){n(78709);t.Z=n.p+"assets/pin-react-active.07d154037a15be5525b823fdc626cf29.svg"},59834:function(e,t,n){n(78709);t.Z=n.p+"assets/pin-react.fda934b5daf26dd4da2a71a7e7e44431.svg"},5844:function(e,t,n){n.r(t),n.d(t,{default:function(){return ee}});var r=n(78709),a=n(12707),l=n(55110);var c=n(84106),i=n(14844);function o(e){return o="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},o(e)}function s(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},l=Object.keys(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}function u(e){var t=function(e,t){if("object"!==o(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==o(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===o(t)?t:String(t)}function m(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function f(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?m(Object(n),!0).forEach((function(t){p(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):m(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function p(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function d(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==n)return;var r,a,l=[],c=!0,i=!1;try{for(n=n.call(e);!(c=(r=n.next()).done)&&(l.push(r.value),!t||l.length!==t);c=!0);}catch(e){i=!0,a=e}finally{try{c||null==n.return||n.return()}finally{if(i)throw a}}return l}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return v(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return v(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var h=function(e){var t=(0,l.k6)(),a=n(31296),o=d((0,r.useState)(e.activeFilter),2),m=o[0],v=o[1],h=d((0,r.useState)(null),2),g=h[0],y=h[1],E=d((0,r.useState)(null),2),b=E[0],w=E[1],N=(0,i.Z)({method:"get",url:"",baseURL:e.url,headers:{Accept:"application/json"},params:m}),O=N.response;N.error,N.isLoading,(0,r.useEffect)((function(){if(null!==O){var e=O.topics&&O.topics.map((function(e){return{value:e.token,label:e.title}})),t=O.category&&O.category.map((function(e){return{value:e.token,label:e.title}}));y(e),w(t)}}),[O]);var S=(0,r.useCallback)((function(e){var t=e.target,n=t.name,r=t.value;r.length>2?v((function(e){return f(f({},e),{},p({},n,r))}),[]):v((function(e){var t=f({},e);t[n];return s(t,[n].map(u))}))})),j=(0,r.useCallback)((function(e,t){var n=t.name;e?v((function(t){return f(f({},t),{},p({},n,e.value))}),[]):v((function(e){var t=f({},e);t[n];return s(t,[n].map(u))}))})),I=(0,r.useRef)(!0);(0,r.useEffect)((function(){I.current?I.current=!1:(t.push({pathname:"",search:a.stringify(m)}),e.onChange(m))}),[m]);var x=g&&g.filter((function(t){return t.value===e.activeFilter.topics})),k=b&&b.filter((function(t){return t.value===e.activeFilter.category})),A={control:function(e){return f(f({},e),{},{backgroundColor:"white",borderRadius:"0",height:"50px"})},placeholder:function(e){return f(f({},e),{},{color:"000",fontWeight:"bold",fontSize:"12px",textTransform:"uppercase",letterSpacing:"1.2px"})},option:function(e,t){t.data,t.isDisabled,t.isFocused,t.isSelected;return f({},e)}};return r.createElement(r.Fragment,null,r.createElement("form",{className:"r-filter",onSubmit:function(t){t.preventDefault(),e.onChange(m)}},r.createElement("div",{className:"r-filter-search"},r.createElement("input",{className:"input-custom-class",name:"SearchableText",type:"text",value:m.SearchableText,onChange:S,placeholder:"Recherche"}),r.createElement("button",{type:"submit"}))),r.createElement("div",{className:"r-filter topics-Filter"},r.createElement(c.ZP,{styles:A,name:"topics",className:"select-custom-class library-topics",isClearable:!0,onChange:j,options:g&&g,placeholder:"Thématiques",value:x&&x[0]})),r.createElement("div",{className:"r-filter  facilities-Filter"},r.createElement(c.ZP,{styles:A,name:"category",className:"select-custom-class library-facilities",isClearable:!0,onChange:j,options:b&&b,placeholder:"Catégories",value:k&&k[0]})))},g=n(6489),y=n(78279),E=n.n(y),b=n(8047),w=n.n(b),N=n(78478),O=(n(17110),["u"]);function S(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==n)return;var r,a,l=[],c=!0,i=!1;try{for(n=n.call(e);!(c=(r=n.next()).done)&&(l.push(r.value),!t||l.length!==t);c=!0);}catch(e){i=!0,a=e}finally{try{c||null==n.return||n.return()}finally{if(i)throw a}}return l}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return j(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return j(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function j(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function I(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},l=Object.keys(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var x=function(e){var t=e.queryUrl,a=e.onChange,c=(0,l.k6)(),o=n(31296),s=Object.assign({UID:o.parse((0,g.Z)().toString()).u,fullobjects:1}),u=(s.u,I(s,O)),m=S((0,r.useState)(u),2),f=m[0],p=m[1],d=S((0,r.useState)({}),2),v=d[0],h=d[1],y=S((0,r.useState)(0),2),b=y[0],w=y[1],j=S((0,r.useState)(0),2),x=j[0],k=j[1],A=(0,i.Z)({method:"get",url:"",baseURL:t,headers:{Accept:"application/json"},params:f},[]),_=A.response;A.error,A.isLoading;(0,r.useEffect)((function(){p(u)}),[o.parse((0,g.Z)().toString()).u]),(0,r.useEffect)((function(){null!==_&&h(_.items[0]),window.scrollTo(0,0)}),[_]),(0,r.useEffect)((function(){v.items&&v.items.length>0&&(w(v.items.filter((function(e){return"File"===e["@type"]}))),k(v.items.filter((function(e){return"Image"===e["@type"]}))))}),[v]),E().locale("be");var U=E().utc(v.start).format("DD-MM-YYYY"),C=E().utc(v.end).format("DD-MM-YYYY"),H=E().utc(v.start).format("LT"),D=E().utc(v.end).format("LT"),P="https://www.google.com/maps/dir/?api=1&destination="+v.street+"+"+v.number+"+"+v.complement+"+"+v.zipcode+"+"+v.city;return P=P.replaceAll("+null",""),r.createElement("div",{className:"envent-content r-content"},r.createElement("button",{type:"button",onClick:function(){c.push("./"),a(null)}},"Retour"),r.createElement("article",null,r.createElement("header",null,r.createElement("h2",{className:"r-content-title"},v.title)),r.createElement("figure",null,r.createElement("div",{className:"r-content-img",style:{backgroundImage:v["@id"]?"url("+v["@id"]+"/@@images/image/affiche)":""}})),r.createElement("span",{className:"news-info-title"},"Infos pratiques"),r.createElement("div",{className:"r-content-news-info"},r.createElement("div",{className:"r-content-news-info-container"},r.createElement("div",{className:"r-content-news-info-schedul"},r.createElement("div",{className:"icon-baseline"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",preserveAspectRatio:"xMinYMin",viewBox:"0 0 19.41 19.41"},r.createElement("path",{d:"M16.09,2.74H14.35V.85a.44.44,0,0,0-.43-.44H12.47A.44.44,0,0,0,12,.85V2.74H7.38V.85A.44.44,0,0,0,7,.41H5.5a.44.44,0,0,0-.44.44V2.74H3.32A1.74,1.74,0,0,0,1.58,4.48V17.26A1.74,1.74,0,0,0,3.32,19H16.09a1.74,1.74,0,0,0,1.75-1.74V4.48A1.74,1.74,0,0,0,16.09,2.74Zm-.21,14.52H3.54A.22.22,0,0,1,3.32,17h0V6.22H16.09V17a.21.21,0,0,1-.21.22Z"}))),r.createElement("div",{className:"dpinlb"},r.createElement("div",{className:"r-content-news-info--date"},U===C?r.createElement("div",null,v.whole_day?r.createElement("div",{className:"r-content-date-start"},r.createElement("span",null,"Le "),r.createElement("div",{className:"r-time"},U)):r.createElement("div",{className:"r-content-date-one-day"},r.createElement("div",{className:"r-content-date-start"},r.createElement("span",null,"Le "),r.createElement("div",{className:"r-time"},U)),r.createElement("div",{className:"r-content-date-start-hours"},r.createElement("span",null,"de "),r.createElement("div",{className:"r-time-hours"},H),r.createElement("span",null," à "),r.createElement("div",{className:"r-time-hours"},D)))):r.createElement("div",{className:"r-content-date-du-au"},r.createElement("div",{className:"r-content-date-start"},r.createElement("span",null,"Du "),r.createElement("div",{className:"r-time"},U)),r.createElement("div",{className:"r-content-date-end"},r.createElement("span",null," au "),r.createElement("div",{className:"r-time"},C)))))),r.createElement("div",{className:"r-content-news-info-aera"},v.street?r.createElement("div",{className:"icon-baseline"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},r.createElement("path",{d:"M9,18.34C3.9,10.94,3,10.18,3,7.45a6.75,6.75,0,0,1,13.49,0c0,2.73-.94,3.49-6,10.89a.85.85,0,0,1-1.17.22A.77.77,0,0,1,9,18.34Zm.7-8.07A2.82,2.82,0,1,0,6.89,7.45a2.83,2.83,0,0,0,2.82,2.82Z"}))):"",r.createElement("div",{className:"dpinlb"},r.createElement("div",{className:"r-content-news-info--itinirary"},v.street?r.createElement("a",{href:P,target:"_blank"},r.createElement("span",null,"Itinéraire")):""),!0===v.reduced_mobility_facilities?r.createElement("div",{className:"r-content-news-info--reduced"},r.createElement("span",null,"Accessible aux PMR")):"")),r.createElement("div",{className:"r-content-news-info-contact"},r.createElement("div",{className:"icon-baseline"}),r.createElement("div",{className:"dpinlb"},r.createElement("div",{className:"r-content-news-info--name"},r.createElement("span",null,v.contact_name)),r.createElement("div",{className:"r-content-news-info--phone"},r.createElement("span",null,r.createElement("a",{href:"tel:".concat(v.contact_phone)},v.contact_phone))),r.createElement("div",{className:"r-content-news-info--email"},r.createElement("a",{href:"tel:".concat(v.contact_email)},v.contact_email)))),null===v.event_url&&null===v.online_participation&&null===v.video_url?"":r.createElement("div",{className:"r-content-news-info-link"},r.createElement("div",{className:"icon-baseline"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},r.createElement("path",{d:"M16.36,2.22H3.06a1.3,1.3,0,0,0-1.3,1.3h0v9a1.3,1.3,0,0,0,1.3,1.3H7.52v1.74h-.7a.8.8,0,0,0,0,1.6h5.79a.8.8,0,0,0,0-1.6h-.7V13.85h4.45a1.31,1.31,0,0,0,1.3-1.3v-9A1.3,1.3,0,0,0,16.36,2.22Zm-1.9,10.83a.37.37,0,1,1,.36-.37h0a.36.36,0,0,1-.36.36Zm1.6.08a.45.45,0,1,1,.44-.45h0a.44.44,0,0,1-.44.45h0Zm.53-1.35H2.82V3.52a.23.23,0,0,1,.23-.23H16.36a.23.23,0,0,1,.23.23h0v8.27Z"}))),r.createElement("div",{className:"dpinlb"},null===v.event_url?"":r.createElement("div",{className:"r-content-news-info-event_link"},r.createElement("a",{href:v.event_url},"Lien de l'événement")),null===v.online_participation?"":r.createElement("div",{className:"r-content-news-info--online_participation"},r.createElement("a",{href:v.online_participation},"Participation en ligne")),null===v.video_url?"":r.createElement("div",{className:"r-content-news-info--video"},r.createElement("a",{href:v.video_url},"Lien vers la vidéo")))),null===v.facebook&&null===v.instagram&&null===v.twitter?"":r.createElement("div",{className:"r-content-news-info-social"},r.createElement("ul",null,v.facebook?r.createElement("li",null,r.createElement("a",{href:v.facebook,target:"_blank"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-204.79995 -341.33325 1774.9329 2047.9995"},r.createElement("path",{d:"M1365.333 682.667C1365.333 305.64 1059.693 0 682.667 0 305.64 0 0 305.64 0 682.667c0 340.738 249.641 623.16 576 674.373V880H402.667V682.667H576v-150.4c0-171.094 101.917-265.6 257.853-265.6 74.69 0 152.814 13.333 152.814 13.333v168h-86.083c-84.804 0-111.25 52.623-111.25 106.61v128.057h189.333L948.4 880H789.333v477.04c326.359-51.213 576-333.635 576-674.373",fill:"#100f0d"}),r.createElement("path",{d:"M948.4 880l30.267-197.333H789.333V554.609C789.333 500.623 815.78 448 900.584 448h86.083V280s-78.124-13.333-152.814-13.333c-155.936 0-257.853 94.506-257.853 265.6v150.4H402.667V880H576v477.04a687.805 687.805 0 00106.667 8.293c36.288 0 71.91-2.84 106.666-8.293V880H948.4",fill:"#fff"})))):"",v.instagram?r.createElement("li",null,r.createElement("a",{href:v.instagram,target:"_blank"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-100.7682 -167.947 873.3244 1007.682"},r.createElement("g",{fill:"#100f0d"},r.createElement("path",{d:"M335.895 0c-91.224 0-102.663.387-138.49 2.021-35.752 1.631-60.169 7.31-81.535 15.612-22.088 8.584-40.82 20.07-59.493 38.743-18.674 18.673-30.16 37.407-38.743 59.495C9.33 137.236 3.653 161.653 2.02 197.405.386 233.232 0 244.671 0 335.895c0 91.222.386 102.661 2.02 138.488 1.633 35.752 7.31 60.169 15.614 81.534 8.584 22.088 20.07 40.82 38.743 59.495 18.674 18.673 37.405 30.159 59.493 38.743 21.366 8.302 45.783 13.98 81.535 15.612 35.827 1.634 47.266 2.021 138.49 2.021 91.222 0 102.661-.387 138.488-2.021 35.752-1.631 60.169-7.31 81.534-15.612 22.088-8.584 40.82-20.07 59.495-38.743 18.673-18.675 30.159-37.407 38.743-59.495 8.302-21.365 13.981-45.782 15.612-81.534 1.634-35.827 2.021-47.266 2.021-138.488 0-91.224-.387-102.663-2.021-138.49-1.631-35.752-7.31-60.169-15.612-81.534-8.584-22.088-20.07-40.822-38.743-59.495-18.675-18.673-37.407-30.159-59.495-38.743-21.365-8.302-45.782-13.981-81.534-15.612C438.556.387 427.117 0 335.895 0zm0 60.521c89.686 0 100.31.343 135.729 1.959 32.75 1.493 50.535 6.965 62.37 11.565 15.68 6.094 26.869 13.372 38.622 25.126 11.755 11.754 19.033 22.944 25.127 38.622 4.6 11.836 10.072 29.622 11.565 62.371 1.616 35.419 1.959 46.043 1.959 135.73 0 89.687-.343 100.311-1.959 135.73-1.493 32.75-6.965 50.535-11.565 62.37-6.094 15.68-13.372 26.869-25.127 38.622-11.753 11.755-22.943 19.033-38.621 25.127-11.836 4.6-29.622 10.072-62.371 11.565-35.413 1.616-46.036 1.959-135.73 1.959-89.694 0-100.315-.343-135.73-1.96-32.75-1.492-50.535-6.964-62.37-11.564-15.68-6.094-26.869-13.372-38.622-25.127-11.754-11.753-19.033-22.943-25.127-38.621-4.6-11.836-10.071-29.622-11.565-62.371-1.616-35.419-1.959-46.043-1.959-135.73 0-89.687.343-100.311 1.959-135.73 1.494-32.75 6.965-50.535 11.565-62.37 6.094-15.68 13.373-26.869 25.126-38.622 11.754-11.755 22.944-19.033 38.622-25.127 11.836-4.6 29.622-10.072 62.371-11.565 35.419-1.616 46.043-1.959 135.73-1.959"}),r.createElement("path",{d:"M335.895 447.859c-61.838 0-111.966-50.128-111.966-111.964 0-61.838 50.128-111.966 111.966-111.966 61.836 0 111.964 50.128 111.964 111.966 0 61.836-50.128 111.964-111.964 111.964zm0-284.451c-95.263 0-172.487 77.224-172.487 172.487 0 95.261 77.224 172.485 172.487 172.485 95.261 0 172.485-77.224 172.485-172.485 0-95.263-77.224-172.487-172.485-172.487m219.608-6.815c0 22.262-18.047 40.307-40.308 40.307-22.26 0-40.307-18.045-40.307-40.307 0-22.261 18.047-40.308 40.307-40.308 22.261 0 40.308 18.047 40.308 40.308"}))))):"",v.twitter?r.createElement("li",null,r.createElement("a",{href:v.twitter,target:"_blank"},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-44.7006 -60.54775 387.4052 363.2865"},r.createElement("path",{fill:"#000",d:"M93.719 242.19c112.46 0 173.96-93.168 173.96-173.96 0-2.646-.054-5.28-.173-7.903a124.338 124.338 0 0030.498-31.66c-10.955 4.87-22.744 8.148-35.11 9.626 12.622-7.57 22.313-19.543 26.885-33.817a122.62 122.62 0 01-38.824 14.841C239.798 7.433 223.915 0 206.326 0c-33.764 0-61.144 27.381-61.144 61.132 0 4.798.537 9.465 1.586 13.941-50.815-2.557-95.874-26.886-126.03-63.88a60.977 60.977 0 00-8.279 30.73c0 21.212 10.794 39.938 27.208 50.893a60.685 60.685 0 01-27.69-7.647c-.009.257-.009.507-.009.781 0 29.61 21.075 54.332 49.051 59.934a61.218 61.218 0 01-16.122 2.152 60.84 60.84 0 01-11.491-1.103c7.784 24.293 30.355 41.971 57.115 42.465-20.926 16.402-47.287 26.171-75.937 26.171-4.929 0-9.798-.28-14.584-.846 27.059 17.344 59.189 27.464 93.722 27.464"})))):""))),r.createElement("div",{className:"r-content-news-info-action"},v.ticket_url?r.createElement("div",{className:"r-content-booking"},r.createElement("a",{href:v.ticket_url},r.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},r.createElement("circle",{cx:"13.03",cy:"14.61",r:"0.63",fill:"fill:#fff"}),r.createElement("circle",{cx:"11.59",cy:"6.52",r:"0.63",fill:"fill:#fff"}),r.createElement("path",{d:"M17.11,11.47h.62V7.71h-1.6a1.25,1.25,0,0,1-1.25-1.25,1.27,1.27,0,0,1,.67-1.12l.54-.28-1.6-3.39-12.8,6h0v3.76h.63a1.26,1.26,0,0,1,0,2.51H1.68v3.76H17.73V14h-.62a1.26,1.26,0,1,1,0-2.51Zm-6.9-6.4a.63.63,0,0,0,1.14-.53l2.54-1.2.58,1.23A2.52,2.52,0,0,0,14,7.71H4.63Zm6.27,10.08v1.34H13.66a.63.63,0,1,0-1.26,0H2.93V15.16a2.51,2.51,0,0,0,0-4.86V9H12.4a.63.63,0,0,0,1.26,0h2.82V10.3a2.51,2.51,0,0,0,0,4.86Z",fill:"fill:#fff"}),r.createElement("circle",{cx:"13.03",cy:"10.85",r:"0.63",fill:"fill:#fff"}),r.createElement("circle",{cx:"13.03",cy:"12.73",r:"0.63",fill:"fill:#fff"})),"Billetterie")):"")),r.createElement("div",{className:"r-content-description"},r.createElement(N.D,null,v.description)),r.createElement("div",{className:"r-content-text",dangerouslySetInnerHTML:{__html:v.text&&v.text.data}}),b?r.createElement("div",{className:"r-content-files"},r.createElement("h2",{className:"r-content-files-title"},"Téléchargements"),b.map((function(e){return r.createElement("div",{className:"r-content-file"},r.createElement("a",{href:e.targetUrl,className:"r-content-file-link",rel:"nofollow"},r.createElement("span",{className:"r-content-file-title"},e.title),r.createElement("span",{className:"r-content-file-icon"},r.createElement("svg",{width:"21",height:"21",viewBox:"0 0 24 24",fill:"none",stroke:"#8899a4","stroke-width":"2","stroke-linecap":"square","stroke-linejoin":"arcs"},r.createElement("path",{d:"M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"}))," ")))}))):"",x?r.createElement("div",{className:"r-content-gallery"},r.createElement("div",{className:"spotlight-group flexbin r-content-gallery"},x.map((function(e){return r.createElement("a",{className:"spotlight",href:e.image.scales.extralarge.download,"data-description":"Lorem ipsum dolor sit amet, consetetur sadipscing."},r.createElement("img",{src:e.image.scales.preview.download,alt:"Lorem ipsum dolor sit amet"}))})))):""))},k=(n(54570),function(e){var t=e.contactItem,n=t.title&&t.title,a=(t.taxonomy_contact_category&&t.taxonomy_contact_category[0],E()(t.start&&t.start));t.number&&t.number,t.street&&t.street,t.complement&&t.complement,t.zipcode&&t.zipcode,t.city&&t.city,t.country&&t.country,t.phones&&t.phones,t.mails&&t.mails,t.topics&&t.topics;return r.createElement("div",{className:"r-list-item"},r.createElement("div",{className:t.image?"r-item-img":"r-item-img r-item-img-placeholder",style:{backgroundImage:t.image?"url("+t.image.scales.preview.download+")":""}}),r.createElement("div",{className:"r-item-text"},t.category?r.createElement("span",{className:"r-item-categorie"},t.category.title):"",r.createElement("span",{className:"r-item-title"},n),a?r.createElement("span",{className:"r-item-date"},r.createElement(w(),{format:"DD-MM-YYYY"},a)):""))}),A=n(29924),_=n.n(A),U=function(e){var t=e.contactArray,n=e.onChange,l=e.onHover;e.parentCallback;function c(e){l(e)}return r.createElement(r.Fragment,null,r.createElement("ul",{className:"r-result-list event-result-list"},t.map((function(e,t){return r.createElement("li",{key:t,className:"r-list-item-group",onMouseEnter:function(){return c(e.UID)},onMouseLeave:function(){return c(null)},onClick:function(){return t=e.UID,void n(t);var t}},r.createElement(a.rU,{className:"r-list-item-link",style:{textDecoration:"none"},to:{pathname:_()(e.title).replace(/[^a-zA-Z ]/g,"").replace(/\s/g,"-").toLowerCase(),search:"?u=".concat(e.UID),state:{idItem:e.UID}}}),r.createElement(k,{contactItem:e,key:e.created}))}))))},C=n(38458),H=n(35108),D=n(16683),P=n(22948),M=n(79221),L=n(48818),Z=n.n(L),V=n(59834),T=n(67676);function B(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==n)return;var r,a,l=[],c=!0,i=!1;try{for(n=n.call(e);!(c=(r=n.next()).done)&&(l.push(r.value),!t||l.length!==t);c=!0);}catch(e){i=!0,a=e}finally{try{c||null==n.return||n.return()}finally{if(i)throw a}}return l}(e,t)||function(e,t){if(!e)return;if("string"==typeof e)return F(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);"Object"===n&&e.constructor&&(n=e.constructor.name);if("Map"===n||"Set"===n)return Array.from(e);if("Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return F(e,t)}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function F(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function Y(e){var t=e.activeItem,n=e.arrayOfLatLngs,r=(0,C.Sx)();if(t){var a=[];a.push(t.geolocation.latitude),a.push(t.geolocation.longitude),r.setView(a,15)}else{var l=new(Z().LatLngBounds)(n);r.fitBounds(l)}return null}var q=function(e){var t=B((0,r.useState)(null),2),n=t[0],l=t[1],c=B((0,r.useState)(null),2),i=(c[0],c[1]),o=B((0,r.useState)([]),2),s=o[0],u=o[1],m=B((0,r.useState)(null),2),f=m[0],p=m[1];function d(e){return new(Z().Icon)({iconUrl:e,iconSize:[29,37]})}(0,r.useEffect)((function(){var t=e.items.filter((function(e){return e.geolocation.latitude&&50.4989185!==e.geolocation.latitude&&4.7184485!==e.geolocation.longitude}));u(t)}),[e]);var v=function(t){return t===e.clickId||t===e.hoverId?999:1};return(0,r.useEffect)((function(){if(null!==e.clickId){var t=s&&s.filter((function(t){return t.UID===e.clickId}));l(t[0])}else l(null)}),[e.clickId]),(0,r.useEffect)((function(){if(e.hoverId){var t=s&&s.filter((function(t){return t.UID===e.hoverId}));i(t[0])}else i(null)}),[e.hoverId]),(0,r.useEffect)((function(){if(s.length>0){var e=[];s.map((function(t,n){var r=t.geolocation.latitude,a=t.geolocation.longitude;e.push([r,a])})),p(e)}}),[s]),r.createElement("div",null,r.createElement(H.h,{style:{height:"calc(100vh - ".concat(e.headerHeight,"px)"),minHeight:"600px"},center:[50.85034,4.35171],zoom:15},r.createElement(D.I,{attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',url:"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"}),null!=f?r.createElement(Y,{activeItem:n,arrayOfLatLngs:f&&f}):"",s&&s.map((function(t){return r.createElement(P.J,{key:t.UID,icon:(n=t.UID,n===e.clickId||n===e.hoverId?d(T.Z):d(V.Z)),zIndexOffset:v(t.UID),position:[t.geolocation?t.geolocation.latitude:"",t.geolocation?t.geolocation.longitude:""],eventHandlers:{mouseover:function(e){}}},r.createElement(M.G,{closeButton:!1},r.createElement(a.rU,{className:"r-map-popup",style:{textDecoration:"none"},to:{pathname:_()(t.title.replace(/\s/g,"-").toLowerCase()),search:"?u=".concat(t.UID),state:{idItem:t.UID}}},r.createElement("span",{className:"r-map-popup-title"},t.title),r.createElement("p",{className:"r-map-popup-category"},t.category&&t.category.title))));var n}))))},z=["u"];function R(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function $(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?R(Object(n),!0).forEach((function(t){W(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):R(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function W(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function G(e){return function(e){if(Array.isArray(e))return Q(e)}(e)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(e)||K(e)||function(){throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function J(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null==n)return;var r,a,l=[],c=!0,i=!1;try{for(n=n.call(e);!(c=(r=n.next()).done)&&(l.push(r.value),!t||l.length!==t);c=!0);}catch(e){i=!0,a=e}finally{try{c||null==n.return||n.return()}finally{if(i)throw a}}return l}(e,t)||K(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function K(e,t){if(e){if("string"==typeof e)return Q(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?Q(e,t):void 0}}function Q(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function X(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},l=Object.keys(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(r=0;r<l.length;r++)n=l[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}function ee(e){return r.createElement(a.UT,null,r.createElement(te,{queryFilterUrl:e.queryFilterUrl,queryUrl:e.queryUrl+"?b_size=20",proposeUrl:e.proposeUrl}))}function te(e){var t=n(31296),c=Object.assign({b_start:0,fullobjects:1},t.parse((0,g.Z)().toString())),o=(c.u,X(c,z)),s=J((0,r.useState)([]),2),u=s[0],m=s[1],f=J((0,r.useState)([]),2),p=f[0],d=f[1],v=J((0,r.useState)(null),2),y=v[0],E=v[1],b=J((0,r.useState)(null),2),w=b[0],N=b[1],O=J((0,r.useState)(o),2),S=O[0],j=O[1],I=J((0,r.useState)(0),2),k=I[0],A=I[1],_=J((0,r.useState)(!1),2),C=_[0],H=_[1],D=J((0,r.useState)(null),2),P=(D[0],D[1],(0,i.Z)({method:"get",url:"",baseURL:e.queryUrl,headers:{Accept:"application/json"},params:S,load:C},[])),M=P.response,L=(P.error,P.isLoading),Z=P.isMore;(0,r.useEffect)((function(){null!==M&&(m(Z?function(e){return[].concat(G(e),G(M.items))}:M.items),d(M.items_total))}),[M]);var V=function(e){E(e)};(0,r.useEffect)((function(){j((function(e){return $($({},e),{},{b_start:k})}))}),[k]);var T=document.getElementById("portal-header").offsetHeight,B=(0,r.useRef)(),F=J(r.useState({height:0}),2),Y=F[0],R=F[1];(0,r.useEffect)((function(){R({height:B.current.clientHeight})}),[B.current]);var W,K;r.useRef(0),document.getElementById("portal-logo").offsetHeight;return u&&u.length>0?(W=r.createElement(U,{onChange:V,contactArray:u,onHover:function(e){N(e)}}),K=r.createElement(q,{headerHeight:Y.height+T,clickId:y,hoverId:w,items:u})):W=r.createElement("p",null,"Aucun événement n'a été trouvé"),r.createElement(a.UT,null,r.createElement("div",{className:"ref",ref:function(e){}},r.createElement("div",{className:"r-result-filter-container",ref:B,style:{top:T}},r.createElement("div",{id:"r-result-filter",className:"r-result-filter container annuaire-result-filter"},r.createElement(h,{url:e.queryFilterUrl,activeFilter:S,onChange:function(e){H(!1),A((function(e){return 0})),j(e),window.scrollTo(0,0)}}),e.proposeUrl&&r.createElement("div",{className:"r-add-event"},r.createElement("a",{target:"_blank",href:e.proposeUrl},"Proposer un événement")),p>0?r.createElement("p",{className:"r-results-numbers"},r.createElement("span",null,p),p>1?" événements trouvés":"événement trouvé"):r.createElement("p",{className:"r-results-numbers"},"Aucun résultat"))),r.createElement(l.rs,null,r.createElement(l.AW,{path:"/:name"},r.createElement("div",{className:"r-wrapper container r-annuaire-wrapper"},r.createElement("div",{className:"r-result r-annuaire-result"},r.createElement(x,{queryUrl:e.queryUrl,onChange:V})),r.createElement("div",{className:"r-map annuaire-map",style:{top:Y.height+T,height:"calc(100vh-"+Y.height+T}},K))),r.createElement(l.AW,{exact:!0,path:"*"},r.createElement("div",{className:"r-wrapper container r-annuaire-wrapper"},r.createElement("div",{className:"r-result r-annuaire-result"},r.createElement("div",null,W),r.createElement("div",{className:"r-load-more"},p-20>k?r.createElement("button",{onClick:function(){A((function(e){return e+20})),H(!0)},className:"btn-grad"},L?"Chargement...":"Plus de résultats"):r.createElement("span",{className:"no-more-result"},L?"Chargement...":""))),r.createElement("div",{className:"r-map annuaire-map",style:{top:Y.height+T,height:"calc(100vh-"+Y.height+T}},K))))))}}}]);