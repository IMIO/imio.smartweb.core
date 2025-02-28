import React, { useEffect, useState, useContext, useRef } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ScrollContext } from "../../hooks/ScrollContext";
import Filters from "./Filters/Filter";
import CampaignContent from "./CampaignContent/CampaignContent";
import CampaignList from "./CampaignList/CampaignList";
import Map from "../../utils/CampaignMap";
import useAxios from "../../hooks/useAxios";
import "./Campaign.scss";
import "../Filters/MainFilter.scss";
import useFilterQuery from "../../hooks/useFilterQuery";
import { Provider, Translate } from "react-translated";
import translation from "../../utils/translation";
import moment from "moment";
import queryString from "query-string";

export default function Campaign(props) {
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
                    <CampaignView
                        queryZonesUrl={props.queryZonesUrl}
                        queryTopicsUrl={props.queryTopicsUrl}
                        queryUrl={props.queryUrl}
                        proposeUrl={props.proposeUrl}
                        batchSize={props.batchSize}
                        displayMap={props.displayMap}
                        language={props.currentLanguage}
                    />
                </ScrollContext.Provider>
            </Provider>
        </BrowserRouter>
    );
}
function CampaignView(props) {
    const { u, ...parsed } = Object.assign(
        {
            b_start: 0,
            fullobjects: 1,
            "event_dates.query": [moment().format("YYYY-MM-DD")],
            "event_dates.range": props.onlyPastCampaign === "True" ? "max" : "min",
        },
        queryString.parse(useFilterQuery().toString())
    );
    const { scrollPos, updateScrollPos } = useContext(ScrollContext);
    const [itemsArray, setItemsArray] = useState([]);
    const [itemsNumber, setItemsNumber] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [hoverId, setHoverId] = useState(null);
    const [filters, setFilters] = useState({ b_start: 0 });
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

    // set all campaigns state
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
    // useEffect(() => {
    //     setFilters((prevFilters) => {
    //         return {
    //             ...prevFilters,
    //             b_start: batchStart,
    //         };
    //     });
    // }, [batchStart]);

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
        listRender = <CampaignList onChange={clickID} itemsArray={itemsArray} onHover={hoverID} />;
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
                        queryZonesUrl={props.queryZonesUrl}
                        queryTopicsUrl={props.queryTopicsUrl}
                        activeFilter={filters}
                        onChange={filtersChange}
                    />
                    {props.proposeUrl && (
                        <div className="r-add-contact">
                            <a target="_blank" rel="noreferrer" href={props.proposeUrl}>
                                <Translate text="Proposer un projet" />
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    fill="currentColor"
                                    className="bi bi-plus-circle"
                                    viewBox="0 0 16 16"
                                >
                                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16" />
                                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4" />
                                </svg>
                            </a>
                        </div>
                    )}
                    {itemsNumber > 0 ? (
                        <p className="r-results-numbers">
                            <span>{itemsNumber}</span>
                            {itemsNumber > 1 ? (
                                <Translate text="projets trouvés" />
                            ) : (
                                <Translate text="projet trouvé" />
                            )}
                        </p>
                    ) : (
                        <p className="r-results-numbers">
                            <Translate text="Aucun résultat" />
                        </p>
                    )}
                </div>
            </div>
            <Routes>
                <Route
                    exact
                    path="/"
                    element={
                        <div className="r-wrapper container r-campaign-wrapper">
                            <div className="r-result r-campaign-result">
                                {itemsNumber > 0 ? (
                                    <p className="r-results-numbers">
                                        <span>{itemsNumber}</span>
                                        {itemsNumber > 1 ? (
                                            <Translate text="projets trouvés" />
                                        ) : (
                                            <Translate text="projet trouvé" />
                                        )}
                                    </p>
                                ) : (
                                    <p className="r-results-numbers">
                                        <Translate text="Aucun résultat" />
                                    </p>
                                )}
                                <div>{listRender}</div>
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
                                    className="r-map campaign-map"
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
                        <div className="r-wrapper container r-campaign-wrapper">
                            <div className="r-result r-campaign-result">
                                <CampaignContent
                                    queryUrl={props.queryUrl}
                                    onChange={clickID}
                                    onlyPastCampaign={props.onlyPastCampaign}
                                    contextAuthenticatedUser={props.contextAuthenticatedUser}
                                />
                            </div>
                            {displayMap && (
                                <div
                                    className="r-map campaign-map"
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
