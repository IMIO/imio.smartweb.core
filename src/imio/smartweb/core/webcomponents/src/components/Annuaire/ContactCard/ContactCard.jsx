import React, { useEffect, useState } from "react";
import { Translate } from "react-translated";

const ContactCard = ({ item, contextAuthenticatedUser }) => {
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
        <>
            {contextAuthenticatedUser === "False" ? (
                <a
                    href={item["@id"]}
                    target="_blank"
                    title="Editer la fiche"
                    className="edit-rest-elements"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        fill="currentColor"
                        class="bi bi-pencil-square"
                        viewBox="0 0 16 16"
                    >
                        <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                        <path
                            fill-rule="evenodd"
                            d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"
                        />
                    </svg>
                </a>
            ) : (
                ""
            )}

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
        </>
    );
};

export default ContactCard;
