import React, { useEffect, useState, useContext, createContext } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import useAxios from "../../hooks/useAxios";
import CampaignList from "./CampaignList/CampaignList";
import CampaignContent from "./CampaignContent/CampaignContent";
import "./Campaign.scss";

export default function Campaign(props) {
    return (
        <BrowserRouter basename={props.viewPath}>
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
    if (response && response.length > 0) {
        listRender = <CampaignList itemsArray={response} />;
    } else if (!isLoading) {
        listRender = (
            <p>
                <Translate text="Aucune actualité n'a été trouvée" />
            </p>
        );
    }
    return (
        <div>
            <div>
                <h1>React campaign</h1>
                <Routes>
                    <Route
                        exact
                        path="/"
                        element={<div className="r-wrapper containter">{listRender}</div>}
                    ></Route>
                    <Route
                        path={"/:name"}
                        element={
                            <div className="r-wrapper container r-annuaire-wrapper">
                                <div className="r-result r-annuaire-result">
                                    <CampaignContent item={response} queryUrl={props.queryUrl} />
                                </div>
                            </div>
                        }
                    ></Route>
                </Routes>
            </div>
        </div>
    );
}
