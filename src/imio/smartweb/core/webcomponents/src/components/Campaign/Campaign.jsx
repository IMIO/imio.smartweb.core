import React, { useEffect, useState, useContext, createContext } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import useAxios from "../../hooks/useAxios";
import CampaignList from "./CampaignList/CampaignList";
import CampaignContent from "./CampaignContent/CampaignContent";
import { Provider, Translate } from "react-translated";
import translation from "../../utils/translation";

import "./Campaign.scss";

export default function Campaign(props) {
    console.log("Ici le component Campaign.jsx (index)");
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
    return (
        <Routes>
            <Route
                exact
                path="/"
                element={
                    <div className="r-wrapper r-campaign">
                        <CampaignList queryUrl={props.queryUrl} />
                    </div>
                }
            ></Route>
            <Route
                path={"/:name"}
                element={
                    <div className="r-wrapper r-campaign">
                        <div className="r-result r-campaign-result">
                            <CampaignContent queryUrl={props.queryUrl} />
                        </div>
                    </div>
                }
            ></Route>
        </Routes>
    );
}
