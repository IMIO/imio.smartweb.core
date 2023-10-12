import ContactCard from "../ContactCard/ContactCard";
import { Link } from "react-router-dom";
import React from "react";
import removeAccents from "remove-accents";
const ContactList = ({ contactArray, onChange, onHover, parentCallback }) => {
    function handleClick(event) {
        onChange(event);
    }

    function handleHover(event) {
        onHover(event);
    }
    return (
        <React.Fragment>
            <ul className="r-result-list event-result-list">
                {contactArray.map((contactItem, i) => (
                    <li
                        key={i}
                        className="r-list-item-group"
                        onMouseEnter={() => handleHover(contactItem.UID)}
                        onMouseLeave={() => handleHover(null)}
                        onClick={() => handleClick(contactItem.UID)}
                    >
                        <Link
                            className="r-list-item-link"
                            style={{ textDecoration: "none" }}
                            to={{
                                pathname: removeAccents(contactItem.title).replace(/[^a-zA-Z ]/g, "").replace(/\s/g, "-").toLowerCase(),
                                search: `?u=${contactItem.UID}`,
                                state: {
                                    idItem: contactItem.UID,
                                },
                            }}
                        ></Link>
                        <ContactCard contactItem={contactItem} key={contactItem.created} />
                    </li>
                ))}
            </ul>
        </React.Fragment>
    );
};
export default ContactList;
