import React, { useEffect, useState, useRef } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Filters from "./Filters/Filter";
import EventContent from "./EventContent/EventContent";
import EventList from "./EventList/EventList";
import Map from "../../utils/Map";
import useAxios from "../../hooks/useAxios";
import "./Events.scss";
import useFilterQuery from "../../hooks/useFilterQuery";
import { Provider, Translate } from "react-translated";
import translation from '../../utils/translation';
import moment from "moment";

export default function Events(props) {
    return (
        <Router basename={props.viewPath}>
            <Provider language={props.currentLanguage} translation={translation}>
                <EventsView
                    queryFilterUrl={props.queryFilterUrl}
                    queryUrl={props.queryUrl}
                    proposeUrl={props.proposeUrl}
                    batchSize={props.batchSize}
                    displayMap={props.displayMap}
                    language={props.currentLanguage}
                />
            </Provider>
        </Router>
    );
}
function EventsView(props) {
    const queryString = require("query-string");
    const { u, ...parsed } = Object.assign(
        { b_start: 0, fullobjects: 1, "event_dates.query":[moment().format('YYYY-MM-DD')],"event_dates.range":"min"},
        queryString.parse(useFilterQuery().toString())
    );
    const [itemsArray, setItemsArray] = useState([]);
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
    let portalHeader = document.getElementById("portal-header");
    let portalHeaderHeight = portalHeader.offsetHeight;

    const filterRef = useRef();
    const [style, setStyle] = React.useState({ height: 0 });
    useEffect(() => {
        setStyle({
            height: filterRef.current.clientHeight,
        });
    }, [filterRef.current]);

    // coditional list render
    let listRender;
    let MapRender;
    if (itemsArray && itemsArray.length > 0) {
        listRender = (
            <EventList onChange={clickID} itemsArray={itemsArray} onHover={hoverID} />
        );
        MapRender = (
            <Map
                headerHeight={style.height + portalHeaderHeight}
                clickId={clickId}
                hoverId={hoverId}
                items={itemsArray}
                queryUrl={props.queryUrl}
            />
        );
    } else if (!isLoading) {
        listRender = <p><Translate text="Aucun événement n'a été trouvé" /></p>;
    }

    const divLoader = <div className="lds-roller-container"><div className="lds-roller"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></div>;
    return (
        <div className={`ref ${displayMap ? "view-map" : "no-map"}`}>
            <div
                className="r-result-filter-container"
                ref={filterRef}
                style={{ top: portalHeaderHeight }}
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
                    />
                    {props.proposeUrl &&
                        (
                            <div className="r-add-event">
                                <a target="_blank" href={props.proposeUrl}><Translate text='Proposer un événement' /></a>
                            </div>
                        )
                    }
                    {itemsNumber > 0 ? (
                        <p className="r-results-numbers">
                            <span>{itemsNumber}</span>
                            {itemsNumber > 1
                                ? <Translate text='événements trouvés' />
                                : <Translate text='événement trouvé' />}
                        </p>
                    ) : (
                        <p className="r-results-numbers"><Translate text='Aucun résultat' /></p>
                    )}
                </div>
            </div>
            <Switch>

                <Route exact path="/">
                    <div className="r-wrapper container r-annuaire-wrapper">
                        <div className="r-result r-annuaire-result">
                            <div>{listRender}</div>
                            <div className="r-load-more">
                                {itemsNumber - props.batchSize > batchStart ? (
                                    <div>
                                        <span className="no-more-result">
                                            {isLoading ? divLoader : ""}
                                        </span>
                                        <button onClick={loadMore} className="btn-grad">
                                            {isLoading ? <Translate text='Chargement...' /> : <Translate text='Plus de résultats' />}
                                        </button>
                                    </div>
                                ) : (
                                    <span className="no-more-result">
                                        {isLoading ? divLoader : ""}
                                    </span>
                                )}
                            </div>
                        </div>
                        {displayMap && <div
                            className="r-map annuaire-map"
                            style={{
                                top: style.height + portalHeaderHeight,
                                height: "calc(100vh-" + style.height + portalHeaderHeight,
                            }}
                        >
                            {MapRender}
                        </div>
                        }
                    </div>
                </Route>
                <Route path={"/:name"}>
                    <div className="r-wrapper container r-annuaire-wrapper">
                        <div className="r-result r-annuaire-result">
                            <EventContent queryUrl={props.queryUrl} onChange={clickID} />
                        </div>
                        {displayMap && <div
                            className="r-map annuaire-map"
                            style={{
                                top: style.height + portalHeaderHeight,
                                height: "calc(100vh-" + style.height + portalHeaderHeight,
                            }}
                        >
                            {MapRender}
                        </div>
                        }
                    </div>
                </Route>
            </Switch>
        </div>
    );
}
