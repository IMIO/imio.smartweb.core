import React, { useEffect, useState } from "react";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import Skeleton from "./Skeleton/Skeleton.jsx";
import Filters from "./Filters/Filter";
import ContactContent from "./ContactContent/ContactContent";
import ContactList from "./ContactList/ContactList";
import useAxios from "../../hooks/useAxios";
import "./News.scss";
import useFilterQuery from "../../hooks/useFilterQuery";
import { Provider, Translate } from "react-translated";
import translation from '../../utils/translation';

export default function News(props) {
    return (
        <Router>
            <Provider language="fr" translation={translation}>
                <NewsView
                    queryFilterUrl={props.queryFilterUrl}
                    queryUrl={props.queryUrl}
                    proposeUrl={props.proposeUrl}
                    batchSize={props.batchSize}
                />
            </Provider>
        </Router>
    );
}
const NewsView = (props) => {
    const queryString = require("query-string");
    const { u, ...parsed } = Object.assign(
        { b_start: 0, fullobjects: 1 },
        queryString.parse(useFilterQuery().toString())
    );
    const [contactArray, setcontactArray] = useState([]);
    const [contactNumber, setcontactNumber] = useState([]);
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
                setcontactArray((contactArray) => [...contactArray, ...response.items]);
            } else {
                setcontactArray(response.items);
            }
            setcontactNumber(response.items_total);
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
        setBatchStart((batchStart) => batchStart + props.batchSize);
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
    if (contactArray && contactArray.length > 0) {
        listRender = <ContactList onChange={clickID} contactArray={contactArray} />;
    } else {
        listRender = <p><Translate text="Aucune actualité n'a été trouvée" /></p>;
    }
    return (
        <div>
            <Router>
                <div className="r-wrapper r-actu-wrapper">
                    <div className="r-result r-annuaire-result">
                        <Switch>
                            <Route path={"/:name"}>
                                <ContactContent
                                    onChange={clickID}
                                    onReturn={filtersChange}
                                    queryUrl={props.queryUrl}
                                />
                            </Route>
                            <Route exact path="*">
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
                                    {contactNumber > 0 ? (
                                        <p className="r-results-numbers">
                                            <span>{contactNumber}</span>{" "}
                                            {contactNumber > 1
                                                ? <Translate text=' Actualités trouvées' />
                                                : <Translate text=' Actualité trouvée' />}
                                        </p>
                                    ) : (
                                        <p className="r-results-numbers"><Translate text='Aucun résultat' /></p>
                                    )}
                                </div>
                                <div>{listRender}</div>
                                <div className="r-load-more">
                                    {contactNumber - props.batchSize > batchStart ? (
                                        <button onClick={loadMore} className="btn-grad">
                                            {isLoading ? <Translate text='Chargement...' /> : <Translate text='Plus de résultats' />}
                                        </button>
                                    ) : (
                                        <span className="no-more-result">
                                            {isLoading ? <Translate text='Chargement...' /> : ""}
                                        </span>
                                    )}
                                </div>
                            </Route>
                        </Switch>
                    </div>
                </div>
            </Router>
        </div>
    );
};
