import React from "react";
import imgPlaceholder from "../../../assets/img-placeholder-bla.png";

const ContactCard = ({ contactItem }) => {
    const title = contactItem.title && contactItem.title;
    const category =
        contactItem.taxonomy_contact_category && contactItem.taxonomy_contact_category[0];

    const number = contactItem.number ? contactItem.number : "";
    const street = contactItem.street ? contactItem.street : "";
    const complement = contactItem.complement ? contactItem.complement : "";
    const zipcode = contactItem.zipcode ? contactItem.zipcode : "";
    const city = contactItem.city ? contactItem.city : "";
    const country = contactItem.country ? contactItem.country : "";
    const phones = contactItem.phones ? contactItem.phones : "";
    const mails = contactItem.mails ? contactItem.mails : "";
    const topics = contactItem.topics ? contactItem.topics : "";
    // console.log(category)
    return (
        <div className="r-list-item">
            <div
                className="r-item-img"
                style={{
                    backgroundImage: contactItem.image
                        ? "url(" + contactItem.image.scales.preview.download + ")"
                        : "url(" + imgPlaceholder + ")",
                }}
            />

            <div className="r-item-text">
                <span className="r-item-title">{title}</span>
                {category ? <span className="r-item-categorie">{category.title}</span> : ""}
            </div>
        </div>
    );
};

export default ContactCard;
