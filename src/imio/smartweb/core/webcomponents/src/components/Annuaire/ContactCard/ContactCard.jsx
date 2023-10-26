import React, { useEffect, useState } from "react";

const ContactCard = ({ contactItem }) => {
    const [image, setImage] = useState(new Image());
    const [imageClassName, setImageClassName] = useState("");
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
    let countryTitle = contactItem.country && contactItem.country.title
    let itineraryLink =
        "https://www.google.com/maps/dir/?api=1&destination=" +
        contactItem.street +
        "+" +
        contactItem.number +
        "+" +
        contactItem.complement +
        "+" +
        contactItem.zipcode +
        "+" +
        contactItem.city +
        "+" +
        countryTitle

    itineraryLink = itineraryLink.replaceAll('+null', '')

    // Set image and image className
    useEffect(() => {
        const loadImage = async () => {
            const img = new Image();
            const src = contactItem.image_affiche_scale || contactItem.logo_thumb_scale || "";

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

        if (contactItem.image_affiche_scale || contactItem.logo_thumb_scale) {
            loadImage();
        }
    }, [contactItem]);
    
    return (
        <div className="r-list-item">
            {image && image.src
                ? <>
                    <div className="r-item-img">
                        <div className="r-content-figure-blur"
                            style={{ backgroundImage: "url(" + image.src + ")" }}
                        />
                        <img className={"r-content-figure-img" + " " + imageClassName}
                            src={image.src} />
                    </div>
                </>
                : <>
                    <div className="r-item-img r-item-img-placeholder"></div>
                </>
            }
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
                                <a href={itineraryLink} target="_blank">
                                    Itinéraire
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
