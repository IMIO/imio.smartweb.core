import React from "react";
import moment from "moment";
import { Translate } from "react-translated";

const ContactCard = ({ item, showCategoriesOrTopics, contextAuthenticatedUser }) => {
    moment.locale("be");
    const title = item.title && item.title;
    const start = moment.utc(item.start).format("DD-MM-YYYY");
    const end = moment.utc(item.end).format("DD-MM-YYYY");
    return (
        <>
            {contextAuthenticatedUser === "False" ? (
                <a
                    href={item["@id"]}
                    target="_blank"
                    title="Editer la fiche"
                    className="edit-rest-elements"
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
                        item.topics &&
                        item.topics[0] && (
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
        </>
    );
};

export default ContactCard;
