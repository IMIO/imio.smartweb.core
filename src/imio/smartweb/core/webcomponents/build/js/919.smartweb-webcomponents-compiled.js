"use strict";(self.webpackChunkimio_smartweb_core_webcomponents=self.webpackChunkimio_smartweb_core_webcomponents||[]).push([[919],{34919:(e,t,a)=>{a.r(t),a.d(t,{default:()=>N});var r=a(25602),n=a(8174),l=a(19154),s=a(41665),c=a(99938),i=a(83198),u=a(72668);const o=function(e){let t=(0,s.Zp)();const[a,n]=(0,r.useState)(e.activeFilter),[o,m]=(0,r.useState)({}),[d,h]=(0,r.useState)(null),[g,f]=(0,r.useState)(null);(0,r.useEffect)((()=>{(()=>{const t=c.A.request({method:"get",url:"",baseURL:e.url+"/@vocabularies/imio.smartweb.vocabulary.Topics",headers:{Accept:"application/json"}}),a=c.A.request({method:"get",url:"",baseURL:e.url+"/@vocabularies/imio.smartweb.vocabulary.IAm",headers:{Accept:"application/json"}});c.A.all([t,a]).then(c.A.spread((function(){const e=arguments.length<=0?void 0:arguments[0],t=arguments.length<=1?void 0:arguments[1];if(null!==e){const t=e.data.items.map((e=>({value:e.token,label:e.title})));h(t)}if(null!==t){const e=t.data.items.map((e=>({value:e.token,label:e.title})));f(e)}}))).catch((e=>{console.error("errors")}))})()}),[]);const v=e=>{m({SearchableText:e.target.value}),e.target.value?n((t=>({...t,SearchableText:e.target.value})),[]):n((e=>{const t={...e},{SearchableText:a,...r}=t;return r}))},E=(0,r.useCallback)(((e,t)=>{const a=t.name;e?n((t=>({...t,[a]:e.value})),[]):n((e=>{const t={...e},{[a]:r,...n}=t;return n}))})),p=(0,r.useRef)(!0);(0,r.useEffect)((()=>{p.current?p.current=!1:(t({pathname:"./",search:u.A.stringify(a)}),e.onChange(a))}),[a]);let b=d&&d.filter((t=>t.value===e.activeFilter.topics)),N=g&&g.filter((t=>t.value===e.activeFilter.iam));const T={control:e=>({...e,backgroundColor:"white",borderRadius:"0",height:"50px"}),placeholder:e=>({...e,color:"000",fontWeight:"bold",fontSize:"12px",textTransform:"uppercase",letterSpacing:"1.2px"}),option:(e,t)=>{let{data:a,isDisabled:r,isFocused:n,isSelected:l}=t;return{...e}}};return r.createElement(r.Fragment,null,r.createElement("div",{className:"col-md-6 py-1 r-search search-bar-filter"},r.createElement("form",{onSubmit:e=>{e.preventDefault(),o.SearchableText?n((e=>({...e,SearchableText:o.SearchableText})),[]):n((e=>{const t={...e},{SearchableText:a,...r}=t;return r}))}},r.createElement("label",null,r.createElement(i.rk,null,(e=>{let{translate:t}=e;return r.createElement("input",{name:"SearchableText",type:"text",onChange:v,value:o.SearchableText,placeholder:t({text:"Recherche"})})}))),r.createElement("button",{type:"submit"}))),r.createElement("div",{className:"col-md-3 col-lg-2 py-1 r-search search-select-filter"},r.createElement(i.rk,null,(e=>{let{translate:t}=e;return r.createElement(l.Ay,{styles:T,name:"iam",className:"r-search-select",isClearable:!0,onChange:E,options:g&&g,placeholder:t({text:"Je suis"}),value:N&&N[0]})}))),r.createElement("div",{className:"col-md-3 col-lg-2 py-1 r-search search-select-filter"},r.createElement(i.rk,null,(e=>{let{translate:t}=e;return r.createElement(l.Ay,{styles:T,name:"topics",className:"r-search-select",isClearable:!0,onChange:E,options:d&&d,placeholder:t({text:"Thématiques"}),value:b&&b[0]})}))))};var m=a(86110),d=a(14799),h=a.n(d);const g=e=>{const[t,a]=(0,r.useState)([]),{response:n,error:l,isLoading:s}=(0,m.A)({method:"get",url:"",baseURL:e.url+"/@search?&_core=directory&b_size=100",headers:{Accept:"application/json"},params:e.urlParams.SearchableText||e.urlParams.iam||e.urlParams.topics?e.urlParams:{}},[e]);return(0,r.useEffect)((()=>{a(null!==n?n.items:[])}),[n]),r.createElement("div",{className:"search-contact"},r.createElement("div",{className:"r-search-header"},r.createElement("h2",{className:"r-search-header-title"},r.createElement(i.HT,{text:"Contacts"})),r.createElement("p",{className:"r-search-header-count"},t.length>0?r.createElement(r.Fragment,null," ",t.length," "," "," ",r.createElement(i.HT,{text:"Résultats"})," "):r.createElement(i.HT,{text:"Aucun résultat"}))),r.createElement("ul",{className:"r-search-list"},t.map(((t,a)=>r.createElement("li",{key:a,className:"r-search-item"},r.createElement("a",{href:t._url},r.createElement("div",{className:"r-search-img"},t.has_leadimage[0]?r.createElement("div",{className:"r-search-img",style:{backgroundImage:"url("+t.image_url+")"}}):r.createElement("div",{className:"r-search-img no-search-item-img"})),r.createElement(h(),{highlightClassName:"r-search-highlighter",searchWords:[e.urlParams.SearchableText],textToHighlight:t.title})))))))},f=e=>{const[t,a]=(0,r.useState)([]),{response:n,error:l,isLoading:s}=(0,m.A)({method:"get",url:"",baseURL:e.url+"/@search?&_core=news&b_size=100",headers:{Accept:"application/json"},params:e.urlParams.SearchableText||e.urlParams.iam||e.urlParams.topics?e.urlParams:{}},[e]);return(0,r.useEffect)((()=>{a(null!==n?n.items:[])}),[n]),r.createElement("div",{className:"search-news"},r.createElement("div",{className:"r-search-header"},r.createElement("h2",{className:"r-search-header-title"},r.createElement(i.HT,{text:"Actualités"})),r.createElement("p",{className:"r-search-header-count"},t.length>0?r.createElement(r.Fragment,null," ",t.length," "," "," ",r.createElement(i.HT,{text:"Résultats"})," "):r.createElement(i.HT,{text:"Aucun résultat"}))),r.createElement("ul",{className:"r-search-list"},t.map(((t,a)=>r.createElement("li",{key:a,className:"r-search-item"},r.createElement("a",{href:t._url},r.createElement("div",{className:"r-search-img"},t.has_leadimage[0]?r.createElement("div",{className:"r-search-img",style:{backgroundImage:"url("+t.image_url+")"}}):r.createElement("div",{className:"r-search-img no-search-item-img"})),r.createElement(h(),{highlightClassName:"r-search-highlighter",searchWords:[e.urlParams.SearchableText],textToHighlight:t.title})))))))},v=e=>{const[t,a]=(0,r.useState)([]),{response:n,error:l,isLoading:s}=(0,m.A)({method:"get",url:"",baseURL:e.url+"/@search?&_core=events&b_size=100",headers:{Accept:"application/json"},params:e.urlParams.SearchableText||e.urlParams.iam||e.urlParams.topics?e.urlParams:{}},[e]);return(0,r.useEffect)((()=>{a(null!==n?n.items:[])}),[n]),r.createElement("div",{className:"search-events"},r.createElement("div",{className:"r-search-header"},r.createElement("h2",{className:"r-search-header-title"},r.createElement(i.HT,{text:"Événements"})),r.createElement("p",{className:"r-search-header-count"},t.length>0?r.createElement(r.Fragment,null," ",t.length," "," "," ",r.createElement(i.HT,{text:"Résultats"})," "):r.createElement(i.HT,{text:"Aucun résultat"}))),r.createElement("ul",{className:"r-search-list"},t.map(((t,a)=>r.createElement("li",{key:a,className:"r-search-item"},r.createElement("a",{href:t._url},r.createElement("div",{className:"r-search-img"},t.has_leadimage[0]?r.createElement("div",{className:"r-search-img",style:{backgroundImage:"url("+t.image_url+")"}}):r.createElement("div",{className:"r-search-img no-search-item-img"})),r.createElement(h(),{highlightClassName:"r-search-highlighter",searchWords:[e.urlParams.SearchableText],textToHighlight:t.title})))))))},E=e=>{const[t,a]=(0,r.useState)([]),{response:n,error:l,isLoading:s}=(0,m.A)({method:"get",url:"",baseURL:e.url+"/@search?&b_size=100",headers:{Accept:"application/json"},params:e.urlParams.SearchableText||e.urlParams.iam||e.urlParams.topics?e.urlParams:{}},[e]);return(0,r.useEffect)((()=>{a(null!==n?n.items:[])}),[n]),r.createElement("div",{className:"search-web"},r.createElement("div",{className:"r-search-header"},r.createElement("h2",{className:"r-search-header-title"},r.createElement(i.HT,{text:"Infos pratiques"})),r.createElement("p",{className:"r-search-header-count"},t.length>0?r.createElement(r.Fragment,null," ",t.length," "," "," ",r.createElement(i.HT,{text:"Résultats"})," "):r.createElement(i.HT,{text:"Aucun résultat"}))),r.createElement("ul",{className:"r-search-list"},t.map(((t,a)=>r.createElement("li",{key:a,className:"r-search-item"},r.createElement("a",{href:t["@id"]},r.createElement(h(),{highlightClassName:"r-search-highlighter",searchWords:[e.urlParams.SearchableText],textToHighlight:t.title})))))))};var p=a(18874),b=a(48743);function N(e){return r.createElement(n.Kd,null,r.createElement(i.Kq,{language:e.currentLanguage,translation:b.A},r.createElement(T,{queryFilterUrl:e.queryFilterUrl,queryUrl:e.queryUrl,resultOption:JSON.parse(e.resultOption)})))}const T=e=>{const t=u.A.parse((0,p.A)().toString()),{SearchableText:a,iam:n,topics:l}=t,s={SearchableText:a,iam:n,topics:l},[c,i]=(0,r.useState)(s),[m,d]=(0,r.useState)(6);return r.createElement("div",{className:"ref"},r.createElement("div",{className:"r-search r-search-container"},r.createElement("div",{className:"row r-search-filters"},r.createElement(o,{url:e.queryUrl,activeFilter:c,onChange:e=>{i(e)}})),r.createElement("div",{className:"r-search-result"},r.createElement(E,{urlParams:c,url:e.queryUrl}),e.resultOption.news&&r.createElement(f,{urlParams:c,url:e.queryUrl}),e.resultOption.events&&r.createElement(v,{urlParams:c,url:e.queryUrl}),e.resultOption.directory&&r.createElement(g,{urlParams:c,url:e.queryUrl}))))}},86110:(e,t,a)=>{a.d(t,{A:()=>l});var r=a(25602),n=a(99938);const l=e=>{const[t,a]=(0,r.useState)(null),[l,s]=(0,r.useState)(""),[c,i]=(0,r.useState)(!0),[u,o]=(0,r.useState)(!1),m=new AbortController;return(0,r.useEffect)((()=>((async e=>{if(i(!0),e.load?o(!0):o(!1),0!=Object.keys(e.params).length)try{const t=await n.A.request(e);a(t.data),i(!1),s(null)}catch(e){s(e)}else a(null)})({...e,signal:m.signal}),()=>m.abort())),[e.params]),{response:t,error:l,isLoading:c,isMore:u}}},18874:(e,t,a)=>{a.d(t,{A:()=>n});var r=a(41665);const n=function(){return new URLSearchParams((0,r.zy)().search)}},48743:(e,t,a)=>{a.d(t,{A:()=>r});const r={Publié:{en:"Published",fr:"Publié",de:"Veröffentlicht",nl:"Gepubliceerd"},Actualisé:{en:"Updated",fr:"Actualisé",de:"Aktualisiert",nl:"Bijgewerkt"},Événements:{en:"Events",fr:"Événements",de:"Veranstaltungen",nl:"Evenementen"},Actualités:{en:"News",fr:"Actualités",de:"Nachrichten",nl:"Nieuws"},Contacts:{en:"Contacts",fr:"Contacts",de:"Kontakte",nl:"Contacten"},"Infos pratiques":{en:"Practical information",fr:"Infos pratiques",de:"Praktische Informationen",nl:"Praktische informatie"},"Chargement...":{en:"Loading",fr:"Chargement...",de:"Laden",nl:"Laden..."},Recherche:{en:"Search",fr:"Recherche",de:"Suche",nl:"Zoeken"},Thématiques:{en:"Themes",fr:"Thématiques",de:"Themen",nl:"Thema's"},"Je suis":{en:"I am",fr:"Je suis",de:"Ich bin",nl:"Ik ben"},Catégories:{en:"Categories",fr:"Catégories",de:"Kategorien",nl:"Categorieën"},Facilités:{en:"Facilities",fr:"Facilités",de:"Einrichtungen",nl:"Faciliteiten"},"Plus de résultats":{en:"More results",fr:"Plus de résultats",de:"Mehr Ergebnisse",nl:"Meer resultaten"},"Aucun résultat":{en:"No result",fr:"Aucun résultat",de:"Kein Ergebnis",nl:"Geen resultaat"},Résultats:{en:"Results",fr:"Résultats",de:"Ergebnisse",nl:"Resultaten"},Retour:{en:"Return",fr:"Retour",de:"Zurück",nl:"Terug"},Téléchargements:{en:"Downloads",fr:"Téléchargements",de:"Downloads",nl:"Downloads"},Billetterie:{en:"Ticketing",fr:"Billetterie",de:"Tickets",nl:"Ticketverkoop"},"Lien vers la vidéo":{en:"Link to video",fr:"Lien vers la vidéo",de:"Link zum Video",nl:"Link naar video"},"Participation en ligne":{en:"Join online",fr:"Participation en ligne",de:"Online teilnehmen",nl:"Doe online mee"},"Actualités trouvées":{en:" News found",fr:" Actualités trouvées",de:" Nachrichten gefunden",nl:" Nieuws gevonden"},"Actualité trouvée":{en:" News found",fr:" Actualité trouvée",de:" Nachricht gefunden",nl:" Nieuws gevonden"},"Aucune actualité n'a été trouvée":{en:"No news was found",fr:"Aucune actualité n'a été trouvée",de:"Keine Nachrichten gefunden",nl:"Geen nieuws gevonden"},"Proposer une actualité":{en:"Suggest a news",fr:"Proposer une actualité",de:"Nachricht vorschlagen",nl:"Nieuws voorstellen"},"événements trouvés":{en:" Events found",fr:" Événements trouvés",de:" Veranstaltungen gefunden",nl:" Evenementen gevonden"},"événement trouvé":{en:" Event found",fr:" Événement trouvé",de:" Veranstaltung gefunden",nl:" Evenement gevonden"},"Aucun événement n'a été trouvé":{en:"No event was found",fr:"Aucun événement n'a été trouvé",de:"Keine Veranstaltungen gefunden",nl:"Geen evenement gevonden"},"Proposer un événement":{en:"Suggest a event",fr:"Proposer un événement",de:"Veranstaltung vorschlagen",nl:"Evenement voorstellen"},"Infos pratiques":{en:"Practical information",fr:"Infos pratiques",de:"Praktische Informationen",nl:"Praktische informatie"},"Accessible aux PMR":{en:"Accessibility for PRM",fr:"Accessible aux PMR",de:"Barrierefreiheit für PMR",nl:"Toegankelijk voor PRM"},"Lien de l'événement":{en:"Event link",fr:"Lien de l'événement",de:"Veranstaltungslink",nl:"Evenement link"},"contacts trouvés":{en:" Contact found",fr:" Contacts trouvés",de:" Kontakt gefunden",nl:" Contact gevonden"},"contact trouvé":{en:" Contact found",fr:" Contact trouvé",de:" Kontakt gefunden",nl:" Contact gevonden"},"Aucun contact n'a été trouvé":{en:"No contact was found",fr:"Aucun contact n'a été trouvé",de:"Kein Kontakt gefunden",nl:"Geen contact gevonden"},"Proposer un contact":{en:"Suggest a contact",fr:"Proposer un contact",de:"Kontakt vorschlagen",nl:"Contact voorstellen"},"Toutes les dates":{en:"All dates",fr:"Toutes les dates",de:"Alle Daten",nl:"Alle data"},"Aujourd'hui":{en:"Today",fr:"Aujourd'hui",de:"Heute",nl:"Vandaag"},Demain:{en:"Tomorrow",fr:"Demain",de:"Morgen",nl:"Morgen"},"Ce week-end":{en:"This weekend",fr:"Ce week-end",de:"Dieses Wochenende",nl:"Dit weekend"},"Cette semaine":{en:"This week",fr:"Cette semaine",de:"Diese Woche",nl:"Deze week"},"Ce mois-ci":{en:"This month",fr:"Ce mois-ci",de:"Diesen Monat",nl:"Deze maand"},"Personnalisé (Du ... au ...)":{en:"Custom (From ... to ...)",fr:"Personnalisé (Du ... au ...)",de:"Benutzerdefiniert (Von ... bis ...)",nl:"Aangepast (Van ... tot ...)"},au:{en:"to",fr:"au",de:"bis",nl:"tot"},Personnalisé:{en:"Custom",fr:"Personnalisé",de:"Benutzerdefiniert",nl:"Aangepast"},Monday:{en:"Monday",fr:"Lundi",de:"Montag",nl:"Maandag"},Tuesday:{en:"Tuesday",fr:"Mardi",de:"Dienstag",nl:"Dinsdag"},Wednesday:{en:"Wednesday",fr:"Mercredi",de:"Mittwoch",nl:"Woensdag"},Thursday:{en:"Thursday",fr:"Jeudi",de:"Donnerstag",nl:"Donderdag"},Friday:{en:"Friday",fr:"Vendredi",de:"Freitag",nl:"Vrijdag"},Saturday:{en:"Saturday",fr:"Samedi",de:"Samstag",nl:"Zaterdag"},Sunday:{en:"Sunday",fr:"Dimanche",de:"Sonntag",nl:"Zondag"}}}}]);