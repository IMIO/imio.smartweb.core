import { useHistory, useParams, useLocation } from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";

const ContactContent = ({ queryUrl, onChange }) => {
    let history = useHistory();
    const queryString = require("query-string");
    const parsed = queryString.parse(useFilterQuery().toString());
    const [params, setParams] = useState({});

    const [contactItem, setcontactItem] = useState({});
    const { response, error, isLoading } = useAxios({
        method: "get",
        url: "",
        baseURL: queryUrl,
        headers: {
            Accept: "application/json",
        },
        params: params,
    });
    useEffect(() => {
        if (response !== null) {
            setcontactItem(response.items[0]);
        }
    }, [response]);

    useEffect(() => {
        setParams({
            UID: parsed.u,
            fullobjects: 1,
        });
    }, []);


    function handleClick() {
        history.push(".");
        onChange(null);
    }
    return (
        <div className="contact-content">
            <button type="button" onClick={handleClick}>
                Go home
            </button>
            <span className="title">{contactItem.title}</span>

        </div>
    );
};
export default ContactContent;
