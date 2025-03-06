import React, { useState } from "react";
import { BrowserRouter } from "react-router-dom";
import Filters from "./Filters/Filter";
import ContactResult from "./ContactResult/ContactResult";
import NewsResult from "./NewsResult/NewsResult";
import EventsResult from "./EventsResult/EventsResult";
import WebResult from "./WebResult/WebResult";
import useFilterQuery from "../../hooks/useFilterQuery";
import { Provider } from "react-translated";
import translation from "../../utils/translation";
import queryString from "query-string";
import { Translate } from "react-translated";

import "./Search.scss";

export default function Search(props) {
    return (
        <BrowserRouter>
            <Provider language={props.currentLanguage} translation={translation}>
                <SearchView
                    queryFilterUrl={props.queryFilterUrl}
                    queryUrl={props.queryUrl}
                    resultOption={JSON.parse(props.resultOption)}
                    areViewsAvailable={JSON.parse(props.areViewsAvailable)}
                />
            </Provider>
        </BrowserRouter>
    );
}
const SearchView = (props) => {
    console.log(props.areViewsAvailable);
    const parsed = queryString.parse(useFilterQuery().toString());
    const { SearchableText, iam, topics } = parsed;
    const parsed2 = { SearchableText: SearchableText, iam: iam, topics: topics };
    // const parsed2 = { ...parsed };
    const [filters, setFilters] = useState(parsed2);
    const [batchSize, setBatchSize] = useState(6);

    const filtersChange = (value) => {
        setFilters(value);
    };
    const callback = () => {
        setBatchSize(batchSize + 5);
    };
    return (
        <div className="ref">
            <div className="r-search r-search-container">
                <div className="row r-search-filters">
                    <Filters url={props.queryUrl} activeFilter={filters} onChange={filtersChange} />
                </div>
                <div className="r-search-result">
                    <WebResult urlParams={filters} url={props.queryUrl} />
                    {props.resultOption.news &&
                        (props.areViewsAvailable.news ? (
                            <NewsResult
                                urlParams={filters}
                                url={props.queryUrl}
                                available={props.areViewsAvailable.news}
                            />
                        ) : (
                            <div className="r-search-header">
                                <h2 className="r-search-header-title">
                                    <Translate text="Actualités" />
                                </h2>
                                <div className="search-disabled-message">
                                    Recherche impossible car vue actualités supprimée
                                </div>
                            </div>
                        ))}
                    {props.resultOption.events &&
                        (props.areViewsAvailable.events ? (
                            <EventsResult
                                urlParams={filters}
                                url={props.queryUrl}
                                available={props.areViewsAvailable.events}
                            />
                        ) : (
                            <div className="r-search-header">
                                <h2 className="r-search-header-title">
                                    <Translate text="Événements" />
                                </h2>
                                <div className="search-disabled-message">
                                    Recherche impossible car vue événements supprimée
                                </div>
                            </div>
                        ))}
                    {props.resultOption.directory &&
                        (props.areViewsAvailable.directory ? (
                            <ContactResult
                                urlParams={filters}
                                url={props.queryUrl}
                                available={props.areViewsAvailable.directory}
                            />
                        ) : (
                            <div className="r-search-header">
                                <h2 className="r-search-header-title">
                                    <Translate text="Annuaire" />
                                </h2>
                                <div className="search-disabled-message">
                                    Recherche impossible car vue annuaire supprimée
                                </div>
                            </div>
                        ))}
                </div>
            </div>
        </div>
    );
};
