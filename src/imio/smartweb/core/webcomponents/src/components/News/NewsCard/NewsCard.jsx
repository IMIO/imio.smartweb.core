import React, { useEffect, useState, useContext } from "react";
import moment from "moment";
import ReactMarkdown from "react-markdown";
import { Translate } from "react-translated";
import { LanguageContext } from "../News.jsx";
const NewsCard = ({ item, showCategoriesOrTopics }) => {
    const [limitDescription, setLimitDescription] = useState();
    const [itemTopic, setItemTopic] = useState(null);

    const numberLimit = 150;
    const title = item.title && item.title;
    const description = item.description || "";

    useEffect(() => {
        if (description.length >= numberLimit) {
            let truncatedDescription = description.substring(0, numberLimit);
            if (description.endsWith("**")) {
                truncatedDescription += "**";
            }
            setLimitDescription(truncatedDescription + "...");
        } else {
            setLimitDescription(description);
        }
        if (item.topics && item.topics.length > 0) {
            setItemTopic(item.topics[0].title);
        } else {
            setItemTopic(null);
        }
    }, [item]);
    moment.locale(useContext(LanguageContext));
    const created = moment(item.effective).startOf("minute").fromNow();
    const lastModified = moment(item.modified).startOf("minute").fromNow();
    return (
        <>
            <div className="r-list-item">
                <div
                    className={
                        item.image_vignette_scale
                            ? "r-item-img"
                            : "r-item-img r-item-img-placeholder"
                    }
                    style={{
                        backgroundImage: item.image_vignette_scale
                            ? "url(" + item.image_vignette_scale + ")"
                            : "",
                    }}
                />
                <div className="r-item-text">
                    <span className="r-item-title">{title}</span>
                    {showCategoriesOrTopics === "topic" ? (
                        itemTopic && (
                            <span className="r-item-categorie">{item.topics[0].title}</span>
                        )
                    ) : showCategoriesOrTopics === "category" ? (
                        item.local_category ? (
                            <span className="r-item-categorie">{item.local_category.title}</span>
                        ) : (
                            item.category && (
                                <span className="r-item-categorie">{item.category.title}</span>
                            )
                        )
                    ) : (
                        ""
                    )}
                    {description ? (
                        <ReactMarkdown className="r-item-description">
                            {limitDescription}
                        </ReactMarkdown>
                    ) : (
                        ""
                    )}
                    <div className="r-item-read-more" style={{ textDecoration: "none" }}>
                        {created === lastModified ? (
                            <div className="r-card-date-last">
                                <span>
                                    <Translate text="Publié" />{" "}
                                </span>
                                <span>{created}</span>
                            </div>
                        ) : (
                            <div className="r-card-date-last">
                                <span>
                                    <Translate text="Actualisé" />{" "}
                                </span>
                                <span>{lastModified}</span>
                            </div>
                        )}
                    </div>
                </div>
                <div className="r-item-arrow-more"></div>
            </div>
        </>
    );
};

export default NewsCard;
