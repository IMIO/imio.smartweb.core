import React, { useEffect, useState, createContext, useContex } from "react";
import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";
import Filters from "./Filters/Filter";
import NewsContent from "./NewsContent/NewsContent";
import NewsList from "./NewsList/NewsList";
import useAxios from "../../hooks/useAxios";
import "./News.scss";
import useFilterQuery from "../../hooks/useFilterQuery";
import { Provider, Translate } from "react-translated";
import translation from '../../utils/translation';
import queryString from 'query-string';

export const LanguageContext = createContext("fr");
export default function News(props) {
    return (
        <LanguageContext.Provider value={props.currentLanguage}>
            <BrowserRouter basename={props.viewPath}>
                <Provider language={props.currentLanguage} translation={translation}>
                    <NewsView
                        queryFilterUrl={props.queryFilterUrl}
                        queryUrl={props.queryUrl}
                        proposeUrl={props.proposeUrl}
                        batchSize={props.batchSize}
                    />
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
    const [itemsArray, setItemsArray] = useState([]);
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
        listRender = <NewsList onChange={clickID} itemsArray={itemsArray} />;
    } else if (!isLoading) {
        listRender = <p><Translate text="Aucune actualité n'a été trouvée" /></p>;
    }

    const divLoader = <div className="lds-roller-container"><div className="lds-roller"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></div>;

    return (
        <div>
            <div className="r-wrapper r-actu-wrapper">
                <div className="r-result r-annuaire-result">
                    <Routes>
                        <Route exact path="/" element={
                            <>
                                <div className="r-result-filter actu-result-filter">
                                    <Filters
                                        url={props.queryFilterUrl}
                                        activeFilter={filters}
                                        onChange={filtersChange}
                                    />
                                    {props.proposeUrl &&
                                        (
                                            <div className="r-add-news">
                                                <a target="_blank" href={props.proposeUrl}><Translate text='Proposer une actualité' /></a>
                                            </div>
                                        )
                                    }
                                    {itemsNumber > 0 ? (
                                        <p className="r-results-numbers">
                                            <span>{itemsNumber}</span>{" "}
                                            {itemsNumber > 1
                                                ? <Translate text='Actualités trouvées' />
                                                : <Translate text='Actualité trouvée' />}
                                        </p>
                                    ) : (
                                        <p className="r-results-numbers"><Translate text='Aucun résultat' /></p>
                                    )}
                                </div>
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
                            </>
                        }>
                        </Route>
                        <Route path={"/:name"} element={
                            <NewsContent
                                onChange={clickID}
                                onReturn={filtersChange}
                                queryUrl={props.queryUrl}
                            />
                        }>
                        </Route>
                    </Routes>
                </div>
            </div>
        </div>
    );
};
