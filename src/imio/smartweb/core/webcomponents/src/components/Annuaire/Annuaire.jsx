import React, { useEffect, useState,useRef } from "react";
import {HashRouter as Router, Switch, Route} from "react-router-dom";
import Skeleton from "./Skeleton/Skeleton.jsx";
import Filters from "./Filters/Filter";
import ContactContent from "./ContactContent/ContactContent";
import ContactList from "./ContactList/ContactList";
import ContactMap from "./ContactMap/ContactMap";
import useAxios from "../../hooks/useAxios";
import "./Annuaire.scss";
import useFilterQuery from "../../hooks/useFilterQuery";

export default function Annuaire(props) {
    return (
        <Router>
            <AnnuaireView queryFilterUrl={props.queryFilterUrl} queryUrl={props.queryUrl} />
        </Router>
    );
}
function AnnuaireView(props) {
    const queryString = require("query-string");
    const { u, ...parsed } = Object.assign({ b_size: 5, fullobjects: 1 }, queryString.parse(useFilterQuery().toString()))
    const [contactArray, setcontactArray] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [filters, setFilters] = useState(parsed);
    const [hoverId, setHoverId] = useState(null);
    const [batchSize, setBatchSize] = useState(5);
    const [refTop, setRefTop] = useState(null);
    const { response, error, isLoading } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.queryUrl,
            headers: {
                Accept: "application/json",
            },
            params: filters,
        },
        []
    );

    // set all contacts state
    useEffect(() => {
        if (response !== null) {
            setcontactArray(response.items);
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
        setFilters(value);
    };

    // set batch
    const callback = () => {
        setFilters(prevFilters => {
            return { 
              ...prevFilters, 
              b_size: batchSize + 5
            }
          })
    };

    // Map style
    const ref = React.useRef(0)
    let header = document.getElementById('portal-logo');
    let headerHeight = header.offsetHeight
    // coditional list render
    let listRender;
    let MapRender;
    if (contactArray && contactArray.length > 0) {      
        listRender = <ContactList onChange={clickID} contactArray={contactArray}  onHover={hoverID} parentCallback={callback} />;
        MapRender = <ContactMap headerHeight={headerHeight} clickId={clickId} hoverId={hoverId} items={contactArray} />;
        
    } else {
        listRender = <p>Aucun contact n'a été trouvé</p>
    }
    return (
        <Router>
            <div
                className="ref"
                ref={refElem => {
                    if(refElem) {
                        setRefTop(refElem.getBoundingClientRect().top + document.documentElement.scrollTop)
                    }
                }}
            >
                <div className="r-wrapper r-annuaire-wrapper">
                    <div className="r-result r-annuaire-result">
                        <Switch>
                            <Route path={"/:name"}>
                                <ContactContent queryUrl={props.queryUrl} onChange={clickID} />
                            </Route>
                            <Route exact path="*">
                                <div className="r-result-filter annuaire-result-filter">
                                    <Filters
                                        url={props.queryFilterUrl}
                                        activeFilter={filters}
                                        onChange={filtersChange}
                                    />
                                </div>
                                {isLoading ? (
                                    <div>
                                        <Skeleton /> <Skeleton /> <Skeleton />
                                    </div>
                                ) : (
                                    <div>{listRender}</div>
                                )}
                            </Route>
                        </Switch>
                    </div>
                    <div className="r-map annuaire-map" 
                        style={{ marginTop:`-${refTop - headerHeight}px`}}
                    >
                        {MapRender}
                    </div>
                </div>
            </div>
        </Router>
    );
}
