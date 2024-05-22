import EventCard from "../EventCard/EventCard";
import { Link } from "react-router-dom";
import React from "react";
import removeAccents from "remove-accents";
const ContactList = ({ itemsArray, onChange, onHover, showCategoriesOrTopics }) => {
    function handleClick(event) {
        onChange(event);
    }

    function handleHover(event) {
        onHover(event);
    }
    return (
        <React.Fragment>
            <ul className="r-result-list event-result-list">
                {itemsArray.map((item, i) => (
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
                        <EventCard
                            item={item}
                            showCategoriesOrTopics={showCategoriesOrTopics}
                            key={item.created}
                        />
                    </li>
                ))}
            </ul>
        </React.Fragment>
    );
};
export default ContactList;
