import React, { useEffect, useState } from "react";
import { Translate } from "react-translated";

const ContactCard = ({ item }) => {
    const [image, setImage] = useState(new Image());
    const [imageClassName, setImageClassName] = useState("");
    const title = item.title && item.title;
    const category = item.taxonomy_contact_category && item.taxonomy_contact_category[0];
    const number = item.number ? item.number : "";
    const street = item.street ? item.street : "";
    const complement = item.complement ? item.complement : "";
    const zipcode = item.zipcode ? item.zipcode : "";
    const city = item.city ? item.city : "";
    const phones = item.phones ? item.phones : "";
    const mails = item.mails ? item.mails : "";
    const topics = item.topics ? item.topics : "";
    let countryTitle = item.country && item.country.title;
    let itineraryLink =
        "https://www.google.com/maps/dir/?api=1&destination=" +
        item.street +
        "+" +
        item.number +
        "+" +
        item.complement +
        "+" +
        item.zipcode +
        "+" +
        item.city +
        "+" +
        countryTitle;

    itineraryLink = itineraryLink.replaceAll("+null", "");

    // Set image and image className
    useEffect(() => {
        const loadImage = async () => {
            const img = new Image();
            const src = item.image_affiche_scale || item.logo_thumb_scale || "";

            img.src = src;

            try {
                await img.decode(); // Wait for the image to be decoded
                setImage(img);
                const imgClassName = img.width < img.height ? "img-contain" : "img-cover";
                setImageClassName(imgClassName);
            } catch (error) {
                // Handle image loading errors here
                console.error("Error loading image:", error);
            }
        };

        if (item.image_affiche_scale || item.logo_thumb_scale) {
            loadImage();
        }
    }, [item]);

    return (
        <div className="r-list-item">
            {image && image.src ? (
                <>
                    <div className="r-item-img">
                        <div
                            className="r-content-figure-blur"
                            style={{ backgroundImage: "url(" + image.src + ")" }}
                        />
                        <img
                            className={"r-content-figure-img" + " " + imageClassName}
                            src={image.src}
                            alt=""
                        />
                    </div>
                </>
            ) : (
                <>
                    <div className="r-item-img r-item-img-placeholder"></div>
                </>
            )}
            <div className="r-item-text">
                <span className="r-item-title">{title}</span>
                {category ? <span className="r-item-categorie">{category.title}</span> : ""}
                <div className="r-item-all">
                    {street ? (
                        <div className="r-item-adresse">
                            {number ? <span>{number + " "}</span> : ""}
                            {street ? <span>{street + ", "}</span> : ""}
                            {complement ? <span>{complement + ", "}</span> : ""}
                            <br />
                            {zipcode ? <span>{zipcode + " "}</span> : ""}
                            {city ? <span>{city}</span> : ""}
                            <div className="itineraty">
                                <a href={itineraryLink} target="_blank" rel="noreferrer">
                                    <Translate text="Itinéraire" />
                                </a>
                            </div>
                        </div>
                    ) : (
                        ""
                    )}
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
                            ? topics.slice(0, 3).map((mail, i) => {
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
