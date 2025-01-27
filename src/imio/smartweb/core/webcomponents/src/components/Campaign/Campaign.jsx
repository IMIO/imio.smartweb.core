import React, { useEffect, useState, useContext, createContext } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import useAxios from "../../hooks/useAxios";
import CampaignList from "./CampaignList/CampaignList";
import CampaignContent from "./CampaignContent/CampaignContent";
import { Provider, Translate } from "react-translated";
import translation from "../../utils/translation";

import "./Campaign.scss";

export default function Campaign(props) {
    return (
        <BrowserRouter basename={props.viewPath}>
            <Provider language={props.currentLanguage} translation={translation}>
                <CampaignView
                    queryFilterUrl={props.queryFilterUrl}
                    queryUrl={props.queryUrl}
                    proposeUrl={props.proposeUrl}
                    batchSize={props.batchSize}
                    displayMap={props.displayMap}
                    onlyPastEvents={props.onlyPastEvents}
                    language={props.currentLanguage}
                    showCategoriesOrTopics={props.showCategoriesOrTopics}
                    contextAuthenticatedUser={props.contextAuthenticatedUser}
                />
            </Provider>
        </BrowserRouter>
    );
}

function CampaignView(props) {
    const [filters, setFilters] = useState({ b_start: 0 });

    const { response, error, isLoading, isMore } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.queryUrl,
            headers: {
                Accept: "application/json",
            },
            params: filters,
        },
        []
    );

    // coditional list render
    let listRender;
    if (response && response.items.length > 0) {
        listRender = <CampaignList itemsArray={response.items} />;
    } else if (!isLoading) {
        listRender = <p>Aucune actualité n'a été trouvée"</p>;
    }
    console.log("Ici le component Campaign.jsx (index)");
    return response && response.items ? (
        <Routes>
            <Route
                exact
                path="/"
                element={<div className="r-wrapper r-campaign">{listRender}</div>}
            ></Route>
            <Route
                path={"/:name"}
                element={
                    <div className="r-wrapper r-campaign-wrapper">
                        <div className="r-result r-campaign-result">
                            <CampaignContent item={response} queryUrl={props.queryUrl} />
                        </div>
                    </div>
                }
            ></Route>
        </Routes>
    ) : (
        <div>Loadings</div>
    );
}
