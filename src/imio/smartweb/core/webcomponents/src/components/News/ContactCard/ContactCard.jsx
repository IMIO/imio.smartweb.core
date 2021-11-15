import React from "react";
import imgPlaceholder from "../../../assets/img-placeholder-bla.png";

const ContactCard = ({ contactItem }) => {
    const title = contactItem.title && contactItem.title;
    const description = contactItem.description && contactItem.description;

    const category = contactItem.taxonomy_contact_category
        ? contactItem.taxonomy_contact_category[0].title
        : "";
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
                {description ? <span className="r-item-title">{category}</span> : ""}
            </div>
        </div>
    );
};

export default ContactCard;
