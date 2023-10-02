import { useHistory } from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";
import ReactMarkdown from 'react-markdown';
import Spotlight from "spotlight.js";
import "../../../../node_modules/flexbin/flexbin.css"
import { Translate } from "react-translated";

const ContactContent = ({ queryUrl, onChange }) => {
    let history = useHistory();
    const queryString = require("query-string");
    const { u, ...parsed } = Object.assign(
        { UID: queryString.parse(useFilterQuery().toString())['u'], fullobjects: 1 },
    );
    const [params, setParams] = useState(parsed);
    const [contactItem, setcontactItem] = useState({});
    const [files, setFiles] = useState(0);
    const [gallery, setGallery] = useState(0);
    const [social, setSocial] = useState([]);
    const [website, setWebsite] = useState([]);
    const [image, setImage] = useState();

    const { response, error, isLoading } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: queryUrl,
            headers: {
                Accept: "application/json",
            },
            params: params,
        },
        []
    );
    useEffect(() => {
        setParams(parsed)
    }, [queryString.parse(useFilterQuery().toString())['u']]);

    // set all contacts state
    useEffect(() => {
        if (response !== null) {
            setcontactItem(response.items[0]);
        }
        window.scrollTo(0, 0);
    }, [response]);

    // set image
    useEffect(() => {
        if (contactItem.image_affiche_scale) {
            const img = new Image();
            img.src = contactItem.image_affiche_scale
            img.onload = () => {
                setImage(img);
            };
        }
    }, [contactItem]);


    // set social link
    useEffect(() => {
        contactItem.urls && setSocial(contactItem.urls.filter(urls => urls.type !== 'website'));
        contactItem.urls && setWebsite(contactItem.urls.filter(urls => urls.type === 'website'));
    }, [contactItem]);

    /// use to set file and gallery items
    useEffect(() => {
        if (contactItem.items && contactItem.items.length > 0) {
            setFiles(contactItem.items.filter(files => files['@type'] === 'File'));
            setGallery(contactItem.items.filter(files => files['@type'] === 'Image'));
        }
    }, [contactItem]);

    function handleClick() {
        history.push("./");
        onChange(null);
    }
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
    return (
        <div className="annuaire-content r-content">
            <button type="button" onClick={handleClick}>
                <Translate text="Retour" />
            </button>
            <article>
                <header>
                    <h2 className="r-content-title">{contactItem.title}</h2>
                    {contactItem.subtitle ? (
                        <h3 className="r-content-subtitle">{contactItem.subtitle}</h3>
                    ) : (
                        ""
                    )}
                </header>
                {contactItem.image_affiche_scale && (
                    <figure className="r-content-figure">
                        <div
                            className="r-content-figure-blur"
                            style={{ backgroundImage: "url(" + contactItem.image_affiche_scale + ")" }} />
                        <img className="r-content-figure-img"
                            src={contactItem.image_affiche_scale}
                            style={{ objectFit: image && image.width >= image.height ? "cover" : "contain" }} />
                    </figure>
                )}

            </article>
            <div className="contactCard">
                <div className="contactText">
                    <div className="r-content-description">
                        <ReactMarkdown>{contactItem.description}</ReactMarkdown>
                    </div>
                    <div className="contactTextAll">
                        <p className="annuaire-info-title">Infos pratiques</p>
                        {contactItem.category ? <span>{contactItem.category}</span> : ""}
                        {contactItem.street ? (
                            <div className="annaire-adresse">
                                <div className="annaire-adresse-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt-fill" viewBox="0 0 16 16">
                                        <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6z" />
                                    </svg>
                                </div>
                                <div className="annaire-adresse-content">
                                    <a href={itineraryLink} target="_blank">
                                        {contactItem.number ? <span>{contactItem.number + " "}</span> : ""}
                                        {contactItem.street ? <span>{contactItem.street + ", "}</span> : ""}
                                        {contactItem.complement ? (
                                            <span>{contactItem.complement + ", "}</span>
                                        ) : (
                                            ""
                                        )}
                                        {contactItem.zipcode ? <span>{contactItem.zipcode + " "}</span> : ""}
                                        {contactItem.city ? <span>{contactItem.city}</span> : ""}
                                    </a>
                                </div>

                            </div>

                        ) : (
                            ""
                        )}

                        {contactItem.phones && contactItem.phones.length > 0
                            ? (<div className="annuaire-phone">
                                <div className="annuaire-phone-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-telephone-fill" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M1.885.511a1.745 1.745 0 0 1 2.61.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.678.678 0 0 0 .178.643l2.457 2.457a.678.678 0 0 0 .644.178l2.189-.547a1.745 1.745 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.634 18.634 0 0 1-7.01-4.42 18.634 18.634 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877L1.885.511z" />
                                    </svg>
                                </div>
                                <div className="annuaire-phone-content">
                                    {contactItem.phones.map((phone) => {
                                        return (
                                            <span>
                                                {phone.label ? phone.label + ": " : ""}
                                                <a href={"tel:" + phone.number}>
                                                    {phone.number}
                                                </a>
                                            </span>
                                        );
                                    })}
                                </div>
                            </div>)
                            : ""}

                        {contactItem.mails && contactItem.mails.length > 0
                            ? <div className="annuaire-website-mails">
                                <div className="annuaire-website-mails-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                                        <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z" />
                                    </svg>
                                </div>
                                <div className="annuaire-website-mails-content">
                                    {contactItem.mails.map((mail) => {
                                        return (
                                            <span>
                                                {mail.label ? mail.label + ": " : ""}
                                                <a href={"mailto:" + mail.mail_address}>
                                                    {mail.mail_address}
                                                </a>
                                            </span>
                                        );
                                    })}
                                </div>
                            </div>
                            : ""}

                        {contactItem.urls && contactItem.urls.length > 0
                            ? <div className="annuaire-website-link">
                                <div className="annuaire-website-link-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-laptop-fill" viewBox="0 0 16 16">
                                        <path d="M2.5 2A1.5 1.5 0 0 0 1 3.5V12h14V3.5A1.5 1.5 0 0 0 13.5 2h-11zM0 12.5h16a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 12.5z" />
                                    </svg>
                                </div>
                                <ul className="annuaire-website-link-content">
                                    {contactItem.urls.filter(url => url.type === "website").map(website => {
                                        return (
                                            <>
                                                <li>
                                                    <a href={website.url} target="_blank">
                                                        {(website.url)}
                                                    </a>
                                                </li>
                                            </>
                                        );
                                    })}
                                </ul>
                            </div>
                            : ""}

                        {/* add social icons */}
                        {social &&
                            <div className="annuaire-social-link">
                                {social.length > 1 ? (
                                    <ul>
                                        {social.map(url => {
                                            return (
                                                <li>
                                                    <a href={url.url} target="_blank">
                                                        {url.type === "facebook" ? (
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
                                                                <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z" />
                                                            </svg>
                                                        )
                                                            : url.type === "instagram" ? (
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-instagram" viewBox="0 0 16 16">
                                                                    <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z" />
                                                                </svg>
                                                            )
                                                                : url.type === "twitter" ? (
                                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-twitter" viewBox="0 0 16 16">
                                                                        <path d="M5.026 15c6.038 0 9.341-5.003 9.341-9.334 0-.14 0-.282-.006-.422A6.685 6.685 0 0 0 16 3.542a6.658 6.658 0 0 1-1.889.518 3.301 3.301 0 0 0 1.447-1.817 6.533 6.533 0 0 1-2.087.793A3.286 3.286 0 0 0 7.875 6.03a9.325 9.325 0 0 1-6.767-3.429 3.289 3.289 0 0 0 1.018 4.382A3.323 3.323 0 0 1 .64 6.575v.045a3.288 3.288 0 0 0 2.632 3.218 3.203 3.203 0 0 1-.865.115 3.23 3.23 0 0 1-.614-.057 3.283 3.283 0 0 0 3.067 2.277A6.588 6.588 0 0 1 .78 13.58a6.32 6.32 0 0 1-.78-.045A9.344 9.344 0 0 0 5.026 15z" />
                                                                    </svg>
                                                                )
                                                                    : url.type === "youtube" ? (
                                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-youtube" viewBox="0 0 16 16">
                                                                            <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z" />
                                                                        </svg>
                                                                    )
                                                                        : url.type === "pinterest" ? (
                                                                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-pinterest" viewBox="0 0 16 16">
                                                                                <path d="M8 0a8 8 0 0 0-2.915 15.452c-.07-.633-.134-1.606.027-2.297.146-.625.938-3.977.938-3.977s-.239-.479-.239-1.187c0-1.113.645-1.943 1.448-1.943.682 0 1.012.512 1.012 1.127 0 .686-.437 1.712-.663 2.663-.188.796.4 1.446 1.185 1.446 1.422 0 2.515-1.5 2.515-3.664 0-1.915-1.377-3.254-3.342-3.254-2.276 0-3.612 1.707-3.612 3.471 0 .688.265 1.425.595 1.826a.24.24 0 0 1 .056.23c-.061.252-.196.796-.222.907-.035.146-.116.177-.268.107-1-.465-1.624-1.926-1.624-3.1 0-2.523 1.834-4.84 5.286-4.84 2.775 0 4.932 1.977 4.932 4.62 0 2.757-1.739 4.976-4.151 4.976-.811 0-1.573-.421-1.834-.919l-.498 1.902c-.181.695-.669 1.566-.995 2.097A8 8 0 1 0 8 0z" />
                                                                            </svg>
                                                                        )
                                                                            : ""
                                                        }
                                                    </a>
                                                </li>)
                                        })}
                                    </ul>
                                ) : (
                                    <div>
                                        <a href={social[0] && social[0].url} target="_blank">
                                            {social[0] && social[0].type === "facebook" ? (
                                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-facebook" viewBox="0 0 16 16">
                                                    <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z" />
                                                </svg>
                                            )
                                                : social[0] && social[0].type === "instagram" ? (
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-instagram" viewBox="0 0 16 16">
                                                        <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z" />
                                                    </svg>
                                                )
                                                    : social[0] && social[0].type === "twitter" ? (
                                                        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-twitter" viewBox="0 0 16 16">
                                                            <path d="M5.026 15c6.038 0 9.341-5.003 9.341-9.334 0-.14 0-.282-.006-.422A6.685 6.685 0 0 0 16 3.542a6.658 6.658 0 0 1-1.889.518 3.301 3.301 0 0 0 1.447-1.817 6.533 6.533 0 0 1-2.087.793A3.286 3.286 0 0 0 7.875 6.03a9.325 9.325 0 0 1-6.767-3.429 3.289 3.289 0 0 0 1.018 4.382A3.323 3.323 0 0 1 .64 6.575v.045a3.288 3.288 0 0 0 2.632 3.218 3.203 3.203 0 0 1-.865.115 3.23 3.23 0 0 1-.614-.057 3.283 3.283 0 0 0 3.067 2.277A6.588 6.588 0 0 1 .78 13.58a6.32 6.32 0 0 1-.78-.045A9.344 9.344 0 0 0 5.026 15z" />
                                                        </svg>
                                                    )
                                                        : social[0] && social[0].type === "youtube" ? (
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-youtube" viewBox="0 0 16 16">
                                                                <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z" />
                                                            </svg>
                                                        )
                                                            : social[0] && social[0].type === "pinterest" ? (
                                                                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-pinterest" viewBox="0 0 16 16">
                                                                    <path d="M8 0a8 8 0 0 0-2.915 15.452c-.07-.633-.134-1.606.027-2.297.146-.625.938-3.977.938-3.977s-.239-.479-.239-1.187c0-1.113.645-1.943 1.448-1.943.682 0 1.012.512 1.012 1.127 0 .686-.437 1.712-.663 2.663-.188.796.4 1.446 1.185 1.446 1.422 0 2.515-1.5 2.515-3.664 0-1.915-1.377-3.254-3.342-3.254-2.276 0-3.612 1.707-3.612 3.471 0 .688.265 1.425.595 1.826a.24.24 0 0 1 .056.23c-.061.252-.196.796-.222.907-.035.146-.116.177-.268.107-1-.465-1.624-1.926-1.624-3.1 0-2.523 1.834-4.84 5.286-4.84 2.775 0 4.932 1.977 4.932 4.62 0 2.757-1.739 4.976-4.151 4.976-.811 0-1.573-.421-1.834-.919l-.498 1.902c-.181.695-.669 1.566-.995 2.097A8 8 0 1 0 8 0z" />
                                                                </svg>
                                                            )
                                                                : ""
                                            }
                                        </a>
                                    </div>
                                )
                                }
                            </div>
                        }

                        {/* add topics */}
                        <div className="topics">
                            {contactItem.topics
                                ? contactItem.topics.map((mail) => {
                                    return <span>{mail.title}</span>;
                                })
                                : ""}
                        </div>

                        {contactItem.logo_thumb_scale ? (
                                <img
                                    className="annuaire-logo"
                                    src={contactItem.logo_thumb_scale}
                                    alt="Logo"
                                />
                        ) : (
                            ""
                        )}
                    </div>
                </div>
                {/* add files to download */}
                {
                    files ? (
                        <div className="r-content-files">
                            {files.map((file) => (
                                <div className="r-content-file">
                                    <a href={file.targetUrl} className="r-content-file-link" rel="nofollow">
                                        <span className="r-content-file-title">{file.title}</span>
                                        {/* <span className="r-content-file-size">{file.file.size}</span> */}
                                        <span className="r-content-file-icon"><svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="#8899a4" stroke-width="2" stroke-linecap="square" stroke-linejoin="arcs"><path d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"></path></svg> </span>
                                    </a>
                                </div>
                            ))}
                        </div>
                    ) : ("")
                }
                {/* add gallery */}
                {
                    gallery ? (
                        <div className="r-content-gallery">
                            <div className="spotlight-group flexbin r-content-gallery">
                                {gallery.map((image) => (
                                    <a className="spotlight" href={image.image_extralarge_scale} >
                                        <img src={image.image_preview_scale} />
                                    </a>
                                ))}
                            </div>
                        </div>
                    ) : ("")
                }
            </div>
        </div>
    );
};
export default ContactContent;
