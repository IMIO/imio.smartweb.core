import React from "react";
import imgPlaceholder from "../../../assets/img-placeholder-bla.png";
import moment from "moment";
import Moment from "react-moment";
const ContactCard = ({ contactItem }) => {
    const title = contactItem.title && contactItem.title;
    const category =
        contactItem.taxonomy_contact_category && contactItem.taxonomy_contact_category[0];
    const start = moment(contactItem.start && contactItem.start);

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
                {contactItem.category ? (
                    <span className="r-item-categorie">{contactItem.category.title}</span>
                ) : (
                    ""
                )}
                <span className="r-item-title">{title}</span>
                {start ? (
                    <span className="r-item-date">
                        <Moment format="DD-MM-YYYY">{start}</Moment>
                    </span>
                ) : (
                    ""
                )}
            </div>
        </div>
    );
};

export default ContactCard;
