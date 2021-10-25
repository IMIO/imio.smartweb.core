import React, { useEffect, useState } from "react";
import { HashRouter as Router, Switch, Route, useParams, useLocation } from "react-router-dom";
import { getPath } from "../../utils/url";
import Skeleton from "./Skeleton/Skeleton.jsx";
import Filters from "./Filters/Filter"
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
              const queryString = require('query-string');
        const parsed = queryString.parse(useFilterQuery().toString());
    const [contactArray, setcontactArray] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [hoverId, setHoverId] = useState(null);
    const [params, setParams] = useState({});
    const [filters, setFilters] = useState({});
    const [batchSize, setBatchSize] = useState(5);
    const [refTop, setRefTop] = useState(null);
    const { response, error, isLoading } = useAxios({
        method: "get",
        url: "",
        baseURL: props.queryUrl,
        headers: {
            Accept: "application/json",
        },
        params: params,
    }, [parsed,filters]);

    useEffect(() => {
        if (response !== null) {
            setcontactArray(response.items);
        }
    }, [response]);

    const clickID = (id) => {
        setClickId(id);
    };

    const hoverID = (id) => {
        setHoverId(id);
    };

    const filtersChange = (value) => {
        setFilters(value)
    }
    const callback = () => {
        setBatchSize(batchSize + 5);
    }
    useEffect(() => {

        setParams({ ...filters, 'b_size': batchSize, "fullobjects": 1 })

    }, [filters, batchSize]);
    console.log(parsed)
    console.log(params)



    // console.log(parsed)

    return (
        <Router>
            <div
                className="ref"
                ref={(el) => {
                    if (!el) return;
                    setRefTop(el.getBoundingClientRect().top);
                }}
                style={{ height: `calc(100vh -  ${refTop}px)` }}
            >
                <h1>{props.queryUrl}</h1>
                <div className="r-wrapper r-annuaire-wrapper">
                    <div className="r-result r-annuaire-result">
                        <Switch>
                            <Route path={"/:id"}>
                                <ContactContent onChange={clickID} contactArray={contactArray} />
                            </Route>
                            <Route exact path="*">
                                <div className="r-result-filter annuaire-result-filter">
                                    <Filters url={props.queryFilterUrl} onChange={filtersChange} />
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
                        <ContactMap
                            clickId={clickId}
                            hoverId={hoverId}
                            items={contactArray}
                        />
                    </div>
                </div>
            </div>
        </Router>
    );
};


