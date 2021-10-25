import { useHistory, useParams,useLocation } from "react-router-dom";
import React, { useEffect, useState } from "react";
import { getPath } from "../../../utils/url";
import useAxios from "../../../hooks/useAxios";


const ContactContent = ({ contactArray, onChange }) => {
    let history = useHistory();
    const { id } = useParams();
    const [contactItem, setcontactItem] = useState({});
    const {pathname, search, hash} = useLocation()
    // const [params, setParams] = useState({});
    // const { response, error, isLoading } = useAxios({
    //     method: "get",
    //     url: "",
    //     baseURL: props.queryUrl,
    //     headers: {
    //         Accept: "application/json",
    //     },
    //     params: params,
    // },[params]);

    // useEffect(() => {
    //     if (response !== null) {
    //         setcontactArray(response.items);
    //     }
    // }, [response]);

    // useEffect(() => {
    //         setParams(response.items);
    // }, [response]);

    useEffect(() => {
        if (contactArray.length > 0) {
            var result = contactArray.filter((obj) => {
                return obj.UID === id;
            });
            setcontactItem(result[0]);
        }
    }, [id, contactArray]);

    function handleClick() {
        history.push(".");
        onChange(null);
    }
    const params = {'@id': getPath()+id}
    return (
        <div className="contact-content">
            <p>The search parameter is : {pathname}</p>
            <button type="button" onClick={handleClick}>
                Go home
            </button>
            <div className="contactCard">
                <div className="contactText">
                    <div className="contactTextTitle">
                        <span className="title">{contactItem.title}</span>
                    </div>
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
