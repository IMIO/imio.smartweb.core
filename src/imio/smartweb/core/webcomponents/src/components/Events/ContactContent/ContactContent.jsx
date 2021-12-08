import { useHistory} from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";
import moment from 'moment'
import Moment from 'react-moment';
const ContactContent = ({queryUrl, onChange }) => {
    let history = useHistory();
    const queryString = require("query-string");
    const parsed = queryString.parse(useFilterQuery().toString());
    const parsed2 = { ...parsed, UID: parsed['u'], fullobjects: 1 };
    const [params, setParams] = useState(parsed2);
    const [contactItem, setcontactItem] = useState({});
    const { response, error, isLoading } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: queryUrl,
            headers: {
                Accept: "application/json",
            },
            params: params,
        },
        []
    );

    // set all contacts state
    useEffect(() => {
        if (response !== null) {
            setcontactItem(response.items[0]);
        }
    }, [response]);

    function handleClick() {
        history.push("./");
        onChange(null);
    }
    const start = moment(contactItem.start);
    const end = moment(contactItem.end);
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
                <div className="r-content-news-info"> 
                    <div class="r-content-date">
                        <div className="r-content-date-start">
                            <span>Du </span>
                            <Moment format='DD-MM-YYYY'>{start}</Moment>
                        </div>
                        <div className="r-content-date-end">
                            <span>au </span>
                            <Moment format='DD-MM-YYYY'>{end}</Moment>
                        </div>
                    </div>
                    <div className="r-content-book">
                        <a href={contactItem.ticket_url}>Billetterie</a>
                    </div>
                    <div className="r-content-event-link">
                        <a href={contactItem.event_url}>Lien de l'événement</a>
                    </div>
                    <div className="r-content-online-participation">
                        <a href={contactItem.online_participation}>Participation en ligne</a>
                    </div>
                </div>
                <div class="r-content-text"
                    dangerouslySetInnerHTML={{
                        __html: contactItem.text && contactItem.text.data
                    }}></div>
            </article>
        </div>
    );
};
export default ContactContent;
