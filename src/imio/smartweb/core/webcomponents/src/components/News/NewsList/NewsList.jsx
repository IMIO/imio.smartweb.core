import React, { useEffect, useContext } from "react";
import NewsCard from "../NewsCard/NewsCard";
import { Link } from "react-router-dom";
import removeAccents from "remove-accents";
import { ScrollContext } from "../../../hooks/ScrollContext";
const NewsList = ({ itemsArray, onChange, showCategoriesOrTopics, contextAuthenticatedUser }) => {
    const { scrollPos, updateScrollPos } = useContext(ScrollContext);

    function handleClick(event) {
        onChange(event);
        updateScrollPos(window.scrollY);
    }

    useEffect(() => {
        window.scrollTo({ top: scrollPos, left: 0, behavior: "instant" });
    }, [itemsArray]);
    return (
        <React.Fragment>
            <ul className="r-result-list actu-result-list">
                {itemsArray.map((item, i) => (
                    <li key={i} className="r-list-item-group" onClick={() => handleClick(item.UID)}>
                        {contextAuthenticatedUser === "False" ? (
                            <a
                                href={item["@id"]}
                                target="_blank"
                                title="Editer la fiche"
                                className="edit-rest-elements edit-rest-elements-news"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="16"
                                    height="16"
                                    fill="currentColor"
                                    class="bi bi-pencil-square"
                                    viewBox="0 0 16 16"
                                >
                                    <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                                    <path
                                        fill-rule="evenodd"
                                        d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"
                                    />
                                </svg>
                            </a>
                        ) : (
                            ""
                        )}
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
                                contextAuthenticatedUser={contextAuthenticatedUser}
                            />
                        </Link>
                    </li>
                ))}
            </ul>
        </React.Fragment>
    );
};
export default NewsList;
