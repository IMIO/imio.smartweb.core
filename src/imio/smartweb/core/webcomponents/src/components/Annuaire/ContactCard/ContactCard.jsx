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
                <div className="r-item-all">
                    <div className="r-item-adresse">
                        {number ? <span>{number + " "}</span> : ""}
                        {street ? <span>{street + ", "}</span> : ""}
                        {complement ? <span>{complement + ", "}</span> : ""}
                        <br />
                        {zipcode ? <span>{zipcode + " "}</span> : ""}
                        {city ? <span>{city}</span> : ""}
                        <div className="itineraty">
                            {street ? (
                                <a
                                    href={
                                        "https://www.google.com/maps/dir/?api=1&destination=" +
                                        street +
                                        "+" +
                                        number +
                                        "+" +
                                        complement +
                                        "+" +
                                        zipcode +
                                        "+" +
                                        city +
                                        "+" +
                                        country
                                    }
                                >
                                    Itinéraire
                                </a>
                            ) : (
                                ""
                            )}
                        </div>
                    </div>
                    <div className="r-item-contact">
                        <div className="phones">
                            {phones
                                ? phones.map((phone, i) => {
                                      return <span key={i}>{phone.number}</span>;
                                  })
                                : ""}
                        </div>
                        <div className="mails">
                            {mails
                                ? mails.map((mail, i) => {
                                      return <span key={i}>{mail.mail_address}</span>;
                                  })
                                : ""}
                        </div>
                        <div className="topics">
                            {topics
                                ? topics.map((mail, i) => {
                                      return <span key={i}>{mail.title}</span>;
                                  })
                                : ""}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ContactCard;
