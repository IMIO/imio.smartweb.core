import React, { useState, useEffect } from "react";
import useAxios from "../../../hooks/useAxios";
import Highlighter from "react-highlight-words";
import imgPlaceholder from "../../../assets/img-placeholder-bla.png";


const NewsResult = (props) => {
    const [resultArray, setresultArray] = useState([]);
    const { response, error, isLoading } = useAxios({
        method: "get",
        url: "",
        baseURL: props.url+'/@search?&_core=news', //props.queryUrl*/,
        headers: {
            Accept: "application/json",
        },
        params: props && props.urlParams,
    }, [props]);

    useEffect(() => {
        if (response !== null) {
            setresultArray(response.items);
        }
    }, [response]);
    return (
        <div className="search-news col-lg-3">
            <div className="r-search-header">
                <h2 className="r-search-header-title">Actualités</h2>
                <p className="r-search-header-count">{resultArray ? resultArray.length : '0'} résultats</p>
            </div>
            <ul className="r-search-list">
                {resultArray.map((contactItem, i) => (
                    <li key={i} className="r-search-item">
                        <a href={contactItem['_url']}>
                        <div
                            className="r-search-img"
                            style={{
                                backgroundImage: !contactItem.has_leadimage
                                    ? "url(" + contactItem['@id'] + "/@@images/image/preview" + ")"
                                    : "url(" + imgPlaceholder + ")",
                            }}
                        />
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
