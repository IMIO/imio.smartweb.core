import ContactCard from "../ContactCard/ContactCard";
import { Link } from "react-router-dom";
import React from "react";
import removeAccents from "remove-accents";
const ContactList = ({ contactArray, onChange, parentCallback }) => {
    function handleClick(event) {
        onChange(event);
    }
    return (
        <React.Fragment>
            <ul className="r-result-list actu-result-list">
                {contactArray.map((contactItem, i) => (
                    <li
                        key={i}
                        className="r-list-item-group"
                        onClick={() => handleClick(contactItem.UID)}
                    >
                        <Link
                            className="r-news-list-item-link"
                            style={{ textDecoration: "none" }}
                            to={{
                                pathname: removeAccents(contactItem.title).replace(/[^a-zA-Z ]/g, "").replace(/\s/g, "-").toLowerCase(),
                                search: `?u=${contactItem.UID}`,
                                state: {
                                    idItem: contactItem.UID,
                                },
                            }}
                        >
                        <ContactCard contactItem={contactItem} key={contactItem.created} />
                        </Link>
                    </li>
                ))}
            </ul>
        </React.Fragment>
    );
};
export default ContactList;
