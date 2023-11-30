import React from "react";
import moment from "moment";
import Moment from "react-moment";
const ContactCard = ({ item }) => {
    const title = item.title && item.title;
    const category =
        item.taxonomy_contact_category && item.taxonomy_contact_category[0];
    const start = moment(item.start && item.start);

    const number = item.number ? item.number : "";
    const street = item.street ? item.street : "";
    const complement = item.complement ? item.complement : "";
    const zipcode = item.zipcode ? item.zipcode : "";
    const city = item.city ? item.city : "";
    const country = item.country ? item.country : "";
    const phones = item.phones ? item.phones : "";
    const mails = item.mails ? item.mails : "";
    const topics = item.topics ? item.topics : "";
    return (
        <div className="r-list-item">
            <div
                className={item.image_vignette_scale?"r-item-img":"r-item-img r-item-img-placeholder"}
                style={{
                    backgroundImage: item.image_vignette_scale
                        ? "url(" + item.image_vignette_scale + ")"
                        : "",
                }}
            />

            <div className="r-item-text">
                {start &&
                    <span className="r-item-date">
                        <Moment format="DD-MM-YYYY">{start}</Moment>
                    </span>
                }
                <span className="r-item-title">{title}</span>
                {item.category && <span className="r-item-categorie">{item.category.title}</span>}
            </div>
        </div>
    );
};

export default ContactCard;
