import React, { useEffect, useState, useContext, useRef } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ScrollContext } from "../../hooks/ScrollContext";
import Filters from "./Filters/Filter";
import EventContent from "./EventContent/EventContent";
import EventList from "./EventList/EventList";
import Map from "../../utils/Map";
import useAxios from "../../hooks/useAxios";
import "./Events.scss";
import "../Filters/MainFilter.scss";
import useFilterQuery from "../../hooks/useFilterQuery";
import { Provider, Translate } from "react-translated";
import translation from "../../utils/translation";
import moment from "moment";
import queryString from "query-string";

export default function Events(props) {
    // Utilisation de useState pour gérer la valeur du contexte
    const [scrollPos, setScrollPos] = useState(0);
    // Fonction pour mettre à jour la position du scroll
    const updateScrollPos = (newScrollPos) => {
        setScrollPos(newScrollPos);
    };
    return (
        <BrowserRouter basename={props.viewPath}>
            <Provider language={props.currentLanguage} translation={translation}>
                <ScrollContext.Provider value={{ scrollPos, updateScrollPos }}>
                    <EventsView
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
                </ScrollContext.Provider>
            </Provider>
        </BrowserRouter>
    );
}
function EventsView(props) {
    const { u, ...parsed } = Object.assign(
        {
            b_start: 0,
            "event_dates.query": [moment().format("YYYY-MM-DD")],
            "event_dates.range": props.onlyPastEvents === "True" ? "max" : "min",
        },
        queryString.parse(useFilterQuery().toString())
    );
    const { scrollPos, updateScrollPos } = useContext(ScrollContext);
    const [itemsArray, setItemsArray] = useState(null);
    const [itemsNumber, setItemsNumber] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [hoverId, setHoverId] = useState(null);
    const [filters, setFilters] = useState(parsed);
    const [batchStart, setBatchStart] = useState(0);
    const [loadMoreLaunch, setLoadMoreLaunch] = useState(false);
    const displayMap = props.displayMap === "True" ? true : false;
    const { response, error, isLoading, isMore } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.queryUrl,
            headers: {
                Accept: "application/json",
            },
            params: filters,
            paramsSerializer: { indexes: null },
            load: loadMoreLaunch,
        },
        []
    );

    // set all contacts state
    useEffect(() => {
        if (response !== null) {
            if (isMore) {
                setItemsArray((itemsArray) => [...itemsArray, ...response.items]);
            } else {
                setItemsArray(response.items);
            }
            setItemsNumber(response.items_total);
        }
    }, [response]);

    // set state id when clicked on list element
    const clickID = (id) => {
        setClickId(id);
    };

    // set state hoverId when hover on list element
    const hoverID = (id) => {
        setHoverId(id);
    };

    // set state filters when active filter selection
    const filtersChange = (value) => {
        setLoadMoreLaunch(false);
        setBatchStart(() => 0);
        setFilters(value);
        window.scrollTo(0, 0);
    };

    // set batch
    const loadMore = () => {
        updateScrollPos(window.scrollY);
        setBatchStart((batchStart) => batchStart + parseInt(props.batchSize));
        setLoadMoreLaunch(true);
    };

    // Update filters Batch
    useEffect(() => {
        setFilters((prevFilters) => {
            return {
                ...prevFilters,
                b_start: batchStart,
            };
        });
    }, [batchStart]);

    // filter top style
    const filterRef = useRef();
    const [style, setStyle] = React.useState({ height: 0 });
    const [headerHeight, setHeaderHeight] = useState(0);
    useEffect(() => {
        setStyle({
            height: filterRef.current.clientHeight,
        });
        setHeaderHeight(filterRef.current.offsetTop);
    }, [filterRef]);

    // coditional list render
    let listRender;
    let MapRender;
    if (itemsArray && itemsArray.length > 0) {
        listRender = (
            <EventList
                onChange={clickID}
                itemsArray={itemsArray}
                onHover={hoverID}
                showCategoriesOrTopics={props.showCategoriesOrTopics}
                contextAuthenticatedUser={props.contextAuthenticatedUser}
            />
        );
        MapRender = (
            <Map
                headerHeight={style.height + headerHeight}
                clickId={clickId}
                hoverId={hoverId}
                items={itemsArray}
                queryUrl={props.queryUrl}
            />
        );
    } else if (!isLoading) {
        listRender = (
            <p>
                <Translate text="Aucun événement n'a été trouvé" />
            </p>
        );
    }
    const divLoader = (
        <div className="lds-roller-container">
            <Translate text="Chargement..." />
            <div className="lds-roller">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
    );
    return (
        <div className={`ref ${displayMap ? "view-map" : "no-map"}`}>
            <div
                className="r-result-filter-container"
                ref={filterRef}
                style={{ top: headerHeight }}
            >
                <div
                    id="r-result-filter"
                    className="r-result-filter container annuaire-result-filter"
                >
                    <Filters
                        url={props.queryFilterUrl}
                        activeFilter={filters}
                        onChange={filtersChange}
                        language={props.language}
                        onlyPastEvents={props.onlyPastEvents}
                    />
                    {props.proposeUrl && (
                        <div className="r-add-event">
                            <a target="_blank" href={props.proposeUrl}>
                                <Translate text="Proposer un événement" />
                                <div className="r-add-event-icon">
                                    <svg
                                        data-name="Calque 1"
                                        xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 668.26 676.14"
                                    >
                                        <path d="M162.9 51.83h304.7c-1.03-10.91-1.97-24.53-1.03-35.5.99-11.58 10.86-20.92 21.97-13.91 1.52.96 6.04 6.64 6.04 7.95v41.46h96.41c17.66 0 37.58 21.03 38.34 38.59l.15 330.53c64.12 72.13 46.53 184.36-36.31 233.47-75.97 45.03-172.33 17.55-214.13-59.16-3.7-.39-7.11.99-10.77 1.09-107.79 2.79-215.98-2.19-323.81-.04-23.59-1.48-41.85-16.37-44.42-40.43V92.25c-.86-17.33 20.73-40.42 37.5-40.42h98.4V10.37c0-4.74 8.82-10.3 13.49-10.3s13.49 5.56 13.49 10.3v41.46ZM135.93 78.8H42.52c-1.85 0-7.83 3.01-9.52 4.47-1.81 1.55-5.97 8.02-5.97 10.02v70.43h574.44V92.29c0-5.05-9.56-13.49-14.49-13.49h-92.41v42.46c0 .36-3.72 4.88-4.48 5.51-10.2 8.49-22.25.77-23.48-11.51-1.08-10.75.17-24.22.74-35l-1.26-1.45H162.9v41.46c0 7.08-11.03 10.55-17.26 9.26-3.19-.66-9.72-6.23-9.72-9.26V78.81Zm465.54 111.89H27.03v364.14c0 3.51 9.3 13.49 12.49 13.49H366.2c.09 0 2.2 2.45 1.48-.48-.85-3.46-2.9-7.53-3.68-11.31C339.69 439.65 444.15 343.54 558.51 376c15.31 4.35 29.93 11.48 42.96 20.48v-205.8Zm-92.11 206.1c-101.67 3.96-158.34 120.93-95.1 202.4 61.94 79.8 185.04 60.07 219.2-34.35 30.3-83.75-35.93-171.5-124.1-168.06Z" />
                                        <path d="M125.7 391.75c8.2-1.12 36.31-1.31 43.21 2.24 4.23 2.17 7.43 7.25 8.01 11.97 1.03 8.47.83 29.33.01 38.03-.55 5.9-3.6 11.52-9.48 13.5-5.74 1.92-34.71 1.64-42.05.99-6.3-.56-11.32-3.28-13.49-9.48-1.64-4.67-1.8-39.01-.89-44.94 1.09-7.08 8.1-11.4 14.68-12.29ZM125.47 269.22c8.01-1.33 34.99-1.74 41.96 1.37 5.91 2.63 8.74 7.04 9.47 13.51.95 8.47.9 28.46.05 37.02-.61 6.11-3.52 11.39-9.5 13.48-5.4 1.89-34.95 1.62-42.05.99-6.3-.56-11.32-3.28-13.49-9.48-1.65-4.7-1.77-39.02-.72-44.77 1.37-7.53 7.35-10.97 14.28-12.12ZM240.17 395.84c1.14-1.03 2.71-1.76 4.13-2.36 7.13-2.98 31.5-2.79 40.02-2.03 7.6.68 15.47 5.26 16.47 13.5 1.07 8.86.9 30.97.03 40.03-.74 7.63-5.97 12.63-13.53 13.44-8.95.96-29 .92-38.02.05-6.71-.65-12.62-5.56-13.46-12.52-1.1-9.15-.84-30.59-.02-40.02.32-3.67 1.58-7.58 4.38-10.1ZM249.56 268.86c7.35-1.15 35.4-1.11 41.75 1.73 3.79 1.69 7.16 4.42 8.51 8.47 1.88 5.61 1.69 35.87 1 43.06-.56 5.75-3.95 10.54-9.49 12.49-5.17 1.81-35.3 1.67-42.01.95s-12.66-5.45-13.51-12.47c-.92-7.69-1.05-35.52.26-42.74 1.07-5.88 7.83-10.6 13.49-11.48ZM528.54 509.38h56.44c5.87 0 11.61 8.82 11.58 14.49-.02 4.58-6.21 13.48-10.58 13.48h-57.44v54.45c0 2.01-3.75 9.07-5.47 10.51-7.92 6.68-22.5.53-22.5-9.51v-55.45h-57.44c-1.37 0-6.91-4.49-7.94-6.04-4.48-6.74-2.95-15.54 4.1-19.78.66-.4 4.58-2.15 4.84-2.15h56.44v-55.45c0-1.11 3.57-7.51 4.75-8.51 6.23-5.29 17.03-3.45 21.09 3.65.4.69 2.13 5.5 2.13 5.86v54.45Z" />
                                    </svg>
                                </div>
                            </a>
                        </div>
                    )}
                </div>
            </div>
            <Routes>
                <Route
                    exact
                    path="/"
                    element={
                        <div className="r-wrapper container r-annuaire-wrapper">
                            <div className="r-result r-annuaire-result">
                                {itemsNumber > 0 ? (
                                    <p className="r-results-numbers">
                                        <span>{itemsNumber}</span>
                                        {itemsNumber > 1 ? (
                                            <Translate text="événements trouvés" />
                                        ) : (
                                            <Translate text="événement trouvé" />
                                        )}
                                    </p>
                                ) : (
                                    ""
                                )}
                                <div>{itemsArray !== null ? listRender : divLoader}</div>
                                <div className="r-load-more">
                                    {itemsNumber - props.batchSize > batchStart ? (
                                        <div>
                                            <span className="no-more-result">
                                                {isLoading ? divLoader : ""}
                                            </span>
                                            <button onClick={loadMore} className="btn-grad">
                                                {isLoading ? (
                                                    <Translate text="Chargement..." />
                                                ) : (
                                                    <Translate text="Plus de résultats" />
                                                )}
                                            </button>
                                        </div>
                                    ) : (
                                        <span className="no-more-result">
                                            {isLoading ? divLoader : ""}
                                        </span>
                                    )}
                                </div>
                            </div>
                            {displayMap && (
                                <div
                                    className="r-map annuaire-map"
                                    style={{
                                        top: style.height + headerHeight,
                                        height: "calc(100vh-" + style.height + headerHeight,
                                    }}
                                >
                                    {MapRender}
                                </div>
                            )}
                        </div>
                    }
                ></Route>
                <Route
                    path={"/:name"}
                    element={
                        <div className="r-wrapper container r-annuaire-wrapper">
                            <div className="r-result r-annuaire-result">
                                <EventContent
                                    queryUrl={props.queryUrl}
                                    onChange={clickID}
                                    onlyPastEvents={props.onlyPastEvents}
                                    contextAuthenticatedUser={props.contextAuthenticatedUser}
                                />
                            </div>
                            {displayMap && (
                                <div
                                    className="r-map annuaire-map"
                                    style={{
                                        top: style.height + headerHeight,
                                        height: "calc(100vh-" + style.height + headerHeight,
                                    }}
                                >
                                    {MapRender}
                                </div>
                            )}
                        </div>
                    }
                ></Route>
            </Routes>
        </div>
    );
}
