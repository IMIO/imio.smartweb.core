import React, { useEffect, useState } from "react";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import Skeleton from "./Skeleton/Skeleton.jsx";
import Filters from "./Filters/Filter";
import ContactContent from "./ContactContent/ContactContent";
import ContactList from "./ContactList/ContactList";
import useAxios from "../../hooks/useAxios";
import "./News.scss";
import useFilterQuery from "../../hooks/useFilterQuery";

export default function News(props) {
    return (
        <Router>
            <NewsView queryFilterUrl={props.queryFilterUrl} queryUrl={props.queryUrl+"?b_size=10"} />
        </Router>
    );
}
const NewsView = (props) => {
    const queryString = require("query-string");
    const { u, ...parsed } = Object.assign({ b_start: 0, fullobjects: 1 }, queryString.parse(useFilterQuery().toString()))
    const [contactArray, setcontactArray] = useState([]);
    const [contactNumber, setcontactNumber] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [filters, setFilters] = useState(parsed);
    const [batchStart, setBatchStart] = useState(0);
    const [loadMoreLaunch, setLoadMoreLaunch] = useState(false);
    const { response, error, isLoading,isMore} = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.queryUrl,
            headers: {
                Accept: "application/json",
            },
            params: filters,
            load:loadMoreLaunch,
        },
        []
    );

    // set all news in state
    useEffect(() => {
        if (response !== null) {
            if(isMore){
                setcontactArray((contactArray) => [...contactArray, ...response.items]);
            }else{
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
        setBatchStart((batchStart) => batchStart + 10);
        setLoadMoreLaunch(true);
    };
    console.log(batchStart)
    console.log(isMore)

    // Update filters Batch
    useEffect(() => {
        setFilters(prevFilters => {
            return { 
              ...prevFilters, 
              b_start: batchStart
            }
          })
    }, [batchStart]);
    // coditional list render
    let listRender;
    if (contactArray && contactArray.length > 0) {
        listRender = <ContactList onChange={clickID} contactArray={contactArray} />;

    } else {
        listRender = <p>Aucune actulité n'a été trouvée</p>
    }
    return (
        <div>
            <Router>
                <div className="r-wrapper r-actu-wrapper">
                    <div className="r-result r-annuaire-result">
                        <Switch>
                            <Route path={"/:name"}>
                                <ContactContent onChange={clickID} onReturn={filtersChange} queryUrl={props.queryUrl} />
                            </Route>
                            <Route exact path="*">
                                <div className="r-result-filter actu-result-filter">
                                    <Filters
                                        url={props.queryFilterUrl}
                                        activeFilter={filters}
                                        onChange={filtersChange} />
                                        {contactNumber > 0 ? (
                                            <p className="r-results-numbers"><span>{contactNumber}</span> {contactNumber > 1?'Actualités trouvées':'Actualité trouvée'}</p>
                                        ) : (
                                            <p className="r-results-numbers">Aucun résultat</p>
                                        )}
                                </div>
                                {/* {isLoading ? (
                                    <div>
                                        <Skeleton /> <Skeleton /> <Skeleton />
                                    </div>
                                ) : (
                                )} */}
                                <div>{listRender}</div>
                                <div className="r-load-more">
                                    {(contactNumber -10) > batchStart ? (
                                        <button onClick={loadMore}  className="btn-grad">
                                            {isLoading ? 'Chargement...' : 'Plus de résultats'}
                                        </button>
                                     ):(
                                        <span className="no-more-result">
                                            {isLoading ? 'Chargement...' : ''}
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

