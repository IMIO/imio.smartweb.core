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
            <NewsView queryFilterUrl={props.queryFilterUrl} queryUrl={props.queryUrl} />
        </Router>
    );
}

const NewsView = (props) => {
    const queryString = require("query-string");
    const parsed = queryString.parse(useFilterQuery().toString());
    const parsed2 ={ ...parsed, UID: parsed['u'],b_size:5,fullobjects:1}
    const [contactArray, setcontactArray] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [filters, setFilters] = useState(parsed2);
    const [batchSize, setBatchSize] = useState(5);
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


    // coditional list render
    let listRender;
    if (contactArray && contactArray.length > 0) {      
        listRender = <ContactList onChange={clickID} contactArray={contactArray} parentCallback={callback} />;
        
    } else {
        listRender = <p>Aucun actulité n'a été trouvé</p>
    }

    return (
        <div>  
            <Router>
                <div className="r-wrapper r-actu-wrapper">
                    <div className="r-result r-annuaire-result">
                        <Switch>
                            <Route path={"/:name"}>
                                <ContactContent onChange={clickID} queryUrl={props.queryUrl} />
                            </Route>
                            <Route exact path="*">
                                <div className="r-result-filter actu-result-filter">
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
                                    <div>{listRender}</div>
                                )}
                            </Route>
                        </Switch>
                    </div>
                </div>
            </Router>
        </div>
    );
};

