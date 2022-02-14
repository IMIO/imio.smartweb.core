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
                            className="r-list-item-link"
                            style={{ textDecoration: "none" }}
                            to={{
                                pathname: removeAccents(
                                    contactItem.title.replace(/\s/g, "-").toLowerCase()
                                ),
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
