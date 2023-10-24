import React, { useEffect, useState, useRef } from "react";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import Filters from "./Filters/Filter";
import ContactContent from "./ContactContent/ContactContent";
import ContactList from "./ContactList/ContactList";
import ContactMap from "./ContactMap/ContactMap";
import useAxios from "../../hooks/useAxios";
import "./Annuaire.scss";
import useFilterQuery from "../../hooks/useFilterQuery";
import { Provider, Translate } from "react-translated";
import translation from '../../utils/translation';

export default function Annuaire(props) {
    return (
        <Router>
            <Provider language={props.currentLanguage} translation={translation}>
                <AnnuaireView
                    queryFilterUrl={props.queryFilterUrl}
                    queryUrl={props.queryUrl}
                    proposeUrl={props.proposeUrl}
                    batchSize={props.batchSize}
                    displayMap={props.displayMap}
                />
            </Provider>
        </Router>
    );
}
function AnnuaireView(props) {
    const queryString = require("query-string");
    const { u, ...parsed } = Object.assign(
        { b_start: 0, fullobjects: 1 },
        queryString.parse(useFilterQuery().toString())
    );
    const [contactArray, setcontactArray] = useState([]);
    const [contactNumber, setcontactNumber] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [hoverId, setHoverId] = useState(null);
    const [filters, setFilters] = useState(parsed);
    const [batchStart, setBatchStart] = useState(0);
    const [loadMoreLaunch, setLoadMoreLaunch] = useState(false);
    const displayMap =  props.displayMap === "True" ? true : false;
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

    // set all contacts state
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

    // set state hoverId when hover on list element
    const hoverID = (id) => {
        setHoverId(id);
    };

    // set state filters when active filter selection
    const filtersChange = (value) => {
        setLoadMoreLaunch(false);
        setBatchStart((batchStart) => 0);
        setFilters(value);
        window.scrollTo(0, 0);
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

    // filter top style
    let portalHeader = document.getElementById("portal-header");
    let portalHeaderHeight = portalHeader.offsetHeight;

    const filterRef = useRef();
    const [style, setStyle] = React.useState({ height:0 });
    useEffect(() => {
        setStyle({
            height: filterRef.current.clientHeight,
        });
    }, [filterRef.current]);

    // coditional list render
    let listRender;
    let MapRender;
    if (contactArray && contactArray.length > 0) {
        listRender = (
            <ContactList onChange={clickID} contactArray={contactArray} onHover={hoverID} />
        );
        MapRender = (
            <ContactMap
                headerHeight={style.height + portalHeaderHeight}
                clickId={clickId}
                hoverId={hoverId}
                items={contactArray}
            />
        );
    } else if (!isLoading) {
        listRender = <p><Translate text="Aucun contact n'a été trouvé" /></p>;
    }

    const divLoader = <div className="lds-roller-container"><div className="lds-roller"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div></div>;
    return (
        <Router>
            <div className={`ref ${displayMap ? "view-map" : "no-map"}`}>
                <div
                    className="r-result-filter-container"
                    ref={filterRef}
                    style={{ top: portalHeaderHeight }}
                >
                    <div
                        id="r-result-filter"
                        className="r-result-filter container annuaire-result-filter"
                    >
                        <Filters
                            url={props.queryFilterUrl}
                            activeFilter={filters}
                            onChange={filtersChange}
                        />
                        {props.proposeUrl &&
                            (
                                <div className="r-add-contact">
                                    <a target="_blank" href={props.proposeUrl}><Translate text='Proposer un contact' /></a>
                                </div>
                            )
                        }
                        {contactNumber > 0 ? (
                            <p className="r-results-numbers">
                                <span>{contactNumber}</span>
                                {contactNumber > 1 
                                ? <Translate text='contacts trouvés' />
                                : <Translate text='contact trouvé' />}
                            </p>
                        ) : (
                            <p className="r-results-numbers"><Translate text='Aucun résultat' /></p>
                        )}
                    </div>
                </div>
                <Switch>
                    <Route path={"/:name"}>
                        <div className="r-wrapper container r-annuaire-wrapper">
                            <div className="r-result r-annuaire-result">
                                <ContactContent queryUrl={props.queryUrl} onChange={clickID} />
                            </div>
                            {displayMap && <div
                                className="r-map annuaire-map"
                                style={{
                                    top: style.height + portalHeaderHeight,
                                    height: "calc(100vh-" + style.height + portalHeaderHeight,
                                }}
                            >
                                {MapRender}
                            </div>}
                        </div>
                    </Route>
                    <Route exact path="*">
                        <div className="r-wrapper container r-annuaire-wrapper">
                            <div className="r-result r-annuaire-result">
                                <div>{listRender}</div>
                                <div className="r-load-more">
                                    {contactNumber - props.batchSize > batchStart ? (
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
                            </div>
                            {displayMap && <div
                                className="r-map annuaire-map"
                                style={{
                                    top: style.height + portalHeaderHeight,
                                    height: "calc(100vh-" + style.height + portalHeaderHeight,
                                }}
                            >
                                {MapRender}
                            </div>}
                        </div>
                    </Route>
                </Switch>
            </div>
        </Router>
    );
}
