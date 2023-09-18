import React, { useState, useEffect } from "react";
import useAxios from "../../../hooks/useAxios";
import Highlighter from "react-highlight-words";

const NewsResult = (props) => {
    const [resultArray, setresultArray] = useState([]);
    const { response, error, isLoading } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.url + "/@search?&_core=news&b_size=100", //props.queryUrl*/,
            headers: {
                Accept: "application/json",
            },
            params: (props.urlParams.SearchableText || props.urlParams.iam || props.urlParams.topics) ? props.urlParams : {},
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
    return (
        <div className="search-news">
            <div className="r-search-header">
                <h2 className="r-search-header-title">Actualités</h2>
                <p className="r-search-header-count">
                    {resultArray ? resultArray.length : "0"} résultats
                </p>
            </div>
            <ul className="r-search-list">
                {resultArray.map((contactItem, i) => (
                    <li key={i} className="r-search-item">
                        <a href={contactItem["_url"]}>
                            <div className="r-search-img">
                                {
                                    contactItem.has_leadimage[0] ? (
                                        <div className="r-search-img" style={{
                                            backgroundImage:"url(" + contactItem.image_url +")"
                                        }}></div>
                                    ):(
                                        <div className="r-search-img no-search-item-img"></div>
                                    )
                                }
                            </div>
                            <Highlighter
                                highlightClassName="r-search-highlighter"
                                searchWords={[props.urlParams.SearchableText]}
                                textToHighlight={contactItem.title}
                            />
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
};
export default NewsResult;
