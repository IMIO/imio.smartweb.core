import React, { useState, useEffect } from "react";
import useAxios from "../../../hooks/useAxios";
import Highlighter from "react-highlight-words";

const ContactResult = (props) => {
    const [resultArray, setresultArray] = useState([]);
    const { response, error, isLoading } = useAxios({
        method: "get",
        url: "",
        baseURL: props.url+'/@search?&_core=directory', //props.queryUrl*/,
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
        <div className="search-contact col-3">
            <div className="r-search-header">

                <h2 className="r-search-header-title">Contacts</h2>
                <p className="r-search-header-count">{resultArray ? resultArray.length : '0'} résultats</p>
            </div>
            <ul className="r-search-list">
                {resultArray.map((contactItem, i) => (
                    <li key={i}
                        className="r-search-item"
                    >
                        <a href={contactItem['@id']}>
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
export default ContactResult;