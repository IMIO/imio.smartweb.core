import React, { useState, useCallback } from "react";
import useIsMobile from "../../hooks/useIsMobile";
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
    const parsed = queryString.parse(useFilterQuery().toString());
    const { SearchableText, iam, topics } = parsed;
    const parsed2 = { SearchableText: SearchableText, iam: iam, topics: topics };
    // const parsed2 = { ...parsed };
    const [filters, setFilters] = useState(parsed2);
    const [batchSize, setBatchSize] = useState(6);
    const isMobile = useIsMobile();
    const [resultCounts, setResultCounts] = useState({});

    const filtersChange = (value) => {
        setFilters(value);
    };
    const callback = () => {
        setBatchSize(batchSize + 5);
    };

    const onCountWeb = useCallback((n) => setResultCounts((p) => ({ ...p, web: n })), []);
    const onCountNews = useCallback((n) => setResultCounts((p) => ({ ...p, news: n })), []);
    const onCountEvents = useCallback((n) => setResultCounts((p) => ({ ...p, events: n })), []);
    const onCountDirectory = useCallback((n) => setResultCounts((p) => ({ ...p, directory: n })), []);

    const columns = [
        {
            key: "web",
            count: resultCounts.web,
            el: <WebResult key="web" urlParams={filters} url={props.queryUrl} onCount={onCountWeb} />,
        },
        props.resultOption.news && {
            key: "news",
            count: resultCounts.news,
            el: props.areViewsAvailable.news ? (
                <NewsResult
                    key="news"
                    urlParams={filters}
                    url={props.queryUrl}
                    available={props.areViewsAvailable.news}
                    onCount={onCountNews}
                />
            ) : (
                <div key="news" className="r-search-header">
                    <h2 className="r-search-header-title">
                        <Translate text="Actualités" />
                    </h2>
                    <div className="search-disabled-message">
                        <Translate text="Recherche impossible car vue actualités supprimée" />
                    </div>
                </div>
            ),
        },
        props.resultOption.events && {
            key: "events",
            count: resultCounts.events,
            el: props.areViewsAvailable.events ? (
                <EventsResult
                    key="events"
                    urlParams={filters}
                    url={props.queryUrl}
                    available={props.areViewsAvailable.events}
                    onCount={onCountEvents}
                />
            ) : (
                <div key="events" className="r-search-header">
                    <h2 className="r-search-header-title">
                        <Translate text="Événements" />
                    </h2>
                    <div className="search-disabled-message">
                        <Translate text="Recherche impossible car vue événements supprimée" />
                    </div>
                </div>
            ),
        },
        props.resultOption.directory && {
            key: "directory",
            count: resultCounts.directory,
            el: props.areViewsAvailable.directory ? (
                <ContactResult
                    key="directory"
                    urlParams={filters}
                    url={props.queryUrl}
                    available={props.areViewsAvailable.directory}
                    onCount={onCountDirectory}
                />
            ) : (
                <div key="directory" className="r-search-header">
                    <h2 className="r-search-header-title">
                        <Translate text="Annuaire" />
                    </h2>
                    <div className="search-disabled-message">
                        <Translate text="Recherche impossible car vue annuaire supprimée" />
                    </div>
                </div>
            ),
        },
    ].filter(Boolean);

    if (isMobile) {
        columns.sort((a, b) => {
            const aEmpty = a.count === 0 ? 1 : 0;
            const bEmpty = b.count === 0 ? 1 : 0;
            return aEmpty - bEmpty;
        });
    }

    return (
        <div className="ref">
            <div className="r-search r-search-container">
                <div className="row r-search-filters">
                    <Filters url={props.queryUrl} activeFilter={filters} onChange={filtersChange} />
                </div>
                <div className="r-search-result">{columns.map((col) => col.el)}</div>
            </div>
        </div>
    );
};
