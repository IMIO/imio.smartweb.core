import React, { useEffect, useState } from "react";
import {
    HashRouter as Router,
    useHistory,
    Switch,
    Route,
    useParams,
    useLocation,
} from "react-router-dom";
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
    // let history = useHistory();
    const queryString = require("query-string");
    const parsed = queryString.parse(useFilterQuery().toString());

    const [contactArray, setcontactArray] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [hoverId, setHoverId] = useState(null);
    const [params, setParams] = useState({});
    const [filters, setFilters] = useState(parsed);

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
            params: params,
        },
        [params]
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
    useEffect(() => {
        setParams({ ...filters, b_size: batchSize, fullobjects: 1 });
    }, [filters, batchSize]);
    console.log(response)
    // console.log(params)s

    return (
        <Router>
            {/* <h2>{props.queryFilterUrl}</h2>
            <h2>{props.queryUrl}</h2> */}
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
                                    <ContactList
                                        onChange={clickID}
                                        onHover={hoverID}
                                        contactArray={contactArray}
                                        // onBatching={batchin}
                                        parentCallback={callback}
                                    />
                                )}
                            </Route>
                        </Switch>
                    </div>
                    <div style={{ maxHeight: "500px" }}>
                        <ContactMap clickId={clickId} hoverId={hoverId} items={contactArray} />
                    </div>
                </div>
            </div>
        </Router>
    );
}
