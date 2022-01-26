import { useHistory, useParams, useLocation } from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";

const ContactContent = ({queryUrl, onChange}) => {
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
        },[]
    );

    // set all contacts state
    useEffect(() => {
        if (response !== null) {
            setcontactItem(response.items[0]);
        }
        window.scrollTo(0, 0);

    }, [response]);


    function handleClick() {
        history.push("./");
        onChange(null);
    }
    return (
        <div className="annuaire-content r-content">
            <button type="button" onClick={handleClick}>
                Retour
            </button>
            <article>
            <header>
                    <h2 className="r-content-title">{contactItem.title}</h2>
                    {contactItem.subtitle?
                        <h3 className="r-content-subtitle">{contactItem.subtitle}</h3>
                        : ""
                    }
            </header>
            {contactItem.logo ?
                            <figure>
                            <img className="r-content-img"
                                src={contactItem.logo.scales.thumb.download}
                                alt={contactItem.logo.filename}
                            />
                        </figure>
                        : ""
            }
            </article>
            <div className="contactCard">
                <div className="contactText">
                    <div className="contactTextAll">
                        {contactItem.category ? <span>{contactItem.category}</span> : ""}
                        <div className="adresse">
                            {contactItem.number ? <span>{contactItem.number + " "}</span> : ""}
                            {contactItem.street ? <span>{contactItem.street + ", "}</span> : ""}
                            {contactItem.complement ? (
                                <span>{contactItem.complement + ", "}</span>
                            ) : (
                                ""
                            )}
                            {contactItem.zipcode ? <span>{contactItem.zipcode + " "}</span> : ""}
                            {contactItem.city ? <span>{contactItem.city}</span> : ""}
                        </div>
                        <div className="itineraty">
                            {contactItem.street ? (
                                <a
                                    href={
                                        "https://www.google.com/maps/dir/?api=1&destination=" +
                                        contactItem.street +
                                        "+" +
                                        contactItem.number +
                                        "+" +
                                        contactItem.complement +
                                        "+" +
                                        contactItem.zipcode +
                                        "+" +
                                        contactItem.city +
                                        "+" +
                                        contactItem.country
                                    }
                                >
                                    Itinéraire
                                </a>
                            ) : (
                                ""
                            )}
                        </div>
                        <div className="phones">
                            {contactItem.phones
                                ? contactItem.phones.map((phone) => {
                                      return <span>{phone.number}</span>;
                                  })
                                : ""}
                        </div>
                        <div className="mails">
                            {contactItem.mails
                                ? contactItem.mails.map((mail) => {
                                      return <span>{mail.mail_address}</span>;
                                  })
                                : ""}
                        </div>
                        <div className="topics">
                            {contactItem.topics
                                ? contactItem.topics.map((mail) => {
                                      return <span>{mail.title}</span>;
                                  })
                                : ""}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
export default ContactContent;
