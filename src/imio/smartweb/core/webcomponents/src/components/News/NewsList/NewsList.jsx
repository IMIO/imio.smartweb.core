import React, { useEffect, useContext } from "react";
import NewsCard from "../NewsCard/NewsCard";
import { Link } from "react-router-dom";
import removeAccents from "remove-accents";
import { ScrollContext } from "../../../hooks/ScrollContext";
const NewsList = ({ itemsArray, onChange, showCategoriesOrTopics }) => {

    const { scrollPos, updateScrollPos } = useContext(ScrollContext);


    function handleClick(event) {
        onChange(event);
        updateScrollPos(window.scrollY);
    }

    useEffect(() => {
        window.scrollTo(
           { top: scrollPos,
            left: 0,
            behavior: 'instant'});
    }, [itemsArray]);
    return (
        <React.Fragment>
            <ul className="r-result-list actu-result-list">
                {itemsArray.map((item, i) => (
                    <li key={i} className="r-list-item-group" onClick={() => handleClick(item.UID)}>
                        <Link
                            className="r-news-list-item-link"
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
                        >
                            <NewsCard
                                item={item}
                                showCategoriesOrTopics={showCategoriesOrTopics}
                                key={item.created}
                            />
                        </Link>
                    </li>
                ))}
            </ul>
        </React.Fragment>
    );
};
export default NewsList;
