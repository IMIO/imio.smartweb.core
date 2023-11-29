import React, { useEffect, useState } from "react";
import moment from "moment";
import Moment from "react-moment";
import { Link } from "react-router-dom";
import removeAccents from "remove-accents";
import ReactMarkdown from 'react-markdown';

const NewsCard = ({ item }) => {
    const [limitDescription, setLimitDescription] = useState();
    const numberLimit = 150;
    const title = item.title && item.title;
    const description = item.description && item.description;
    const category = item.taxonomy_contact_category
        ? item.taxonomy_contact_category[0].title
        : "";
    useEffect(() => {
        if (description.length >= numberLimit) {
            setLimitDescription(description.substring(0, numberLimit) + "...");
        } else {
            setLimitDescription(description);
        }
    }, [item]);
    moment.locale('fr')
    const created = moment(item.created).startOf('minute').fromNow();
    const lastModified = moment(item.modified).startOf('minute').fromNow();
    return (
        <div className="r-list-item">
            <div
                className={item.image_preview_scale?"r-item-img":"r-item-img r-item-img-placeholder"}
                style={{
                    backgroundImage: item.image_preview_scale
                        ? "url(" + item.image_preview_scale + ")"
                        : "",
                }}
            />
            <div className="r-item-text">
                {category ? <span className="r-item-categorie">{category}</span> : ""}
                <span className="r-item-title">{title}</span>
                {description ? 
                    <ReactMarkdown className="r-item-description">{limitDescription}</ReactMarkdown> 
                    : ""
                }
                <Link
                    className="r-item-read-more"
                    style={{ textDecoration: "none" }}
                    to={{
                        pathname: removeAccents(
                            item.title.replace(/\s/g, "-").toLowerCase()
                        ),
                        search: `?u=${item.UID}`,
                        state: {
                            idItem: item.UID,
                        },
                    }}
                >
                    {
                        created === lastModified ?
                        (
                        <div className="r-card-date-last">
                            <span>Publié </span>
                            <span>{created}</span>
                        </div>
                        ):
                        (
                        <div className="r-card-date-last">
                            <span>Actualisé </span>
                            <span>{lastModified}</span>
                        </div>
                        )
                    }
                </Link>
            </div>
            <div className="r-item-arrow-more"></div>
        </div>
    );
};

export default NewsCard;