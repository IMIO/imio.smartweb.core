import NewsCard from "../NewsCard/NewsCard";
import { Link } from "react-router-dom";
import React from "react";
import removeAccents from "remove-accents";
const NewsList = ({ itemsArray, onChange, showCategoriesOrTopics }) => {
    function handleClick(event) {
        onChange(event);
    }
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
