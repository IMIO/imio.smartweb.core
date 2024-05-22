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
            <ul className="r-result-list annuaire-result-list">
                {contactArray.map((item, i) => (
                    <li
                        key={i}
                        className="r-list-item-group"
                        onMouseEnter={() => handleHover(item.UID)}
                        onMouseLeave={() => handleHover(null)}
                        onClick={() => handleClick(item.UID)}
                    >
                        <Link
                            className="r-list-item-link"
                            style={{ textDecoration: "none" }}
                            to={{
                                pathname:
                                    "/" +
                                    removeAccents(item.title)
                                        .replace(/[^a-zA-Z ]/g, "")
                                        .replace(/\s/g, "-")
                                        .toLowerCase(),
                                search: `?u=${item.UID}`,
                                state: {
                                    idItem: item.UID,
                                },
                            }}
                        ></Link>
                        <ContactCard item={item} key={item.created} />
                    </li>
                ))}
            </ul>
        </React.Fragment>
    );
};
export default ContactList;
