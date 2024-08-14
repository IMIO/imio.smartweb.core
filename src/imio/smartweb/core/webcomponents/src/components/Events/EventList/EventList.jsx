import React, { useEffect, useContext } from "react";
import EventCard from "../EventCard/EventCard";
import { Link } from "react-router-dom";
import removeAccents from "remove-accents";
import { ScrollContext } from "../../../hooks/ScrollContext";
const ContactList = ({
    itemsArray,
    onChange,
    onHover,
    showCategoriesOrTopics,
    contextAuthenticatedUser,
}) => {
    const { scrollPos, updateScrollPos } = useContext(ScrollContext);

    function handleClick(event) {
        onChange(event);
        updateScrollPos(window.scrollY);
    }

    function handleHover(event) {
        onHover(event);
    }

    useEffect(() => {
        window.scrollTo({ top: scrollPos, left: 0, behavior: "instant" });
    }, [itemsArray]);

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
                            contextAuthenticatedUser={contextAuthenticatedUser}
                        />
                    </li>
                ))}
            </ul>
        </React.Fragment>
    );
};
export default ContactList;
