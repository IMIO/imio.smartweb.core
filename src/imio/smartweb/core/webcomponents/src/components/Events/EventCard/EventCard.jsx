import React from "react";
import moment from "moment";
import { Translate } from "react-translated";

const ContactCard = ({ item, showCategoriesOrTopics }) => {
    moment.locale("be");
    const title = item.title && item.title;
    const start = moment.utc(item.start).format("DD-MM-YYYY");
    const end = moment.utc(item.end).format("DD-MM-YYYY");
    return (
        <div className="r-list-item">
            <div
                className={
                    item.image_vignette_scale ? "r-item-img" : "r-item-img r-item-img-placeholder"
                }
                style={{
                    backgroundImage: item.image_vignette_scale
                        ? "url(" + item.image_vignette_scale + ")"
                        : "",
                }}
            />

            <div className="r-item-text">
                {start && (
                    <span className="r-item-date">
                        {start === end ? (
                            start
                        ) : (
                            <>
                                {start} <Translate text="au" /> {end}
                            </>
                        )}
                    </span>
                )}
                <span className="r-item-title">{title}</span>
                {showCategoriesOrTopics === "topic" ? (
                    item.topics && item.topics[0] && (
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
            </div>
        </div>
    );
};

export default ContactCard;
