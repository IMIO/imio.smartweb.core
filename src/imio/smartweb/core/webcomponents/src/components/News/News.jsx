import React, { useEffect, useState } from "react";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import { getPath } from "../../utils/url";
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
            <NewsView queryFilterUrl={props.queryFilterUrl} queryUrl={props.queryUrl} />
        </Router>
    );
}

const NewsView = (props) => {
    const queryString = require("query-string");
    const parsed = queryString.parse(useFilterQuery().toString());
    const [contactArray, setcontactArray] = useState([]);
    const [clickId, setClickId] = useState(null);
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

    useEffect(() => {
        if (response !== null) {
            setcontactArray(response.items);
        }
    }, [response]);

    const clickID = (id) => {
        setClickId(id);
    };

    const filtersChange = (value) => {
        setFilters(value);
    };
    const callback = () => {
        setBatchSize(batchSize + 5);
    };
    useEffect(() => {
        setParams({ ...filters, b_size: batchSize });
    }, [filters, batchSize]);
    return (
        <div
            className="ref"
            ref={(el) => {
                if (!el) return;
                setRefTop(el.getBoundingClientRect().top);
            }}
            style={{ height: `calc(100vh -  ${refTop}px)` }}
        >   
            <Router>
                <div className="r-wrapper r-annuaire-wrapper">
                    <div className="r-result r-annuaire-result">
                        <Switch>
                            <Route path={"/:name"}>
                                <ContactContent onChange={clickID} queryUrl={props.queryUrl} />
                            </Route>
                            <Route exact path="*">
                                <div className="r-result-filter annuaire-result-filter">
                                    <Filters 
                                    url={props.queryFilterUrl}
                                    activeFilter={filters}
                                    onChange={filtersChange} />
                                </div>
                                {isLoading ? (
                                    <div>
                                        <Skeleton /> <Skeleton /> <Skeleton />
                                    </div>
                                ) : (
                                    <ContactList
                                        onChange={clickID}
                                        contactArray={contactArray}
                                        parentCallback={callback}
                                    />
                                )}
                            </Route>
                        </Switch>
                    </div>
                </div>
            </Router>
        </div>
    );
};

