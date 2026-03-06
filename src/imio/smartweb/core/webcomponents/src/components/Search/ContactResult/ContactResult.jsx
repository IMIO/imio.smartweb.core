import React, { useState, useEffect } from "react";
import useAxios from "../../../hooks/useAxios";
import useIsMobile from "../../../hooks/useIsMobile";
import Highlighter from "react-highlight-words";
import { Translate } from "react-translated";
import Spinner from "../Spinner";

const ContactResult = (props) => {
    const [resultArray, setresultArray] = useState([]);
    const [visibleCount, setVisibleCount] = useState(3);
    const isMobile = useIsMobile();
    const { response, error, isLoading } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.url + "/@search?&_core=directory&b_size=100", //props.queryUrl*/,
            headers: {
                Accept: "application/json",
            },
            params:
                props.urlParams.SearchableText || props.urlParams.iam || props.urlParams.topics
                    ? props.urlParams
                    : {},
        },
        [props]
    );

    useEffect(() => {
        if (response !== null) {
            setresultArray(response.items);
        } else {
            setresultArray([]);
        }
    }, [response]);

    useEffect(() => {
        setVisibleCount(3);
    }, [props.urlParams]);

    return (
        <div className="search-contact">
            <div className="r-search-header">
                <h2 className="r-search-header-title">
                    <Translate text="Contacts" />
                </h2>
                <p className="r-search-header-count">
                    {resultArray.length > 0 ? (
                        <>
                            {" "}
                            {resultArray.length} <Translate text="Résultats" />{" "}
                        </>
                    ) : (
                        <Translate text="Aucun résultat" />
                    )}
                </p>
            </div>
            {isLoading ? (
                <Spinner />
            ) : (
                <ul className="r-search-list">
                    {(isMobile ? resultArray.slice(0, visibleCount) : resultArray).map((item, i) => (
                        <li key={i} className="r-search-item">
                            <a href={item["_url"]}>
                                <div className="r-search-img">
                                    {item.has_leadimage[0] ? (
                                        <div
                                            className="r-search-img"
                                            style={{
                                                backgroundImage: "url(" + item.image_url + ")",
                                            }}
                                        ></div>
                                    ) : (
                                        <div className="r-search-img no-search-item-img"></div>
                                    )}
                                </div>
                                <Highlighter
                                    highlightClassName="r-search-highlighter"
                                    searchWords={[props.urlParams.SearchableText]}
                                    textToHighlight={item.title}
                                />
                            </a>
                        </li>
                    ))}
                </ul>
            )}
            {isMobile && resultArray.length > visibleCount && (
                <button
                    className="r-load-more-btn"
                    onClick={() => setVisibleCount(visibleCount + 3)}
                >
                    <Translate text="Afficher plus" />
                </button>
            )}
        </div>
    );
};
export default ContactResult;
