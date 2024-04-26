(self.webpackChunkimio_smartweb_core_webcomponents=self.webpackChunkimio_smartweb_core_webcomponents||[]).push([[686],{69596:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>I});var a=n(25602),l=n(8174),r=n(41665),s=n(19154),c=n(86110),i=n(83198),o=n(54368),m=n.n(o),u=(n(55369),n(60711)),d=n.n(u),v=n(2494),f=n(57377),h=n(96745),g=n(42090),p=n(31540),E=n(64478);const j={fr:h.fr,nl:g.nl,de:p.de,en:E.b};const w=function(e){let{language:t,setDates:n}=e;const[l,r]=(0,a.useState)([null,null]),[s,c]=l,[o,u]=(0,a.useState)("Période"),[h,g]=(0,a.useState)(),p=d()().format("YYYY-MM-DD"),E={all:a.createElement(i.HT,{text:"Toutes les dates"}),today:a.createElement(i.HT,{text:"Aujourd'hui"}),tomorrow:a.createElement(i.HT,{text:"Demain"}),thisWeekEnd:a.createElement(i.HT,{text:"Ce week-end"}),thisWeek:a.createElement(i.HT,{text:"Cette semaine"}),thisMonth:a.createElement(i.HT,{text:"Ce mois-ci"}),custom:a.createElement(i.HT,{text:"Personnalisé (Du ... au ...)"})};return(0,a.useState)((()=>{g(j[t])}),[]),a.createElement(a.Fragment,null,a.createElement("div",{className:"period-filter"},a.createElement(v.A,{className:"period-filter-toggler",onSelect:e=>{switch(e){case"all":n({"event_dates.query":[p]}),u(E.all);break;case"today":n({"event_dates.query":[p,p]}),u(E.today);break;case"tomorrow":const e=d()().add(1,"days").format("YYYY-MM-DD");n({"event_dates.query":[e,e]}),u(E.tomorrow);break;case"thisWeekEnd":const t=d()().endOf("week").format("YYYY-MM-DD"),a=d()().endOf("week").add(1,"days").format("YYYY-MM-DD");n({"event_dates.query":[t,a]}),u(E.thisWeekEnd);break;case"thisWeek":const l=d()().endOf("week").add(1,"days").format("YYYY-MM-DD");n({"event_dates.query":[p,l]}),u(E.thisWeek);break;case"thisMonth":const r=d()().endOf("month").format("YYYY-MM-DD");n({"event_dates.query":[p,r]}),u(E.thisMonth)}},title:o},a.createElement(f.A.Item,{eventKey:"all"},E.all),a.createElement(f.A.Item,{eventKey:"today"},E.today),a.createElement(f.A.Item,{eventKey:"tomorrow"},E.tomorrow),a.createElement(f.A.Item,{eventKey:"thisWeekEnd"},E.thisWeekEnd),a.createElement(f.A.Item,{eventKey:"thisWeek"},E.thisWeek),a.createElement(f.A.Item,{eventKey:"thisMonth"},E.thisMonth),a.createElement("div",{className:"perdiod-filter-range"},h&&a.createElement(i.rk,null,(e=>{let{translate:t,language:l}=e;return a.createElement(m(),{dateFormat:"dd/MM/yyyy",placeholderText:t({text:"Personnalisé (Du ... au ...)"}),selectsRange:!0,startDate:s,endDate:c,minDate:(new Date).setDate((new Date).getDate()+1),onChange:e=>{r(e),(null!==e[0]&&null!==e[1]||null==e[0]&&null==e[1])&&(e=>{r(e);const t=e.filter((e=>null!==e)).map((e=>d()(e).format("YYYY-MM-DD")));n({"event_dates.query":t}),e.every((e=>null===e))?u(E.all):u(E.custom)})(e)},isClearable:!0,locale:h})}))))))};var y=n(72668);const k=function(e){let t=(0,r.Zp)();const[n,l]=(0,a.useState)(e.activeFilter),[o,m]=(0,a.useState)(null),[u,v]=(0,a.useState)(null),[f,h]=(0,a.useState)(null),{response:g,error:p,isLoading:E}=(0,c.A)({method:"get",url:"",baseURL:e.url,headers:{Accept:"application/json"},params:n,paramsSerializer:{indexes:null}});(0,a.useEffect)((()=>{if(null!==g){const e=g.topics&&g.topics.map((e=>({value:e.token,label:e.title}))),t=g.category&&g.category.map((e=>({value:e.token,label:e.title})));m(e),v(t)}}),[g]);const j=(0,a.useCallback)((e=>{let{target:{name:t,value:n}}=e;n.length>2?l((e=>({...e,[t]:n})),[]):l((e=>{const n={...e},{[t]:a,...l}=n;return l}))})),k=(0,a.useCallback)(((e,t)=>{const n=t.name;e?l((t=>({...t,[n]:e.value})),[]):l((e=>{const t={...e},{[n]:a,...l}=t;return l}))})),b=(0,a.useRef)(!0);(0,a.useEffect)((()=>{b.current?b.current=!1:(t({pathname:"./",search:y.A.stringify(n)}),e.onChange(n))}),[n]);let N=o&&o.filter((t=>t.value===e.activeFilter.topics)),x=u&&u.filter((t=>t.value===e.activeFilter.category));const A={control:e=>({...e,backgroundColor:"white",borderRadius:"0",height:"50px"}),placeholder:e=>({...e,color:"000",fontWeight:"bold",fontSize:"12px",textTransform:"uppercase",letterSpacing:"1.2px"}),option:(e,t)=>{let{data:n,isDisabled:a,isFocused:l,isSelected:r}=t;return{...e}}};return(0,a.useEffect)((()=>{f&&l((e=>{if(f["event_dates.query"].length>1){const{"event_dates.range":t,...n}=f,a="min:max";return{...e,...n,"event_dates.range":a}}return f["event_dates.query"].every((e=>null===e))?{...e,"event_dates.query":[d()().format("YYYY-MM-DD")],"event_dates.range":"min"}:{...e,...f,"event_dates.range":"min"}}))}),[f]),a.createElement(a.Fragment,null,a.createElement("form",{className:"r-filter",onSubmit:function(t){t.preventDefault(),e.onChange(n)}},a.createElement("div",{className:"r-filter-search"},a.createElement(i.rk,null,(e=>{let{translate:t}=e;return a.createElement("input",{className:"input-custom-class",name:"SearchableText",type:"text",value:n.SearchableText,onChange:j,placeholder:t({text:"Recherche"})})})),a.createElement("button",{type:"submit"}))),a.createElement("div",{className:"r-filter topics-Filter"},a.createElement(i.rk,null,(e=>{let{translate:t}=e;return a.createElement(s.Ay,{styles:A,name:"topics",className:"select-custom-class library-topics",isClearable:!0,onChange:k,options:o&&o,placeholder:t({text:"Thématiques"}),value:N&&N[0]})}))),a.createElement("div",{className:"r-filter  facilities-Filter"},a.createElement(i.rk,null,(e=>{let{translate:t}=e;return a.createElement(s.Ay,{styles:A,name:"category",className:"select-custom-class library-facilities",isClearable:!0,onChange:k,options:u&&u,placeholder:t({text:"Catégories"}),value:x&&x[0]})}))),"False"===e.onlyPastEvents&&a.createElement("div",{className:"r-filter  schedul-Filter"},a.createElement(w,{language:e.language,setDates:h})))};var b=n(18874),N=n(91015);n(1053);const x=e=>{let{queryUrl:t,onChange:n}=e,l=(0,r.Zp)();const{u:s,...o}=Object.assign({UID:y.A.parse((0,b.A)().toString()).u,fullobjects:1}),[m,u]=(0,a.useState)(o),[v,f]=(0,a.useState)({}),[h,g]=(0,a.useState)(),[p,E]=(0,a.useState)(),{response:j,error:w,isLoading:k}=(0,c.A)({method:"get",url:"",baseURL:t,headers:{Accept:"application/json"},params:m},[]);(0,a.useEffect)((()=>{u(o)}),[y.A.parse((0,b.A)().toString()).u]),(0,a.useEffect)((()=>{null!==j&&f(j.items[0]),window.scrollTo(0,0)}),[j]),(0,a.useEffect)((()=>{v.items&&v.items.length>0&&(g(v.items.filter((e=>"File"===e["@type"]))),E(v.items.filter((e=>"Image"===e["@type"]))))}),[v]),d().locale("be");const x=d().utc(v.start).format("DD-MM-YYYY"),A=d().utc(v.end).format("DD-MM-YYYY"),_=d().utc(v.start).format("LT"),D=d().utc(v.end).format("LT");let M="https://www.google.com/maps/dir/?api=1&destination="+v.street+"+"+v.number+"+"+v.complement+"+"+v.zipcode+"+"+v.city;return M=M.replaceAll("+null",""),a.createElement("div",{className:"envent-content r-content"},a.createElement("button",{type:"button",onClick:function(){l(".."),n(null)}},a.createElement(i.HT,{text:"Retour"})),a.createElement("article",null,a.createElement("header",null,a.createElement("h2",{className:"r-content-title"},v.title)),a.createElement("figure",null,a.createElement("div",{className:"r-content-img",style:{backgroundImage:v.image_affiche_scale?"url("+v.image_affiche_scale+")":""}})),a.createElement("span",{className:"news-info-title"},a.createElement(i.HT,{text:"Infos pratiques"})),a.createElement("div",{className:"r-content-news-info"},a.createElement("div",{className:"r-content-news-info-container"},a.createElement("div",{className:"r-content-news-info-schedul"},a.createElement("div",{className:"icon-baseline"},a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",preserveAspectRatio:"xMinYMin",viewBox:"0 0 19.41 19.41"},a.createElement("path",{d:"M16.09,2.74H14.35V.85a.44.44,0,0,0-.43-.44H12.47A.44.44,0,0,0,12,.85V2.74H7.38V.85A.44.44,0,0,0,7,.41H5.5a.44.44,0,0,0-.44.44V2.74H3.32A1.74,1.74,0,0,0,1.58,4.48V17.26A1.74,1.74,0,0,0,3.32,19H16.09a1.74,1.74,0,0,0,1.75-1.74V4.48A1.74,1.74,0,0,0,16.09,2.74Zm-.21,14.52H3.54A.22.22,0,0,1,3.32,17h0V6.22H16.09V17a.21.21,0,0,1-.21.22Z"}))),a.createElement("div",{className:"dpinlb"},a.createElement("div",{className:"r-content-news-info--date"},x===A?a.createElement("div",null,v.whole_day?a.createElement("div",{className:"r-content-date-start"},a.createElement("span",null,"Le "),a.createElement("div",{className:"r-time"},x)):v.open_end?a.createElement(a.Fragment,null,a.createElement("div",{className:"r-content-date-one-day"},a.createElement("div",{className:"r-content-date-start"},a.createElement("span",null,"Le "),a.createElement("div",{className:"r-time"},x),a.createElement("span",null," à "),a.createElement("div",{className:"r-time-hours"},_)))):a.createElement(a.Fragment,null,a.createElement("div",{className:"r-content-date-one-day"},a.createElement("div",{className:"r-content-date-start"},a.createElement("span",null,"Le "),a.createElement("div",{className:"r-time"},x)),a.createElement("div",{className:"r-content-date-start-hours"},a.createElement("span",null,"de "),a.createElement("div",{className:"r-time-hours"},_),a.createElement("span",null," à "),a.createElement("div",{className:"r-time-hours"},D))))):a.createElement("div",{className:"r-content-date-du-au"},a.createElement("div",{className:"r-content-date-start"},a.createElement("span",null,"Du "),a.createElement("div",{className:"r-time"},x)),a.createElement("div",{className:"r-content-date-end"},a.createElement("span",null," au "),a.createElement("div",{className:"r-time"},A)))))),a.createElement("div",{className:"r-content-news-info-aera"},v.street?a.createElement("div",{className:"icon-baseline"},a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},a.createElement("path",{d:"M9,18.34C3.9,10.94,3,10.18,3,7.45a6.75,6.75,0,0,1,13.49,0c0,2.73-.94,3.49-6,10.89a.85.85,0,0,1-1.17.22A.77.77,0,0,1,9,18.34Zm.7-8.07A2.82,2.82,0,1,0,6.89,7.45a2.83,2.83,0,0,0,2.82,2.82Z"}))):"",a.createElement("div",{className:"dpinlb"},a.createElement("div",{className:"r-content-news-info--itinirary"},v.street?a.createElement("a",{href:M,target:"_blank"},a.createElement("span",null,"Itinéraire")):""),!0===v.reduced_mobility_facilities?a.createElement("div",{className:"r-content-news-info--reduced"},a.createElement("span",null,a.createElement(i.HT,{text:"Accessible aux PMR"}))):"")),a.createElement("div",{className:"r-content-news-info-contact"},a.createElement("div",{className:"dpinlb"},a.createElement("div",{className:"r-content-news-info--name"},a.createElement("span",null,v.contact_name)),a.createElement("div",{className:"r-content-news-info--phone"},a.createElement("span",null,a.createElement("a",{href:"tel:".concat(v.contact_phone)},v.contact_phone))),a.createElement("div",{className:"r-content-news-info--email"},a.createElement("a",{href:"mailto:".concat(v.contact_email)},v.contact_email)))),null===v.event_url&&null===v.online_participation&&null===v.video_url?"":a.createElement("div",{className:"r-content-news-info-link"},a.createElement("div",{className:"icon-baseline"},a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},a.createElement("path",{d:"M16.36,2.22H3.06a1.3,1.3,0,0,0-1.3,1.3h0v9a1.3,1.3,0,0,0,1.3,1.3H7.52v1.74h-.7a.8.8,0,0,0,0,1.6h5.79a.8.8,0,0,0,0-1.6h-.7V13.85h4.45a1.31,1.31,0,0,0,1.3-1.3v-9A1.3,1.3,0,0,0,16.36,2.22Zm-1.9,10.83a.37.37,0,1,1,.36-.37h0a.36.36,0,0,1-.36.36Zm1.6.08a.45.45,0,1,1,.44-.45h0a.44.44,0,0,1-.44.45h0Zm.53-1.35H2.82V3.52a.23.23,0,0,1,.23-.23H16.36a.23.23,0,0,1,.23.23h0v8.27Z"}))),a.createElement("div",{className:"dpinlb"},null===v.event_url?"":a.createElement("div",{className:"r-content-news-info-event_link"},a.createElement("a",{href:v.event_url},a.createElement(i.HT,{text:"Lien de l'événement"}))),null===v.online_participation?"":a.createElement("div",{className:"r-content-news-info--online_participation"},a.createElement("a",{href:v.online_participation},a.createElement(i.HT,{text:"Participation en ligne"}))),null===v.video_url?"":a.createElement("div",{className:"r-content-news-info--video"},a.createElement("a",{href:v.video_url},a.createElement(i.HT,{text:"Lien vers la vidéo"}))))),null===v.facebook&&null===v.instagram&&null===v.twitter?"":a.createElement("div",{className:"r-content-news-info-social"},a.createElement("ul",null,v.facebook?a.createElement("li",null,a.createElement("a",{href:v.facebook,target:"_blank"},a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-204.79995 -341.33325 1774.9329 2047.9995"},a.createElement("path",{d:"M1365.333 682.667C1365.333 305.64 1059.693 0 682.667 0 305.64 0 0 305.64 0 682.667c0 340.738 249.641 623.16 576 674.373V880H402.667V682.667H576v-150.4c0-171.094 101.917-265.6 257.853-265.6 74.69 0 152.814 13.333 152.814 13.333v168h-86.083c-84.804 0-111.25 52.623-111.25 106.61v128.057h189.333L948.4 880H789.333v477.04c326.359-51.213 576-333.635 576-674.373",fill:"#100f0d"}),a.createElement("path",{d:"M948.4 880l30.267-197.333H789.333V554.609C789.333 500.623 815.78 448 900.584 448h86.083V280s-78.124-13.333-152.814-13.333c-155.936 0-257.853 94.506-257.853 265.6v150.4H402.667V880H576v477.04a687.805 687.805 0 00106.667 8.293c36.288 0 71.91-2.84 106.666-8.293V880H948.4",fill:"#fff"})))):"",v.instagram?a.createElement("li",null,a.createElement("a",{href:v.instagram,target:"_blank"},a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-100.7682 -167.947 873.3244 1007.682"},a.createElement("g",{fill:"#100f0d"},a.createElement("path",{d:"M335.895 0c-91.224 0-102.663.387-138.49 2.021-35.752 1.631-60.169 7.31-81.535 15.612-22.088 8.584-40.82 20.07-59.493 38.743-18.674 18.673-30.16 37.407-38.743 59.495C9.33 137.236 3.653 161.653 2.02 197.405.386 233.232 0 244.671 0 335.895c0 91.222.386 102.661 2.02 138.488 1.633 35.752 7.31 60.169 15.614 81.534 8.584 22.088 20.07 40.82 38.743 59.495 18.674 18.673 37.405 30.159 59.493 38.743 21.366 8.302 45.783 13.98 81.535 15.612 35.827 1.634 47.266 2.021 138.49 2.021 91.222 0 102.661-.387 138.488-2.021 35.752-1.631 60.169-7.31 81.534-15.612 22.088-8.584 40.82-20.07 59.495-38.743 18.673-18.675 30.159-37.407 38.743-59.495 8.302-21.365 13.981-45.782 15.612-81.534 1.634-35.827 2.021-47.266 2.021-138.488 0-91.224-.387-102.663-2.021-138.49-1.631-35.752-7.31-60.169-15.612-81.534-8.584-22.088-20.07-40.822-38.743-59.495-18.675-18.673-37.407-30.159-59.495-38.743-21.365-8.302-45.782-13.981-81.534-15.612C438.556.387 427.117 0 335.895 0zm0 60.521c89.686 0 100.31.343 135.729 1.959 32.75 1.493 50.535 6.965 62.37 11.565 15.68 6.094 26.869 13.372 38.622 25.126 11.755 11.754 19.033 22.944 25.127 38.622 4.6 11.836 10.072 29.622 11.565 62.371 1.616 35.419 1.959 46.043 1.959 135.73 0 89.687-.343 100.311-1.959 135.73-1.493 32.75-6.965 50.535-11.565 62.37-6.094 15.68-13.372 26.869-25.127 38.622-11.753 11.755-22.943 19.033-38.621 25.127-11.836 4.6-29.622 10.072-62.371 11.565-35.413 1.616-46.036 1.959-135.73 1.959-89.694 0-100.315-.343-135.73-1.96-32.75-1.492-50.535-6.964-62.37-11.564-15.68-6.094-26.869-13.372-38.622-25.127-11.754-11.753-19.033-22.943-25.127-38.621-4.6-11.836-10.071-29.622-11.565-62.371-1.616-35.419-1.959-46.043-1.959-135.73 0-89.687.343-100.311 1.959-135.73 1.494-32.75 6.965-50.535 11.565-62.37 6.094-15.68 13.373-26.869 25.126-38.622 11.754-11.755 22.944-19.033 38.622-25.127 11.836-4.6 29.622-10.072 62.371-11.565 35.419-1.616 46.043-1.959 135.73-1.959"}),a.createElement("path",{d:"M335.895 447.859c-61.838 0-111.966-50.128-111.966-111.964 0-61.838 50.128-111.966 111.966-111.966 61.836 0 111.964 50.128 111.964 111.966 0 61.836-50.128 111.964-111.964 111.964zm0-284.451c-95.263 0-172.487 77.224-172.487 172.487 0 95.261 77.224 172.485 172.487 172.485 95.261 0 172.485-77.224 172.485-172.485 0-95.263-77.224-172.487-172.485-172.487m219.608-6.815c0 22.262-18.047 40.307-40.308 40.307-22.26 0-40.307-18.045-40.307-40.307 0-22.261 18.047-40.308 40.307-40.308 22.261 0 40.308 18.047 40.308 40.308"}))))):"",v.twitter?a.createElement("li",null,a.createElement("a",{href:v.twitter,target:"_blank"},a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",height:"800",width:"1200",viewBox:"-44.7006 -60.54775 387.4052 363.2865"},a.createElement("path",{fill:"#000",d:"M93.719 242.19c112.46 0 173.96-93.168 173.96-173.96 0-2.646-.054-5.28-.173-7.903a124.338 124.338 0 0030.498-31.66c-10.955 4.87-22.744 8.148-35.11 9.626 12.622-7.57 22.313-19.543 26.885-33.817a122.62 122.62 0 01-38.824 14.841C239.798 7.433 223.915 0 206.326 0c-33.764 0-61.144 27.381-61.144 61.132 0 4.798.537 9.465 1.586 13.941-50.815-2.557-95.874-26.886-126.03-63.88a60.977 60.977 0 00-8.279 30.73c0 21.212 10.794 39.938 27.208 50.893a60.685 60.685 0 01-27.69-7.647c-.009.257-.009.507-.009.781 0 29.61 21.075 54.332 49.051 59.934a61.218 61.218 0 01-16.122 2.152 60.84 60.84 0 01-11.491-1.103c7.784 24.293 30.355 41.971 57.115 42.465-20.926 16.402-47.287 26.171-75.937 26.171-4.929 0-9.798-.28-14.584-.846 27.059 17.344 59.189 27.464 93.722 27.464"})))):""))),a.createElement("div",{className:"r-content-news-info-action"},v.ticket_url?a.createElement("div",{className:"r-content-booking"},a.createElement("a",{href:v.ticket_url},a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 19.41 19.41"},a.createElement("circle",{cx:"13.03",cy:"14.61",r:"0.63",fill:"fill:#fff"}),a.createElement("circle",{cx:"11.59",cy:"6.52",r:"0.63",fill:"fill:#fff"}),a.createElement("path",{d:"M17.11,11.47h.62V7.71h-1.6a1.25,1.25,0,0,1-1.25-1.25,1.27,1.27,0,0,1,.67-1.12l.54-.28-1.6-3.39-12.8,6h0v3.76h.63a1.26,1.26,0,0,1,0,2.51H1.68v3.76H17.73V14h-.62a1.26,1.26,0,1,1,0-2.51Zm-6.9-6.4a.63.63,0,0,0,1.14-.53l2.54-1.2.58,1.23A2.52,2.52,0,0,0,14,7.71H4.63Zm6.27,10.08v1.34H13.66a.63.63,0,1,0-1.26,0H2.93V15.16a2.51,2.51,0,0,0,0-4.86V9H12.4a.63.63,0,0,0,1.26,0h2.82V10.3a2.51,2.51,0,0,0,0,4.86Z",fill:"fill:#fff"}),a.createElement("circle",{cx:"13.03",cy:"10.85",r:"0.63",fill:"fill:#fff"}),a.createElement("circle",{cx:"13.03",cy:"12.73",r:"0.63",fill:"fill:#fff"})),a.createElement(i.HT,{text:"Billetterie"}))):"")),a.createElement("div",{className:"r-content-description"},a.createElement(N.o,null,v.description)),a.createElement("div",{className:"r-content-text",dangerouslySetInnerHTML:{__html:v.text&&v.text.data}}),h&&a.createElement("div",{className:"r-content-files"},h.map(((e,t)=>a.createElement("div",{key:t,className:"r-content-file"},a.createElement("a",{href:e.targetUrl,className:"r-content-file-link",rel:"nofollow"},a.createElement("span",{className:"r-content-file-title"},e.title),a.createElement("span",{className:"r-content-file-icon"},a.createElement("svg",{width:"21",height:"21",viewBox:"0 0 24 24",fill:"none",stroke:"#8899a4","stroke-width":"2","stroke-linecap":"square","stroke-linejoin":"arcs"},a.createElement("path",{d:"M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"}))," ")))))),p&&a.createElement("div",{className:"r-content-gallery"},a.createElement("div",{className:"spotlight-group flexbin r-content-gallery"},p.map(((e,t)=>a.createElement("a",{key:t,className:"spotlight",href:e.image_full_scale},a.createElement("img",{src:e.image_preview_scale,alt:""}))))))))};var A=n(29442),_=n.n(A);const D=e=>{let{item:t}=e;const n=t.title&&t.title,l=(t.taxonomy_contact_category&&t.taxonomy_contact_category[0],d()(t.start&&t.start));t.number&&t.number,t.street&&t.street,t.complement&&t.complement,t.zipcode&&t.zipcode,t.city&&t.city,t.country&&t.country,t.phones&&t.phones,t.mails&&t.mails,t.topics&&t.topics;return a.createElement("div",{className:"r-list-item"},a.createElement("div",{className:t.image_vignette_scale?"r-item-img":"r-item-img r-item-img-placeholder",style:{backgroundImage:t.image_vignette_scale?"url("+t.image_vignette_scale+")":""}}),a.createElement("div",{className:"r-item-text"},l&&a.createElement("span",{className:"r-item-date"},a.createElement(_(),{format:"DD-MM-YYYY"},l)),a.createElement("span",{className:"r-item-title"},n),t.category&&a.createElement("span",{className:"r-item-categorie"},t.category.title)))};var M=n(75681),C=n.n(M);const H=e=>{let{itemsArray:t,onChange:n,onHover:r,parentCallback:s}=e;function c(e){r(e)}return a.createElement(a.Fragment,null,a.createElement("ul",{className:"r-result-list event-result-list"},t.map(((e,t)=>a.createElement("li",{key:t,className:"r-list-item-group",onMouseEnter:()=>c(e.UID),onMouseLeave:()=>c(null),onClick:()=>{return t=e.UID,void n(t);var t}},a.createElement(l.N_,{className:"r-list-item-link",style:{textDecoration:"none"},to:{pathname:"/"+C()(e.title).replace(/[^a-zA-Z ]/g,"").replace(/\s/g,"-").toLowerCase(),search:"?u=".concat(e.UID),state:{idItem:e.UID}}}),a.createElement(D,{item:e,key:e.created}))))))};var T=n(81499),S=n(48743);function I(e){return a.createElement(l.Kd,{basename:e.viewPath},a.createElement(i.Kq,{language:e.currentLanguage,translation:S.A},a.createElement(z,{queryFilterUrl:e.queryFilterUrl,queryUrl:e.queryUrl,proposeUrl:e.proposeUrl,batchSize:e.batchSize,displayMap:e.displayMap,onlyPastEvents:e.onlyPastEvents,language:e.currentLanguage})))}function z(e){const{u:t,...n}=Object.assign({b_start:0,fullobjects:1,"event_dates.query":[d()().format("YYYY-MM-DD")],"event_dates.range":"True"===e.onlyPastEvents?"max":"min"},y.A.parse((0,b.A)().toString())),[l,s]=(0,a.useState)([]),[o,m]=(0,a.useState)([]),[u,v]=(0,a.useState)(null),[f,h]=(0,a.useState)(null),[g,p]=(0,a.useState)(n),[E,j]=(0,a.useState)(0),[w,N]=(0,a.useState)(!1),A="True"===e.displayMap,{response:_,error:D,isLoading:M,isMore:C}=(0,c.A)({method:"get",url:"",baseURL:e.queryUrl,headers:{Accept:"application/json"},params:g,paramsSerializer:{indexes:null},load:w},[]);(0,a.useEffect)((()=>{null!==_&&(s(C?e=>[...e,..._.items]:_.items),m(_.items_total))}),[_]);const S=e=>{v(e)},I=e=>{h(e)};(0,a.useEffect)((()=>{p((e=>({...e,b_start:E})))}),[E]);let z=document.getElementById("portal-header").offsetHeight;const Y=(0,a.useRef)(),[P,U]=a.useState({height:0});let L,q;(0,a.useEffect)((()=>{U({height:Y.current.clientHeight})}),[Y.current]),l&&l.length>0?(L=a.createElement(H,{onChange:S,itemsArray:l,onHover:I}),q=a.createElement(T.A,{headerHeight:P.height+z,clickId:u,hoverId:f,items:l,queryUrl:e.queryUrl})):M||(L=a.createElement("p",null,a.createElement(i.HT,{text:"Aucun événement n'a été trouvé"})));const V=a.createElement("div",{className:"lds-roller-container"},a.createElement("div",{className:"lds-roller"},a.createElement("div",null),a.createElement("div",null),a.createElement("div",null),a.createElement("div",null),a.createElement("div",null),a.createElement("div",null),a.createElement("div",null),a.createElement("div",null)));return a.createElement("div",{className:"ref ".concat(A?"view-map":"no-map")},a.createElement("div",{className:"r-result-filter-container",ref:Y,style:{top:z}},a.createElement("div",{id:"r-result-filter",className:"r-result-filter container annuaire-result-filter"},a.createElement(k,{url:e.queryFilterUrl,activeFilter:g,onChange:e=>{N(!1),j((()=>0)),p(e),window.scrollTo(0,0)},language:e.language,onlyPastEvents:e.onlyPastEvents}),e.proposeUrl&&a.createElement("div",{className:"r-add-event"},a.createElement("a",{target:"_blank",href:e.proposeUrl},a.createElement(i.HT,{text:"Proposer un événement"}))),o>0?a.createElement("p",{className:"r-results-numbers"},a.createElement("span",null,o),o>1?a.createElement(i.HT,{text:"événements trouvés"}):a.createElement(i.HT,{text:"événement trouvé"})):a.createElement("p",{className:"r-results-numbers"},a.createElement(i.HT,{text:"Aucun résultat"})))),a.createElement(r.BV,null,a.createElement(r.qh,{exact:!0,path:"/",element:a.createElement("div",{className:"r-wrapper container r-annuaire-wrapper"},a.createElement("div",{className:"r-result r-annuaire-result"},a.createElement("div",null,L),a.createElement("div",{className:"r-load-more"},o-e.batchSize>E?a.createElement("div",null,a.createElement("span",{className:"no-more-result"},M?V:""),a.createElement("button",{onClick:()=>{j((t=>t+parseInt(e.batchSize))),N(!0)},className:"btn-grad"},M?a.createElement(i.HT,{text:"Chargement..."}):a.createElement(i.HT,{text:"Plus de résultats"}))):a.createElement("span",{className:"no-more-result"},M?V:""))),A&&a.createElement("div",{className:"r-map annuaire-map",style:{top:P.height+z,height:"calc(100vh-"+P.height+z}},q))}),a.createElement(r.qh,{path:"/:name",element:a.createElement("div",{className:"r-wrapper container r-annuaire-wrapper"},a.createElement("div",{className:"r-result r-annuaire-result"},a.createElement(x,{queryUrl:e.queryUrl,onChange:S})),A&&a.createElement("div",{className:"r-map annuaire-map",style:{top:P.height+z,height:"calc(100vh-"+P.height+z}},q))})))}},86110:(e,t,n)=>{"use strict";n.d(t,{A:()=>r});var a=n(25602),l=n(99938);const r=e=>{const[t,n]=(0,a.useState)(null),[r,s]=(0,a.useState)(""),[c,i]=(0,a.useState)(!0),[o,m]=(0,a.useState)(!1),u=new AbortController;return(0,a.useEffect)((()=>((async e=>{if(i(!0),e.load?m(!0):m(!1),0!=Object.keys(e.params).length)try{const t=await l.A.request(e);n(t.data),i(!1),s(null)}catch(e){s(e)}else n(null)})({...e,signal:u.signal}),()=>u.abort())),[e.params]),{response:t,error:r,isLoading:c,isMore:o}}},18874:(e,t,n)=>{"use strict";n.d(t,{A:()=>l});var a=n(41665);const l=function(){return new URLSearchParams((0,a.zy)().search)}},81499:(e,t,n)=>{"use strict";n.d(t,{A:()=>j});var a=n(25602),l=n(28009),r=n(77059),s=n(60055),c=n(69780),i=n(16545),o=n(18874),m=n(97284),u=n.n(m);const d=n.p+"assets/pin-react.fda934b5daf26dd4da2a71a7e7e44431.svg";const v=n.p+"assets/pin-react-active.07d154037a15be5525b823fdc626cf29.svg";var f=n(8174),h=n(75681),g=n.n(h),p=n(72668);function E(e){let{activeItem:t,arrayOfLatLngs:n}=e;const a=(0,l.ko)();if(t){const e=[];e.push(t.geolocation.latitude),e.push(t.geolocation.longitude),a.setView(e,15)}else{let e=new(u().LatLngBounds)(n);a.fitBounds(e)}return null}const j=function(e){const[t,n]=(0,a.useState)(null),[l,m]=(0,a.useState)([]),[h,j]=(0,a.useState)(null),{u:w,...y}=Object.assign({UID:p.A.parse((0,o.A)().toString()).u});(0,a.useEffect)((()=>{const t=e.items.filter((e=>e.geolocation.latitude&&50.4989185!==e.geolocation.latitude&&4.7184485!==e.geolocation.longitude));m(t)}),[e]);const k=e=>new(u().Icon)({iconUrl:e,iconSize:[29,37]}),b=t=>t===e.clickId||t===e.hoverId?999:1;(0,a.useEffect)((()=>{var e=l&&l.filter((e=>e.UID===y.UID));n(e[0])}),[l]),(0,a.useEffect)((()=>{if(l.length>0){let e=[];l.map(((t,n)=>{let a=t.geolocation.latitude,l=t.geolocation.longitude;e.push([a,l])})),j(e)}}),[l]);const N=l.map((t=>{return a.createElement(r.p,{key:t.UID,icon:(n=t.UID,n===y.UID||n===e.hoverId?k(v):k(d)),zIndexOffset:b(t.UID),position:[t.geolocation?t.geolocation.latitude:"",t.geolocation?t.geolocation.longitude:""],eventHandlers:{mouseover:e=>{}}},a.createElement(s.z,{closeButton:!1},a.createElement(f.N_,{className:"r-map-popup",style:{textDecoration:"none"},to:{pathname:"/"+g()(t.title).replace(/[^a-zA-Z ]/g,"").replace(/\s/g,"-").toLowerCase(),search:"?u=".concat(t.UID),state:{idItem:t.UID}}},a.createElement("span",{className:"r-map-popup-title"},t.title),a.createElement("p",{className:"r-map-popup-category"},t.category&&t.category.title))));var n}));return a.createElement("div",null,a.createElement(c.W,{style:{height:"calc(100vh - ".concat(e.headerHeight,"px)"),minHeight:"600px"},center:[50.85034,4.35171],zoom:15},a.createElement(i.e,{attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',url:"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"}),null!=h?a.createElement(E,{activeItem:t,activeItemUID:y.UID,arrayOfLatLngs:h&&h}):"",l&&N))}},48743:(e,t,n)=>{"use strict";n.d(t,{A:()=>a});const a={Publié:{en:"Published",fr:"Publié",de:"Veröffentlicht",nl:"Gepubliceerd"},Actualisé:{en:"Updated",fr:"Actualisé",de:"Aktualisiert",nl:"Bijgewerkt"},Événements:{en:"Events",fr:"Événements",de:"Veranstaltungen",nl:"Evenementen"},Actualités:{en:"News",fr:"Actualités",de:"Nachrichten",nl:"Nieuws"},Contacts:{en:"Contacts",fr:"Contacts",de:"Kontakte",nl:"Contacten"},"Infos pratiques":{en:"Practical information",fr:"Infos pratiques",de:"Praktische Informationen",nl:"Praktische informatie"},"Chargement...":{en:"Loading",fr:"Chargement...",de:"Laden",nl:"Laden..."},Recherche:{en:"Search",fr:"Recherche",de:"Suche",nl:"Zoeken"},Thématiques:{en:"Themes",fr:"Thématiques",de:"Themen",nl:"Thema's"},"Je suis":{en:"I am",fr:"Je suis",de:"Ich bin",nl:"Ik ben"},Catégories:{en:"Categories",fr:"Catégories",de:"Kategorien",nl:"Categorieën"},Facilités:{en:"Facilities",fr:"Facilités",de:"Einrichtungen",nl:"Faciliteiten"},"Plus de résultats":{en:"More results",fr:"Plus de résultats",de:"Mehr Ergebnisse",nl:"Meer resultaten"},"Aucun résultat":{en:"No result",fr:"Aucun résultat",de:"Kein Ergebnis",nl:"Geen resultaat"},Résultats:{en:"Results",fr:"Résultats",de:"Ergebnisse",nl:"Resultaten"},Retour:{en:"Return",fr:"Retour",de:"Zurück",nl:"Terug"},Téléchargements:{en:"Downloads",fr:"Téléchargements",de:"Downloads",nl:"Downloads"},Billetterie:{en:"Ticketing",fr:"Billetterie",de:"Tickets",nl:"Ticketverkoop"},"Lien vers la vidéo":{en:"Link to video",fr:"Lien vers la vidéo",de:"Link zum Video",nl:"Link naar video"},"Participation en ligne":{en:"Join online",fr:"Participation en ligne",de:"Online teilnehmen",nl:"Doe online mee"},"Actualités trouvées":{en:" News found",fr:" Actualités trouvées",de:" Nachrichten gefunden",nl:" Nieuws gevonden"},"Actualité trouvée":{en:" News found",fr:" Actualité trouvée",de:" Nachricht gefunden",nl:" Nieuws gevonden"},"Aucune actualité n'a été trouvée":{en:"No news was found",fr:"Aucune actualité n'a été trouvée",de:"Keine Nachrichten gefunden",nl:"Geen nieuws gevonden"},"Proposer une actualité":{en:"Suggest a news",fr:"Proposer une actualité",de:"Nachricht vorschlagen",nl:"Nieuws voorstellen"},"événements trouvés":{en:" Events found",fr:" Événements trouvés",de:" Veranstaltungen gefunden",nl:" Evenementen gevonden"},"événement trouvé":{en:" Event found",fr:" Événement trouvé",de:" Veranstaltung gefunden",nl:" Evenement gevonden"},"Aucun événement n'a été trouvé":{en:"No event was found",fr:"Aucun événement n'a été trouvé",de:"Keine Veranstaltungen gefunden",nl:"Geen evenement gevonden"},"Proposer un événement":{en:"Suggest a event",fr:"Proposer un événement",de:"Veranstaltung vorschlagen",nl:"Evenement voorstellen"},"Infos pratiques":{en:"Practical information",fr:"Infos pratiques",de:"Praktische Informationen",nl:"Praktische informatie"},"Accessible aux PMR":{en:"Accessibility for PRM",fr:"Accessible aux PMR",de:"Barrierefreiheit für PMR",nl:"Toegankelijk voor PRM"},"Lien de l'événement":{en:"Event link",fr:"Lien de l'événement",de:"Veranstaltungslink",nl:"Evenement link"},"contacts trouvés":{en:" Contact found",fr:" Contacts trouvés",de:" Kontakt gefunden",nl:" Contact gevonden"},"contact trouvé":{en:" Contact found",fr:" Contact trouvé",de:" Kontakt gefunden",nl:" Contact gevonden"},"Aucun contact n'a été trouvé":{en:"No contact was found",fr:"Aucun contact n'a été trouvé",de:"Kein Kontakt gefunden",nl:"Geen contact gevonden"},"Proposer un contact":{en:"Suggest a contact",fr:"Proposer un contact",de:"Kontakt vorschlagen",nl:"Contact voorstellen"},"Toutes les dates":{en:"All dates",fr:"Toutes les dates",de:"Alle Daten",nl:"Alle data"},"Aujourd'hui":{en:"Today",fr:"Aujourd'hui",de:"Heute",nl:"Vandaag"},Demain:{en:"Tomorrow",fr:"Demain",de:"Morgen",nl:"Morgen"},"Ce week-end":{en:"This weekend",fr:"Ce week-end",de:"Dieses Wochenende",nl:"Dit weekend"},"Cette semaine":{en:"This week",fr:"Cette semaine",de:"Diese Woche",nl:"Deze week"},"Ce mois-ci":{en:"This month",fr:"Ce mois-ci",de:"Diesen Monat",nl:"Deze maand"},"Personnalisé (Du ... au ...)":{en:"Custom (From ... to ...)",fr:"Personnalisé (Du ... au ...)",de:"Benutzerdefiniert (Von ... bis ...)",nl:"Aangepast (Van ... tot ...)"},Personnalisé:{en:"Custom",fr:"Personnalisé",de:"Benutzerdefiniert",nl:"Aangepast"}}},35358:(e,t,n)=>{var a={"./af":42687,"./af.js":42687,"./ar":58475,"./ar-dz":31422,"./ar-dz.js":31422,"./ar-kw":44718,"./ar-kw.js":44718,"./ar-ly":60595,"./ar-ly.js":60595,"./ar-ma":1178,"./ar-ma.js":1178,"./ar-ps":22817,"./ar-ps.js":22817,"./ar-sa":34096,"./ar-sa.js":34096,"./ar-tn":64818,"./ar-tn.js":64818,"./ar.js":58475,"./az":57699,"./az.js":57699,"./be":59445,"./be.js":59445,"./bg":1427,"./bg.js":1427,"./bm":99613,"./bm.js":99613,"./bn":87764,"./bn-bd":23575,"./bn-bd.js":23575,"./bn.js":87764,"./bo":35707,"./bo.js":35707,"./br":89424,"./br.js":89424,"./bs":13575,"./bs.js":13575,"./ca":19088,"./ca.js":19088,"./cs":52650,"./cs.js":52650,"./cv":12405,"./cv.js":12405,"./cy":9e3,"./cy.js":9e3,"./da":60563,"./da.js":60563,"./de":76663,"./de-at":37237,"./de-at.js":37237,"./de-ch":61195,"./de-ch.js":61195,"./de.js":76663,"./dv":45690,"./dv.js":45690,"./el":27141,"./el.js":27141,"./en-au":64650,"./en-au.js":64650,"./en-ca":67896,"./en-ca.js":67896,"./en-gb":629,"./en-gb.js":629,"./en-ie":85106,"./en-ie.js":85106,"./en-il":13721,"./en-il.js":13721,"./en-in":83159,"./en-in.js":83159,"./en-nz":79516,"./en-nz.js":79516,"./en-sg":71230,"./en-sg.js":71230,"./eo":97404,"./eo.js":97404,"./es":11592,"./es-do":82844,"./es-do.js":82844,"./es-mx":23132,"./es-mx.js":23132,"./es-us":31541,"./es-us.js":31541,"./es.js":11592,"./et":7645,"./et.js":7645,"./eu":97726,"./eu.js":97726,"./fa":54397,"./fa.js":54397,"./fi":94997,"./fi.js":94997,"./fil":41037,"./fil.js":41037,"./fo":44567,"./fo.js":44567,"./fr":60548,"./fr-ca":72597,"./fr-ca.js":72597,"./fr-ch":22078,"./fr-ch.js":22078,"./fr.js":60548,"./fy":73893,"./fy.js":73893,"./ga":35236,"./ga.js":35236,"./gd":71663,"./gd.js":71663,"./gl":7463,"./gl.js":7463,"./gom-deva":27298,"./gom-deva.js":27298,"./gom-latn":59533,"./gom-latn.js":59533,"./gu":90504,"./gu.js":90504,"./he":53843,"./he.js":53843,"./hi":24767,"./hi.js":24767,"./hr":19738,"./hr.js":19738,"./hu":131,"./hu.js":131,"./hy-am":40374,"./hy-am.js":40374,"./id":25289,"./id.js":25289,"./is":4076,"./is.js":4076,"./it":21273,"./it-ch":86181,"./it-ch.js":86181,"./it.js":21273,"./ja":25377,"./ja.js":25377,"./jv":39972,"./jv.js":39972,"./ka":53368,"./ka.js":53368,"./kk":97018,"./kk.js":97018,"./km":19068,"./km.js":19068,"./kn":48805,"./kn.js":48805,"./ko":81062,"./ko.js":81062,"./ku":74932,"./ku-kmr":76163,"./ku-kmr.js":76163,"./ku.js":74932,"./ky":3584,"./ky.js":3584,"./lb":49790,"./lb.js":49790,"./lo":70617,"./lo.js":70617,"./lt":120,"./lt.js":120,"./lv":95522,"./lv.js":95522,"./me":54262,"./me.js":54262,"./mi":36978,"./mi.js":36978,"./mk":26568,"./mk.js":26568,"./ml":57309,"./ml.js":57309,"./mn":58715,"./mn.js":58715,"./mr":59879,"./mr.js":59879,"./ms":53008,"./ms-my":46955,"./ms-my.js":46955,"./ms.js":53008,"./mt":19333,"./mt.js":19333,"./my":67714,"./my.js":67714,"./nb":84572,"./nb.js":84572,"./ne":40873,"./ne.js":40873,"./nl":73154,"./nl-be":65766,"./nl-be.js":65766,"./nl.js":73154,"./nn":84696,"./nn.js":84696,"./oc-lnc":99044,"./oc-lnc.js":99044,"./pa-in":93051,"./pa-in.js":93051,"./pl":26828,"./pl.js":26828,"./pt":8132,"./pt-br":29813,"./pt-br.js":29813,"./pt.js":8132,"./ro":8331,"./ro.js":8331,"./ru":43509,"./ru.js":43509,"./sd":58419,"./sd.js":58419,"./se":92332,"./se.js":92332,"./si":37256,"./si.js":37256,"./sk":22546,"./sk.js":22546,"./sl":69403,"./sl.js":69403,"./sq":3888,"./sq.js":3888,"./sr":79369,"./sr-cyrl":50536,"./sr-cyrl.js":50536,"./sr.js":79369,"./ss":24314,"./ss.js":24314,"./sv":52805,"./sv.js":52805,"./sw":50886,"./sw.js":50886,"./ta":2691,"./ta.js":2691,"./te":2727,"./te.js":2727,"./tet":87451,"./tet.js":87451,"./tg":46217,"./tg.js":46217,"./th":14148,"./th.js":14148,"./tk":96205,"./tk.js":96205,"./tl-ph":3861,"./tl-ph.js":3861,"./tlh":53426,"./tlh.js":53426,"./tr":97110,"./tr.js":97110,"./tzl":51992,"./tzl.js":51992,"./tzm":95919,"./tzm-latn":19673,"./tzm-latn.js":19673,"./tzm.js":95919,"./ug-cn":5048,"./ug-cn.js":5048,"./uk":61600,"./uk.js":61600,"./ur":97327,"./ur.js":97327,"./uz":33127,"./uz-latn":86929,"./uz-latn.js":86929,"./uz.js":33127,"./vi":69733,"./vi.js":69733,"./x-pseudo":66261,"./x-pseudo.js":66261,"./yo":93096,"./yo.js":93096,"./zh-cn":80802,"./zh-cn.js":80802,"./zh-hk":46030,"./zh-hk.js":46030,"./zh-mo":45123,"./zh-mo.js":45123,"./zh-tw":26710,"./zh-tw.js":26710};function l(e){var t=r(e);return n(t)}function r(e){if(!n.o(a,e)){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t}return a[e]}l.keys=function(){return Object.keys(a)},l.resolve=r,e.exports=l,l.id=35358}}]);