"use strict";(self.webpackChunkimio_smartweb_core_webcomponents=self.webpackChunkimio_smartweb_core_webcomponents||[]).push([[919],{34919:(e,t,r)=>{r.r(t),r.d(t,{default:()=>T});var a=r(25602),n=r(8174),l=r(32101),s=r(41665),c=r(37178),i=r(83198),o=r(72668);const u=["SearchableText"],m=["SearchableText"];function d(e,t){if(null==e)return{};var r,a,n=function(e,t){if(null==e)return{};var r={};for(var a in e)if({}.hasOwnProperty.call(e,a)){if(-1!==t.indexOf(a))continue;r[a]=e[a]}return r}(e,t);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);for(a=0;a<l.length;a++)r=l[a],-1===t.indexOf(r)&&{}.propertyIsEnumerable.call(e,r)&&(n[r]=e[r])}return n}function h(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,a)}return r}function f(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?h(Object(r),!0).forEach((function(t){g(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):h(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function g(e,t,r){return(t=v(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}function v(e){var t=function(e,t){if("object"!=typeof e||!e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var a=r.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:t+""}const p=function(e){let t=(0,s.Zp)();const[r,n]=(0,a.useState)(e.activeFilter),[h,g]=(0,a.useState)({}),[p,b]=(0,a.useState)(null),[E,y]=(0,a.useState)(null);(0,a.useEffect)((()=>{(()=>{const t=c.A.request({method:"get",url:"",baseURL:e.url+"/@vocabularies/imio.smartweb.vocabulary.Topics",headers:{Accept:"application/json"}}),r=c.A.request({method:"get",url:"",baseURL:e.url+"/@vocabularies/imio.smartweb.vocabulary.IAm",headers:{Accept:"application/json"}});c.A.all([t,r]).then(c.A.spread((function(){const e=arguments.length<=0?void 0:arguments[0],t=arguments.length<=1?void 0:arguments[1];if(null!==e){const t=e.data.items.map((e=>({value:e.token,label:e.title})));b(t)}if(null!==t){const e=t.data.items.map((e=>({value:e.token,label:e.title})));y(e)}}))).catch((e=>{console.error("errors")}))})()}),[]);const P=e=>{g({SearchableText:e.target.value}),e.target.value?n((t=>f(f({},t),{},{SearchableText:e.target.value})),[]):n((e=>{const t=f({},e),{SearchableText:r}=t;return d(t,u)}))},N=(0,a.useCallback)(((e,t)=>{const r=t.name;e?n((t=>f(f({},t),{},{[r]:e.value})),[]):n((e=>{const t=f({},e),{[r]:a}=t;return d(t,[r].map(v))}))})),w=(0,a.useRef)(!0);(0,a.useEffect)((()=>{w.current?w.current=!1:(t({pathname:"./",search:o.A.stringify(r)}),e.onChange(r))}),[r]);let A=p&&p.filter((t=>t.value===e.activeFilter.topics)),j=E&&E.filter((t=>t.value===e.activeFilter.iam));const S={control:e=>f(f({},e),{},{backgroundColor:"white",borderRadius:"0",height:"50px"}),placeholder:e=>f(f({},e),{},{color:"000",fontWeight:"bold",fontSize:"12px",textTransform:"uppercase",letterSpacing:"1.2px"}),option:(e,t)=>{let{data:r,isDisabled:a,isFocused:n,isSelected:l}=t;return f({},e)}};return a.createElement(a.Fragment,null,a.createElement("div",{className:"col-md-6 py-1 r-search search-bar-filter"},a.createElement("form",{onSubmit:e=>{e.preventDefault(),h.SearchableText?n((e=>f(f({},e),{},{SearchableText:h.SearchableText})),[]):n((e=>{const t=f({},e),{SearchableText:r}=t;return d(t,m)}))}},a.createElement("label",null,a.createElement(i.rk,null,(e=>{let{translate:t}=e;return a.createElement("input",{name:"SearchableText",type:"text",onChange:P,value:h.SearchableText,placeholder:t({text:"Recherche"})})}))),a.createElement("button",{type:"submit"}))),a.createElement("div",{className:"col-md-3 col-lg-2 py-1 r-search search-select-filter"},a.createElement(i.rk,null,(e=>{let{translate:t}=e;return a.createElement(l.Ay,{styles:S,name:"iam",className:"r-search-select",isClearable:!0,onChange:N,options:E&&E,placeholder:t({text:"Je suis"}),value:j&&j[0]})}))),a.createElement("div",{className:"col-md-3 col-lg-2 py-1 r-search search-select-filter"},a.createElement(i.rk,null,(e=>{let{translate:t}=e;return a.createElement(l.Ay,{styles:S,name:"topics",className:"r-search-select",isClearable:!0,onChange:N,options:p&&p,placeholder:t({text:"Thématiques"}),value:A&&A[0]})}))))};var b=r(86110),E=r(14799),y=r.n(E);const P=e=>{const[t,r]=(0,a.useState)([]),{response:n,error:l,isLoading:s}=(0,b.A)({method:"get",url:"",baseURL:e.url+"/@search?&_core=directory&b_size=100",headers:{Accept:"application/json"},params:e.urlParams.SearchableText||e.urlParams.iam||e.urlParams.topics?e.urlParams:{}},[e]);return(0,a.useEffect)((()=>{r(null!==n?n.items:[])}),[n]),a.createElement("div",{className:"search-contact"},a.createElement("div",{className:"r-search-header"},a.createElement("h2",{className:"r-search-header-title"},a.createElement(i.HT,{text:"Contacts"})),a.createElement("p",{className:"r-search-header-count"},t.length>0?a.createElement(a.Fragment,null," ",t.length," ",a.createElement(i.HT,{text:"Résultats"})," "):a.createElement(i.HT,{text:"Aucun résultat"}))),a.createElement("ul",{className:"r-search-list"},t.map(((t,r)=>a.createElement("li",{key:r,className:"r-search-item"},a.createElement("a",{href:t._url},a.createElement("div",{className:"r-search-img"},t.has_leadimage[0]?a.createElement("div",{className:"r-search-img",style:{backgroundImage:"url("+t.image_url+")"}}):a.createElement("div",{className:"r-search-img no-search-item-img"})),a.createElement(y(),{highlightClassName:"r-search-highlighter",searchWords:[e.urlParams.SearchableText],textToHighlight:t.title})))))))},N=e=>{const[t,r]=(0,a.useState)([]),{response:n,error:l,isLoading:s}=(0,b.A)({method:"get",url:"",baseURL:e.url+"/@search?&_core=news&b_size=100",headers:{Accept:"application/json"},params:e.urlParams.SearchableText||e.urlParams.iam||e.urlParams.topics?e.urlParams:{}},[e]);return(0,a.useEffect)((()=>{r(null!==n?n.items:[])}),[n]),a.createElement("div",{className:"search-news"},a.createElement("div",{className:"r-search-header"},a.createElement("h2",{className:"r-search-header-title"},a.createElement(i.HT,{text:"Actualités"})),a.createElement("p",{className:"r-search-header-count"},t.length>0?a.createElement(a.Fragment,null," ",t.length," ",a.createElement(i.HT,{text:"Résultats"})," "):a.createElement(i.HT,{text:"Aucun résultat"}))),a.createElement("ul",{className:"r-search-list"},t.map(((t,r)=>a.createElement("li",{key:r,className:"r-search-item"},a.createElement("a",{href:t._url},a.createElement("div",{className:"r-search-img"},t.has_leadimage[0]?a.createElement("div",{className:"r-search-img",style:{backgroundImage:"url("+t.image_url+")"}}):a.createElement("div",{className:"r-search-img no-search-item-img"})),a.createElement(y(),{highlightClassName:"r-search-highlighter",searchWords:[e.urlParams.SearchableText],textToHighlight:t.title})))))))},w=e=>{const[t,r]=(0,a.useState)([]),{response:n,error:l,isLoading:s}=(0,b.A)({method:"get",url:"",baseURL:e.url+"/@search?&_core=events&b_size=100",headers:{Accept:"application/json"},params:e.urlParams.SearchableText||e.urlParams.iam||e.urlParams.topics?e.urlParams:{}},[e]);return(0,a.useEffect)((()=>{r(null!==n?n.items:[])}),[n]),a.createElement("div",{className:"search-events"},a.createElement("div",{className:"r-search-header"},a.createElement("h2",{className:"r-search-header-title"},a.createElement(i.HT,{text:"Événements"})),a.createElement("p",{className:"r-search-header-count"},t.length>0?a.createElement(a.Fragment,null," ",t.length," ",a.createElement(i.HT,{text:"Résultats"})," "):a.createElement(i.HT,{text:"Aucun résultat"}))),a.createElement("ul",{className:"r-search-list"},t.map(((t,r)=>a.createElement("li",{key:r,className:"r-search-item"},a.createElement("a",{href:t._url},a.createElement("div",{className:"r-search-img"},t.has_leadimage[0]?a.createElement("div",{className:"r-search-img",style:{backgroundImage:"url("+t.image_url+")"}}):a.createElement("div",{className:"r-search-img no-search-item-img"})),a.createElement(y(),{highlightClassName:"r-search-highlighter",searchWords:[e.urlParams.SearchableText],textToHighlight:t.title})))))))},A=e=>{const[t,r]=(0,a.useState)([]),{response:n,error:l,isLoading:s}=(0,b.A)({method:"get",url:"",baseURL:e.url+"/@search?&b_size=100",headers:{Accept:"application/json"},params:e.urlParams.SearchableText||e.urlParams.iam||e.urlParams.topics?e.urlParams:{}},[e]);return(0,a.useEffect)((()=>{r(null!==n?n.items:[])}),[n]),a.createElement("div",{className:"search-web"},a.createElement("div",{className:"r-search-header"},a.createElement("h2",{className:"r-search-header-title"},a.createElement(i.HT,{text:"Infos pratiques"})),a.createElement("p",{className:"r-search-header-count"},t.length>0?a.createElement(a.Fragment,null," ",t.length," ",a.createElement(i.HT,{text:"Résultats"})," "):a.createElement(i.HT,{text:"Aucun résultat"}))),a.createElement("ul",{className:"r-search-list"},t.map(((t,r)=>a.createElement("li",{key:r,className:"r-search-item"},a.createElement("a",{href:t["@id"]},a.createElement(y(),{highlightClassName:"r-search-highlighter",searchWords:[e.urlParams.SearchableText],textToHighlight:t.title})))))))};var j=r(18874),S=r(48743);function T(e){return a.createElement(n.Kd,null,a.createElement(i.Kq,{language:e.currentLanguage,translation:S.A},a.createElement(k,{queryFilterUrl:e.queryFilterUrl,queryUrl:e.queryUrl,resultOption:JSON.parse(e.resultOption),areViewsAvailable:JSON.parse(e.areViewsAvailable)})))}const k=e=>{console.log(e.areViewsAvailable);const t=o.A.parse((0,j.A)().toString()),{SearchableText:r,iam:n,topics:l}=t,s={SearchableText:r,iam:n,topics:l},[c,u]=(0,a.useState)(s),[m,d]=(0,a.useState)(6);return a.createElement("div",{className:"ref"},a.createElement("div",{className:"r-search r-search-container"},a.createElement("div",{className:"row r-search-filters"},a.createElement(p,{url:e.queryUrl,activeFilter:c,onChange:e=>{u(e)}})),a.createElement("div",{className:"r-search-result"},a.createElement(A,{urlParams:c,url:e.queryUrl}),e.resultOption.news&&(e.areViewsAvailable.news?a.createElement(N,{urlParams:c,url:e.queryUrl,available:e.areViewsAvailable.news}):a.createElement("div",{className:"r-search-header"},a.createElement("h2",{className:"r-search-header-title"},a.createElement(i.HT,{text:"Actualités"})),a.createElement("div",{className:"search-disabled-message"},"Recherche impossible car vue actualités supprimée"))),e.resultOption.events&&(e.areViewsAvailable.events?a.createElement(w,{urlParams:c,url:e.queryUrl,available:e.areViewsAvailable.events}):a.createElement("div",{className:"r-search-header"},a.createElement("h2",{className:"r-search-header-title"},a.createElement(i.HT,{text:"Événements"})),a.createElement("div",{className:"search-disabled-message"},"Recherche impossible car vue événements supprimée"))),e.resultOption.directory&&(e.areViewsAvailable.directory?a.createElement(P,{urlParams:c,url:e.queryUrl,available:e.areViewsAvailable.directory}):a.createElement("div",{className:"r-search-header"},a.createElement("h2",{className:"r-search-header-title"},a.createElement(i.HT,{text:"Annuaire"})),a.createElement("div",{className:"search-disabled-message"},"Recherche impossible car vue annuaire supprimée"))))))}},86110:(e,t,r)=>{r.d(t,{A:()=>i});var a=r(25602),n=r(37178);function l(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),r.push.apply(r,a)}return r}function s(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?l(Object(r),!0).forEach((function(t){c(e,t,r[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):l(Object(r)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))}))}return e}function c(e,t,r){return(t=function(e){var t=function(e,t){if("object"!=typeof e||!e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var a=r.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:t+""}(t))in e?Object.defineProperty(e,t,{value:r,enumerable:!0,configurable:!0,writable:!0}):e[t]=r,e}const i=e=>{const[t,r]=(0,a.useState)(null),[l,c]=(0,a.useState)(""),[i,o]=(0,a.useState)(!0),[u,m]=(0,a.useState)(!1),d=new AbortController;return(0,a.useEffect)((()=>((async e=>{if(o(!0),e.load?m(!0):m(!1),0===Object.keys(e.params).length)return r(null),void o(!1);try{if(Array.isArray(e.url)){const t=e.url.map(((t,r)=>{const{url:a,identifier:l}="string"==typeof t?{url:t,identifier:"request_".concat(r)}:t;return n.A.request(s(s({},e),{},{url:a,signal:d.signal})).then((e=>({identifier:l,data:e.data})))})),a=(await Promise.all(t)).reduce(((e,t)=>{let{identifier:r,data:a}=t;return e[r]=a,e}),{});r(a)}else{const t=await n.A.request(e);r(t.data)}c(null)}catch(e){c(e),r(null)}finally{o(!1)}})(s(s({},e),{},{signal:d.signal})),()=>d.abort())),[e.params]),{response:t,error:l,isLoading:i,isMore:u}}},18874:(e,t,r)=>{r.d(t,{A:()=>n});var a=r(41665);const n=function(){return new URLSearchParams((0,a.zy)().search)}},48743:(e,t,r)=>{r.d(t,{A:()=>a});const a={Publié:{en:"Published",fr:"Publié",de:"Veröffentlicht",nl:"Gepubliceerd"},Actualisé:{en:"Updated",fr:"Actualisé",de:"Aktualisiert",nl:"Bijgewerkt"},Événements:{en:"Events",fr:"Événements",de:"Veranstaltungen",nl:"Evenementen"},Actualités:{en:"News",fr:"Actualités",de:"Nachrichten",nl:"Nieuws"},Contacts:{en:"Contacts",fr:"Contacts",de:"Kontakte",nl:"Contacten"},"Infos pratiques":{en:"Practical information",fr:"Infos pratiques",de:"Praktische Informationen",nl:"Praktische informatie"},"Chargement...":{en:"Loading",fr:"Chargement...",de:"Laden",nl:"Laden..."},Recherche:{en:"Search",fr:"Recherche",de:"Suche",nl:"Zoeken"},Thématiques:{en:"Themes",fr:"Thématiques",de:"Themen",nl:"Thema's"},"Je suis":{en:"I am",fr:"Je suis",de:"Ich bin",nl:"Ik ben"},Catégories:{en:"Categories",fr:"Catégories",de:"Kategorien",nl:"Categorieën"},"Catégories locale":{en:"Local categories",fr:"Catégories locale",de:"Lokale Kategorien",nl:"Lokale categorieën"},"Catégories spécifiques":{en:"Specific categories",fr:"Catégories spécifiques",de:"Spezifische Kategorien",nl:"Specifieke categorieën"},Quoi:{en:"What",fr:"Quoi",de:"Was",nl:"Wat"},Facilités:{en:"Facilities",fr:"Facilités",de:"Einrichtungen",nl:"Faciliteiten"},"Plus de résultats":{en:"More results",fr:"Plus de résultats",de:"Mehr Ergebnisse",nl:"Meer resultaten"},"Aucun résultat":{en:"No result",fr:"Aucun résultat",de:"Kein Ergebnis",nl:"Geen resultaat"},Résultats:{en:"Results",fr:"Résultats",de:"Ergebnisse",nl:"Resultaten"},Retour:{en:"Return",fr:"Retour",de:"Zurück",nl:"Terug"},Téléchargements:{en:"Downloads",fr:"Téléchargements",de:"Downloads",nl:"Downloads"},Billetterie:{en:"Ticketing",fr:"Billetterie",de:"Tickets",nl:"Ticketverkoop"},"Lien vers la vidéo":{en:"Link to video",fr:"Lien vers la vidéo",de:"Link zum Video",nl:"Link naar video"},"Participation en ligne":{en:"Join online",fr:"Participation en ligne",de:"Online teilnehmen",nl:"Doe online mee"},"Actualités trouvées":{en:" News found",fr:" Actualités trouvées",de:" Nachrichten gefunden",nl:" Nieuws gevonden"},"Actualité trouvée":{en:" News found",fr:" Actualité trouvée",de:" Nachricht gefunden",nl:" Nieuws gevonden"},"Aucune actualité n'a été trouvée":{en:"No news was found",fr:"Aucune actualité n'a été trouvée",de:"Keine Nachrichten gefunden",nl:"Geen nieuws gevonden"},"Proposer une actualité":{en:"Suggest a news",fr:"Proposer une actualité",de:"Nachricht vorschlagen",nl:"Nieuws voorstellen"},"événements trouvés":{en:" Events found",fr:" Événements trouvés",de:" Veranstaltungen gefunden",nl:" Evenementen gevonden"},"projets trouvés":{en:" Projects found",fr:" Projets trouvés",de:" Projekte gefunden",nl:" Projecten gevonden"},"projet trouvé":{en:" Project found",fr:" Projet trouvé",de:" Projekt gefunden",nl:" Project gevonden"},"événement trouvé":{en:" Event found",fr:" Événement trouvé",de:" Veranstaltung gefunden",nl:" Evenement gevonden"},Gratuit:{en:"Free",fr:"Gratuit",de:"Kostenlos",nl:"Gratis"},"Aucun événement n'a été trouvé":{en:"No event was found",fr:"Aucun événement n'a été trouvé",de:"Keine Veranstaltungen gefunden",nl:"Geen evenement gevonden"},"Proposer un événement":{en:"Suggest a event",fr:"Proposer un événement",de:"Veranstaltung vorschlagen",nl:"Evenement voorstellen"},"Infos pratiques":{en:"Practical information",fr:"Infos pratiques",de:"Praktische Informationen",nl:"Praktische informatie"},"Accessible aux PMR":{en:"Accessibility for PRM",fr:"Accessible aux PMR",de:"Barrierefreiheit für PMR",nl:"Toegankelijk voor PRM"},"Lien de l'événement":{en:"Event link",fr:"Lien de l'événement",de:"Veranstaltungslink",nl:"Evenement link"},"contacts trouvés":{en:" Contact found",fr:" Contacts trouvés",de:" Kontakt gefunden",nl:" Contact gevonden"},"contact trouvé":{en:" Contact found",fr:" Contact trouvé",de:" Kontakt gefunden",nl:" Contact gevonden"},"Aucun contact n'a été trouvé":{en:"No contact was found",fr:"Aucun contact n'a été trouvé",de:"Kein Kontakt gefunden",nl:"Geen contact gevonden"},"Proposer un contact":{en:"Suggest a contact",fr:"Proposer un contact",de:"Kontakt vorschlagen",nl:"Contact voorstellen"},"projets trouvés":{en:" Projects found",fr:" Projets trouvés",de:" Projekte gefunden",nl:" Projecten gevonden"},"projet trouvé":{en:" Project found",fr:" Projet trouvé",de:" Projekt gefunden",nl:" Project gevonden"},"Aucun projet n'a été trouvé":{en:"No project was found",fr:"Aucun projet n'a été trouvé",de:"Kein Projekt gefunden",nl:"Geen project gevonden"},"Proposer un projet":{en:"Suggest a project",fr:"Proposer un projet",de:"Projekt vorschlagen",nl:"Project voorstellen"},Quand:{en:"When",fr:"Quand",de:"Wann",nl:"Wanneer"},"Toutes les dates":{en:"All dates",fr:"Toutes les dates",de:"Alle Daten",nl:"Alle data"},"Aujourd'hui":{en:"Today",fr:"Aujourd'hui",de:"Heute",nl:"Vandaag"},Demain:{en:"Tomorrow",fr:"Demain",de:"Morgen",nl:"Morgen"},"Ce week-end":{en:"This weekend",fr:"Ce week-end",de:"Dieses Wochenende",nl:"Dit weekend"},"Cette semaine":{en:"This week",fr:"Cette semaine",de:"Diese Woche",nl:"Deze week"},"Ce mois-ci":{en:"This month",fr:"Ce mois-ci",de:"Diesen Monat",nl:"Deze maand"},"Personnalisé (Du ... au ...)":{en:"Custom (From ... to ...)",fr:"Personnalisé (Du ... au ...)",de:"Benutzerdefiniert (Von ... bis ...)",nl:"Aangepast (Van ... tot ...)"},Le:{en:"On",fr:"Le",de:"Am",nl:"Op"},de:{en:"of",fr:"de",de:"von",nl:"van"},à:{en:"at",fr:"à",de:"um",nl:"om"},Du:{en:"From",fr:"Du",de:"Von",nl:"Van"},au:{en:"to",fr:"au",de:"bis",nl:"tot"},Personnalisé:{en:"Custom",fr:"Personnalisé",de:"Benutzerdefiniert",nl:"Aangepast"},Monday:{en:"Monday",fr:"Lundi",de:"Montag",nl:"Maandag"},Tuesday:{en:"Tuesday",fr:"Mardi",de:"Dienstag",nl:"Dinsdag"},Wednesday:{en:"Wednesday",fr:"Mercredi",de:"Mittwoch",nl:"Woensdag"},Thursday:{en:"Thursday",fr:"Jeudi",de:"Donnerstag",nl:"Donderdag"},Friday:{en:"Friday",fr:"Vendredi",de:"Freitag",nl:"Vrijdag"},Saturday:{en:"Saturday",fr:"Samedi",de:"Samstag",nl:"Zaterdag"},Sunday:{en:"Sunday",fr:"Dimanche",de:"Sonntag",nl:"Zondag"},Fermé:{en:"Closed",fr:"Fermé",de:"Geschlossen",nl:"Gesloten"},Ouvert:{en:"Open",fr:"Ouvert",de:"Geöffnet",nl:"Open"},Itinéraire:{en:"Itinerary",fr:"Itinéraire",de:"Route",nl:"Route"},"Filtrer par profil":{en:"Filter by profile",fr:"Filtrer par profil",de:"Nach Profile filtern",nl:"Filteren op profiel"},"Filtrer par thématique":{en:"Filter by theme",fr:"Filtrer par thématique",de:"Nach Thema filtern",nl:"Filteren op thema"},Commentaires:{en:"Comments",fr:"Commentaires",de:"Kommentare",nl:"Reacties"}}}}]);