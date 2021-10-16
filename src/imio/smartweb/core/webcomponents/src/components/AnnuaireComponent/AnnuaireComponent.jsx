import React, { useEffect, useRef, useState } from "react";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import { getPath } from "../../utils/url";
import Skeleton from "./Skeleton/Skeleton.jsx";
import ContactContent from "./ContactContent/ContactContent";
import ContactList from "./ContactList/ContactList";
import ContactMap from "./ContactMap/ContactMap";
import CategoriesFilter from "./CategoriesFilter/CategoriesFilter";
import TopicsFilter from "./TopicsFilter/TopicsFilter";
import FacilitiesFilter from "./FacilitiesFilter/FacilitiesFilter";
import useAxios from "../../hooks/useAxios";
import "./AnnuaireComponent.scss";

function App() {
    const [contactArray, setcontactArray] = useState([]);
    const [search, setSearch] = useState("");
    const [contactArrayFilter, setcontactArrayFilter] = useState([]);
    const [clickId, setClickId] = useState(null);
    const [hoverId, setHoverId] = useState(null);
    const [params, setParams] = useState({ topics: "education" });
    const inputRef = useRef(null);
    const [refTop, setRefTop] = useState(null);

    const { response, error, isLoading } = useAxios({
        method: "get",
        url: "",
        baseURL:
            "https://annuaire.preprod.imio.be/braine-l-alleud/@search?fullobjects=1&topics=education",
        headers: {
            Accept: "application/json",
        },
        params: params,
    });

    useEffect(() => {
        if (response !== null) {
            setcontactArray(response.items);
        }
    }, [response]);

    const currentPath = getPath();

    const clickID = (id) => {
        setClickId(id);
    };

    const hoverID = (id) => {
        setHoverId(id);
    };

    useEffect(() => {
        setcontactArrayFilter(
            contactArray.filter((contact) =>
                contact.title.toLowerCase().includes(search.toLowerCase())
            )
        );
    }, [search, contactArray]);

    const topicsChange = (value) => {
        if (value === null) {
            setcontactArrayFilter(contactArray);
        } else {
            const cleanArray = contactArray.filter((contact) => contact.topics != null);
            setcontactArrayFilter(
                cleanArray.filter((topics) => topics.topics[0].title.includes(value.value))
            );
        }
    };

    const CategoriesChange = (value) => {
        if (value === null) {
            setcontactArrayFilter(contactArray);
        } else {
            const cleanArray = contactArray.filter(
                (contact) => contact.taxonomy_contact_category != null
            );
            setcontactArrayFilter(
                cleanArray.filter((contact) =>
                    contact.taxonomy_contact_category[0].title.includes(value.value)
                )
            );
        }
    };

    const FacilitiesChange = (value) => {
        if (value === null) {
            setcontactArrayFilter(contactArray);
        } else {
            const cleanArray = contactArray.filter((contact) => contact.facilities != null);
            setcontactArrayFilter(
                cleanArray.filter((contact) => contact.facilities[0].title.includes(value.value))
            );
        }
    };
    console.log("getPath");
    console.log(getPath());
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
                {/* <button onClick={() => setParams({ topics: "sports" })}>change state params</button>
        <div>
          <img className="headerimg" src={header} />
        </div> */}
                <div className="r-wrapper r-annuaire-wrapper">
                    <div className="r-result r-annuaire-result">
                        {/* <form className="contactSearch">
              <label for="fname">Recherche</label>
              <input type="text" placeholder="Mots clés" onChange={(e) => setSearch(e.target.value)} />
            </form> */}

                        <Switch>
                            <Route path={"/:id"}>
                                <ContactContent onChange={clickID} contactArray={contactArray} />
                            </Route>
                            <Route exact path="*">
                                <div className="r-result-filter annuaire-result-filter">
                                    <TopicsFilter
                                        onChange={topicsChange}
                                        contactArray={contactArray}
                                    />
                                    <CategoriesFilter
                                        onChange={CategoriesChange}
                                        contactArray={contactArray}
                                    />
                                    <FacilitiesFilter
                                        onChange={FacilitiesChange}
                                        contactArray={contactArray}
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
                                        contactArray={contactArrayFilter}
                                    />
                                )}
                            </Route>
                        </Switch>
                    </div>
                    <ContactMap clickId={clickId} hoverId={hoverId} items={contactArrayFilter} />
                </div>
            </Router>
        </div>
    );
}

// Thematiques == topi
export default App;

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
