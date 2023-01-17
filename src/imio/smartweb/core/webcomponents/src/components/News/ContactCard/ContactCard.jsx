import React, { useEffect, useState } from "react";
import moment from "moment";
import Moment from "react-moment";
import imgPlaceholder from "../../../assets/img-placeholder-bla.png";
import { Link } from "react-router-dom";
import removeAccents from "remove-accents";

const ContactCard = ({ contactItem }) => {
    const [limitDescription, setLimitDescription] = useState();
    const numberLimit = 150;
    const title = contactItem.title && contactItem.title;
    const description = contactItem.description && contactItem.description;
    const category = contactItem.taxonomy_contact_category
        ? contactItem.taxonomy_contact_category[0].title
        : "";
    useEffect(() => {
        if (description.length >= numberLimit) {
            setLimitDescription(description.substring(0, numberLimit) + "...");
        } else {
            setLimitDescription(description);
        }
    }, [contactItem]);
    moment.locale('fr')
    const created = moment(contactItem.created).startOf('minute').fromNow();
    const lastModified = moment(contactItem.modified).startOf('minute').fromNow();
    return (
        <div className="r-list-item">
            <div
                className={contactItem.image?"r-item-img":"r-item-img r-item-img-placeholder"}
                style={{
                    backgroundImage: contactItem.image
                        ? "url(" + contactItem.image.scales.preview.download + ")"
                        : "",
                }}
            />
            <div className="r-item-text">
                {category ? <span className="r-item-categorie">{category}</span> : ""}
                <span className="r-item-title">{title}</span>
                {description ? <p className="r-item-description">{limitDescription}</p> : ""}
                <Link
                    className="r-item-read-more"
                    style={{ textDecoration: "none" }}
                    to={{
                        pathname: removeAccents(
                            contactItem.title.replace(/\s/g, "-").toLowerCase()
                        ),
                        search: `?u=${contactItem.UID}`,
                        state: {
                            idItem: contactItem.UID,
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

export default ContactCard;
