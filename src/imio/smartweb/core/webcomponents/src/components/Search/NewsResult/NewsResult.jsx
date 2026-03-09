import React, { useState, useEffect } from "react";
import useAxios from "../../../hooks/useAxios";
import useIsMobile from "../../../hooks/useIsMobile";
import Highlighter from "react-highlight-words";
import { Translate } from "react-translated";
import Spinner from "../Spinner";

const NewsResult = (props) => {
    const [resultArray, setresultArray] = useState([]);
    const [visibleCount, setVisibleCount] = useState(1);
    const [announcement, setAnnouncement] = useState("");
    const isMobile = useIsMobile();
    const { response, error, isLoading } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.url + "/@search?&_core=news&b_size=100", //props.queryUrl*/,
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
            props.onCount?.(response.items.length);
        } else {
            setresultArray([]);
        }
    }, [response]); // eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        setVisibleCount(1);
    }, [props.urlParams]);

    return (
        <div className="search-news">
            <div className="r-search-header">
                <h2 className="r-search-header-title">
                    <Translate text="Actualités" />
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
                <ul id="news-results-list" className="r-search-list" aria-label="Liste des résultats pour les actualités">
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
            <div role="status" aria-live="polite" aria-atomic="true" className="r-sr-only">
                {announcement}
            </div>
            {isMobile && resultArray.length > visibleCount && (
                <button
                    type="button"
                    className="r-load-more-btn"
                    aria-controls="news-results-list"
                    onClick={() => {
                        const next = visibleCount + 3;
                        setVisibleCount(next);
                        setAnnouncement(`${Math.min(next, resultArray.length)} / ${resultArray.length}`);
                    }}
                >
                    <Translate text="Afficher plus" />
                </button>
            )}
        </div>
    );
};
export default NewsResult;
