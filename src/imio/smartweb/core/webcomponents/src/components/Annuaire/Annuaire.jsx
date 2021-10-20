import React, { useEffect, useState } from "react";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import { getPath } from "../../utils/url";
import Skeleton from "./Skeleton/Skeleton.jsx";
import Filters from "./Filters/Filter"
import ContactContent from "./ContactContent/ContactContent";
import ContactList from "./ContactList/ContactList";
import ContactMap from "./ContactMap/ContactMap";
import useAxios from "../../hooks/useAxios";
import "./Annuaire.scss";

const Annuaire = (props) => {
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
    },[params]);

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
        setParams({...filters, 'b_size': batchSize,"fullobjects":1})
       
    }, [filters,batchSize]);

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
                            <Route path={"/:id"}>
                                <ContactContent onChange={clickID} contactArray={contactArray} />
                            </Route>
                            <Route exact path="*">
                                <div className="r-result-filter annuaire-result-filter">
                                    <Filters onChange={filtersChange} />
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
            </Router>
        </div>
    );
};

// Thematiques == topi
export default Annuaire;

// const directoryApi = async () => {
//   try {
//     const contacts = await axios.get('https://annuaire.preprod.imio.be/@search?fullobjects=1', {
//       headers: {
//         "Accept": "application/json"
//       }
//     });
//     setcontactArray(contacts.data.items);
//     setcontactResults(contacts.data.items.length);
//   } catch (error) {

//   }
// };

// useEffect(() => {
//   // setcontactArray(data.items);
//   directoryApi();

//   // eslint-disable-next-line
// }, [contactResults, loadmore]);
