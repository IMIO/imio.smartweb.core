import React, { useEffect, useState } from "react";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import { getPath } from "../../utils/url";
import Skeleton from "./Skeleton/Skeleton.jsx";
import Filters from "./Filters/Filter"
import ContactResult from "./ContactResult/ContactResult"
import NewsResult from "./NewsResult/NewsResult"
import EventsResult from "./EventsResult/EventsResult"
import WebResult from "./WebResult/WebResult"

import useAxios from "../../hooks/useAxios";
import "./Search.scss";

const Search = (props) => {
    const [params, setParams] = useState({});
    const [filters, setFilters] = useState({});
    const [batchSize, setBatchSize] = useState(6);


    const filtersChange = (value) => {
        setFilters(value)
    }
    const callback = () => {
        setBatchSize(batchSize + 5);
    }
    useEffect(() => {
        setParams({ ...filters, 'b_size': batchSize })
    }, [filters, batchSize]);

    return (
        <div className="ref">
            <div className="r-search">
                <div className="row r-search-filters">
                    <Filters url={props.queryUrl} onChange={filtersChange} />
                </div>
                <div className="row r-search-result">
                    <WebResult urlParams={params} url={props.queryUrl} />
                    <NewsResult urlParams={params} url={props.queryUrl} />
                    <EventsResult urlParams={params} url={props.queryUrl} />
                    <ContactResult urlParams={params} url={props.queryUrl}  />
                </div>
            </div>
        </div>
    );
};

export default Search;
