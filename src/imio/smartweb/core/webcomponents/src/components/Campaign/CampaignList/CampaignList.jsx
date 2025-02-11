import React, { useEffect, useContext } from "react";
import CampaignCard from "../CampaignCard/CampaignCard";
import { Link } from "react-router-dom";
import removeAccents from "remove-accents";
import { ScrollContext } from "../../../hooks/ScrollContext";
const CampaignList = ({
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
                        onMouseEnter={() => handleHover(item.id)}
                        onMouseLeave={() => handleHover(null)}
                        onClick={() => handleClick(item.id)}
                    >
                        <Link
                            className="r-list-item-link"
                            style={{ textDecoration: "none" }}
                            to={{
                                pathname:
                                    "/" +
                                    removeAccents(item.text)
                                        .replace(/[^a-zA-Z ]/g, "")
                                        .replace(/\s/g, "-")
                                        .toLowerCase(),
                                search: `?u=${item.id}`,
                                state: {
                                    idItem: item.id,
                                },
                            }}
                        ></Link>
                        <CampaignCard
                            item={item.fields}
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
export default CampaignList;
