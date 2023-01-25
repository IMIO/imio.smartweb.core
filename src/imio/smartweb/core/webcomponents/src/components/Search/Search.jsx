import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Filters from "./Filters/Filter";
import ContactResult from "./ContactResult/ContactResult";
import NewsResult from "./NewsResult/NewsResult";
import EventsResult from "./EventsResult/EventsResult";
import WebResult from "./WebResult/WebResult";
import useFilterQuery from "../../hooks/useFilterQuery";
import "./Search.scss";

export default function Search(props) {
    return (
        <Router>
            <SearchView
                queryFilterUrl={props.queryFilterUrl}
                queryUrl={props.queryUrl}
                resultOption={JSON.parse(props.resultOption)}
            />
        </Router>
    );
}
const SearchView = (props) => {
    const queryString = require("query-string");
    const parsed = queryString.parse(useFilterQuery().toString());
    const { SearchableText, iam,topics } = parsed;
    const parsed2 = {'SearchableText':SearchableText,'iam':iam,'topics':topics};
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
                    {props.resultOption.news && (
                        <NewsResult urlParams={filters} url={props.queryUrl} />
                    )}
                    {props.resultOption.events && (
                        <EventsResult urlParams={filters} url={props.queryUrl} />
                    )}
                    {props.resultOption.directory && (
                        <ContactResult urlParams={filters} url={props.queryUrl} />
                    )}
                </div>
            </div>
        </div>
    );
};
