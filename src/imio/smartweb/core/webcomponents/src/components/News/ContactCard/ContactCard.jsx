import React, { useEffect,useState } from "react";

import imgPlaceholder from "../../../assets/img-placeholder-bla.png";
import { Link } from "react-router-dom";
import removeAccents from 'remove-accents';

const ContactCard = ({ contactItem }) => {
    const [limitDescription, setLimitDescription] = useState();
    const numberLimit = 150
    const title = contactItem.title && contactItem.title;
    const description = contactItem.description && contactItem.description;
    const category = contactItem.taxonomy_contact_category
        ? contactItem.taxonomy_contact_category[0].title
        : "";
        useEffect(() => {
            if (description.length >= numberLimit) {
                setLimitDescription(description.substring(0,numberLimit)+"...")
            }else{
                setLimitDescription(description)
            }
        }, [contactItem]);
    return (
        <div className="r-list-item">
            <div
                className="r-item-img"
                style={{
                    backgroundImage: contactItem["@id"]
                        ? "url(" + contactItem["@id"] + "/@@images/image/preview" + ")"
                        : "url(" + imgPlaceholder + ")",
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
                                pathname: removeAccents(contactItem.title.replace(/\s/g, '-').toLowerCase()),
                                search: `?u=${contactItem.UID}`,
                                state: {
                                    idItem: contactItem.UID,
                                },
                            }}
                        >Lire la suite</Link>
            </div>
            <div className="r-item-arrow-more"></div>
        </div>
    );
};

export default ContactCard;
