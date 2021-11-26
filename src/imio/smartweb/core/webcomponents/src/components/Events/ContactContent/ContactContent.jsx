import { useHistory} from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";
import moment from 'moment'
import Moment from 'react-moment';
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

    // set all contacts state
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
        <div className="envent-content r-content">
            <button type="button" onClick={handleClick}>
                Retour
            </button>
            <article>
                <header>
                    <h1 className="r-content-title">{contactItem.title}</h1>
                    <p>{contactItem.description}</p>
                </header>
                <figure>
                    <div className="r-content-img"
                        style={{
                            backgroundImage: contactItem["@id"]
                                ? "url(" + contactItem["@id"] + "/@@images/image/affiche" + ")"
                                : "",
                        }}
                    />
                </figure>
                {/* <div class="r-content-date">
                    <div className="r-content-date-publish">
                        <span>Publié le </span>
                        <Moment format='DD-MM-YYYY'>{publish}</Moment>
                    </div>
                    <div className="r-content-date-last">
                        <span>Modifié le</span>
                        <Moment format='DD-MM-YYYY'>{lastModified}</Moment>
                    </div>
                </div> */}

                <div class="r-content-text"
                    dangerouslySetInnerHTML={{
                        __html: contactItem.text && contactItem.text.data
                    }}></div>
            </article>
        </div>
    );
};
export default ContactContent;
