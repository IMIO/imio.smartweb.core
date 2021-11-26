import React, { useEffect, useState } from "react";
import {HashRouter as Router,Switch,Route,} from "react-router-dom";
import Skeleton from "./Skeleton/Skeleton.jsx";
import Filters from "./Filters/Filter";
import ContactContent from "./ContactContent/ContactContent";
import ContactList from "./ContactList/ContactList";
import ContactMap from "./ContactMap/ContactMap";
import useAxios from "../../hooks/useAxios";
import "./Events.scss";
import useFilterQuery from "../../hooks/useFilterQuery";

export default function Events(props) {
    return (
        <Router>
            <EventsView queryFilterUrl={props.queryFilterUrl} queryUrl={props.queryUrl} />
        </Router>
    );
}
function EventsView(props) {
    const queryString = require("query-string");
    const parsed = queryString.parse(useFilterQuery().toString());
    const parsed2 ={ ...parsed, UID: parsed['u'],b_size:5,fullobjects:1}
    const [contactArray, setcontactArray] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [hoverId, setHoverId] = useState(null);
    const [filters, setFilters] = useState(parsed2);
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
        setBatchSize(batchSize + 5);
    };

    // set url param for fetch
    // useEffect(() => {
    //     setParams({ ...filters});
    // }, [filters, batchSize]);

    // coditional list render
    let listRender;
    let MapRender;
    if (contactArray && contactArray.length > 0) {      
        listRender = <ContactList onChange={clickID} contactArray={contactArray}  onHover={hoverID} parentCallback={callback} />;
        MapRender = <ContactMap clickId={clickId} hoverId={hoverId} items={contactArray} />;
        
    } else {
        listRender = <p>Aucun événement n'a été trouvé</p>
    }
    return (
        <Router>
            <div
                className="ref"
                ref={(el) => {
                    if (!el) return;
                    // let bodyRect = document.body.getBoundingClientRect();
                    // let el = element.getBoundingClientRect();
                    // let offset   = el.top - bodyRect.top;
                    setRefTop(el.getBoundingClientRect().top + window.pageYOffse );
                }}
                style={{ height: `calc(100vh -  ${refTop}px)` }}
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
                    <div style={{ maxHeight: "500px" }}>
                        {MapRender}
                    </div>
                </div>
            </div>
        </Router>
    );
}
