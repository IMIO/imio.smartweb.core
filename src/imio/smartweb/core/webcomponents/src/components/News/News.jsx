import React, { useEffect, useState, useContext, createContext } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ScrollContext } from "../../hooks/ScrollContext";
import Filters from "./Filters/Filter";
import NewsContent from "./NewsContent/NewsContent";
import NewsList from "./NewsList/NewsList";
import useAxios from "../../hooks/useAxios";
import "./News.scss";
import "../Filters/MainFilter.scss";
import useFilterQuery from "../../hooks/useFilterQuery";
import { Provider, Translate } from "react-translated";
import translation from "../../utils/translation";
import queryString from "query-string";

export const LanguageContext = createContext("fr");
export default function News(props) {
    // Utilisation de useState pour gérer la valeur du contexte
    const [scrollPos, setScrollPos] = useState(0);
    // Fonction pour mettre à jour la position du scroll
    const updateScrollPos = (newScrollPos) => {
        setScrollPos(newScrollPos);
    };
    return (
        <LanguageContext.Provider value={props.currentLanguage}>
            <BrowserRouter basename={props.viewPath}>
                <Provider language={props.currentLanguage} translation={translation}>
                    <ScrollContext.Provider value={{ scrollPos, updateScrollPos }}>
                        <NewsView
                            queryFilterUrl={props.queryFilterUrl}
                            queryUrl={props.queryUrl}
                            proposeUrl={props.proposeUrl}
                            batchSize={props.batchSize}
                            showCategoriesOrTopics={props.showCategoriesOrTopics}
                            contextAuthenticatedUser={props.contextAuthenticatedUser}
                        />
                    </ScrollContext.Provider>
                </Provider>
            </BrowserRouter>
        </LanguageContext.Provider>
    );
}
const NewsView = (props) => {
    const { u, ...parsed } = Object.assign(
        { b_start: 0, fullobjects: 1 },
        queryString.parse(useFilterQuery().toString())
    );
    const { scrollPos, updateScrollPos } = useContext(ScrollContext);
    const [itemsArray, setItemsArray] = useState(null);
    const [itemsNumber, setItemsNumber] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [filters, setFilters] = useState(parsed);
    const [batchStart, setBatchStart] = useState(0);
    const [loadMoreLaunch, setLoadMoreLaunch] = useState(false);
    const { response, error, isLoading, isMore } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.queryUrl,
            headers: {
                Accept: "application/json",
            },
            params: filters,
            load: loadMoreLaunch,
        },
        []
    );

    // set all news in state
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

    // set state filters when active filter selection
    const filtersChange = (value) => {
        setLoadMoreLaunch(false);
        setBatchStart((batchStart) => 0);
        setFilters(value);
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
    // coditional list render
    let listRender;
    if (itemsArray && itemsArray.length > 0) {
        listRender = (
            <NewsList
                onChange={clickID}
                itemsArray={itemsArray}
                showCategoriesOrTopics={props.showCategoriesOrTopics}
                contextAuthenticatedUser={props.contextAuthenticatedUser}
            />
        );
    } else if (!isLoading) {
        listRender = (
            <p>
                <Translate text="Aucune actualité n'a été trouvée" />
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
        <div>
            <div className="r-wrapper r-actu-wrapper">
                <div className="r-result r-annuaire-result">
                    <Routes>
                        <Route
                            exact
                            path="/"
                            element={
                                <>
                                    <div className="r-result-filter actu-result-filter">
                                        <Filters
                                            url={props.queryFilterUrl}
                                            activeFilter={filters}
                                            onChange={filtersChange}
                                        />
                                        {props.proposeUrl && (
                                            <div className="r-add-news">
                                                <a target="_blank" href={props.proposeUrl}>
                                                    <Translate text="Proposer une actualité" />
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
                                    </div>
                                    {itemsNumber > 0 ? (
                                        <p className="r-results-numbers">
                                            <span>{itemsNumber}</span>{" "}
                                            {itemsNumber > 1 ? (
                                                <Translate text="Actualités trouvées" />
                                            ) : (
                                                <Translate text="Actualité trouvée" />
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
                                </>
                            }
                        ></Route>
                        <Route
                            path={"/:name"}
                            element={
                                <NewsContent
                                    onChange={clickID}
                                    onReturn={filtersChange}
                                    queryUrl={props.queryUrl}
                                    contextAuthenticatedUser={props.contextAuthenticatedUser}
                                />
                            }
                        ></Route>
                    </Routes>
                </div>
            </div>
        </div>
    );
};
