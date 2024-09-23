import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";
import ReactMarkdown from "react-markdown";
import "spotlight.js";
import "../../../../node_modules/flexbin/flexbin.css";
import { Translate } from "react-translated";
import queryString from "query-string";

const ContactContent = ({ queryUrl, onChange, contextAuthenticatedUser }) => {
    const navigate = useNavigate();
    const { u, ...parsed } = Object.assign({
        UID: queryString.parse(useFilterQuery().toString())["u"],
        fullobjects: 1,
    });
    const [params, setParams] = useState(parsed);
    const [item, setitem] = useState({});
    const [files, setFiles] = useState();
    const [gallery, setGallery] = useState();
    const [social, setSocial] = useState([]);
    const [image, setImage] = useState();
    const [isSchedulVisible, setSchedulVisibility] = useState(true);

    const { response } = useAxios(
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
        setParams(parsed);
    }, [queryString.parse(useFilterQuery().toString())["u"]]);

    // set all contacts state
    useEffect(() => {
        if (response !== null) {
            setitem(response.items[0]);
        }
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "instant",
        });
    }, [response]);

    // set image
    useEffect(() => {
        if (item.image_affiche_scale) {
            const img = new Image();
            img.src = item.image_affiche_scale;
            img.onload = () => {
                setImage(img);
            };
        }
    }, [item]);

    // set social link
    useEffect(() => {
        item.urls && setSocial(item.urls.filter((urls) => urls.type !== "website"));
    }, [item]);

    /// use to set file and gallery items
    useEffect(() => {
        if (item.items && item.items.length > 0) {
            setFiles(item.items.filter((files) => files["@type"] === "File"));
            setGallery(item.items.filter((files) => files["@type"] === "Image"));
        }
    }, [item]);

    function handleClick() {
        navigate("..");
        onChange(null);
    }
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

    const toggleSchedul = () => {
        setSchedulVisibility(!isSchedulVisible);
    };
    return (
        <div className="annuaire-content r-content">
            <button type="button" onClick={handleClick}>
                <Translate text="Retour" />
            </button>

            {contextAuthenticatedUser === "False" ? (
                <a
                    href={item["@id"]}
                    target="_blank"
                    title="Editer la fiche"
                    className="edit-rest-elements edit-rest-elements-content"
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
            <article>
                <header>
                    <h2 className="r-content-title">{item.title}</h2>
                    {item.subtitle ? <h3 className="r-content-subtitle">{item.subtitle}</h3> : ""}
                </header>
                {item.image_affiche_scale && (
                    <figure className="r-content-figure">
                        <div
                            className="r-content-figure-blur"
                            style={{ backgroundImage: "url(" + item.image_affiche_scale + ")" }}
                        />
                        <img
                            className="r-content-figure-img"
                            src={item.image_affiche_scale}
                            style={{
                                objectFit:
                                    image && image.width >= image.height ? "cover" : "contain",
                            }}
                            alt=""
                        />
                    </figure>
                )}
            </article>
            <div className="contactCard">
                <div className="contactText">
                    <div className="r-content-description">
                        <ReactMarkdown>{item.description}</ReactMarkdown>
                    </div>
                    <div className="contactTextAll">
                        <p className="annuaire-info-title">
                            <Translate text="Infos pratiques" />
                        </p>
                        {item.category ? <span>{item.category}</span> : ""}
                        {item.street ? (
                            <div className="annaire-adresse">
                                <div className="annaire-adresse-icon">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        fill="currentColor"
                                        viewBox="0 0 16 16"
                                    >
                                        <path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6z" />
                                    </svg>
                                </div>
                                <div className="annaire-adresse-content">
                                    <a href={itineraryLink} target="_blank" rel="noreferrer">
                                        {item.number ? <span>{item.number + " "}</span> : ""}
                                        {item.street ? <span>{item.street + ", "}</span> : ""}
                                        {item.complement ? (
                                            <span>{item.complement + ", "}</span>
                                        ) : (
                                            ""
                                        )}
                                        {item.zipcode ? <span>{item.zipcode + " "}</span> : ""}
                                        {item.city ? <span>{item.city}</span> : ""}
                                    </a>
                                </div>
                            </div>
                        ) : (
                            ""
                        )}
                        {/* schedule */}
                        {item.table_date && (
                            <a
                                href="javascript:void(0)"
                                onClick={toggleSchedul}
                                className="annuaire-schedul"
                                role="button"
                                aria-expanded="false"
                                aria-label="Afficher l'horaire complet"
                            >
                                <div className="annuaire-schedul-icon">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        fill="currentColor"
                                        className="bi bi-clock-fill"
                                        viewBox="0 0 16 16"
                                    >
                                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71z" />
                                    </svg>
                                </div>
                                <div className="annuaire-schedul-content">
                                    {isSchedulVisible ? (
                                        <>
                                            <span
                                                className={
                                                    item.schedule_for_today === "Fermé"
                                                        ? "annuaire-day-close"
                                                        : "annuaire-day-open"
                                                }
                                            >
                                                <Translate text={item.schedule_for_today} />
                                            </span>
                                            <svg
                                                xmlns="http://www.w3.org/2000/svg"
                                                width="10"
                                                height="10"
                                                fill="currentColor"
                                                className="bi bi-caret-down-fill"
                                                viewBox="0 0 16 16"
                                            >
                                                <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z" />
                                            </svg>
                                        </>
                                    ) : (
                                        <div>
                                            <ul>
                                                {item.table_date.map((day, index) => {
                                                    const dayOfWeek = Object.keys(day)[0];
                                                    const status = day[dayOfWeek];

                                                    return (
                                                        <li key={index}>
                                                            <strong>
                                                                <Translate text={dayOfWeek} />:
                                                            </strong>{" "}
                                                            {status}
                                                        </li>
                                                    );
                                                })}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            </a>
                        )}

                        {item.phones && item.phones.length > 0 ? (
                            <div className="annuaire-phone">
                                <div className="annuaire-phone-icon">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        fill="currentColor"
                                        viewBox="0 0 16 16"
                                    >
                                        <path d="M1.885.511a1.745 1.745 0 0 1 2.61.163L6.29 2.98c.329.423.445.974.315 1.494l-.547 2.19a.678.678 0 0 0 .178.643l2.457 2.457a.678.678 0 0 0 .644.178l2.189-.547a1.745 1.745 0 0 1 1.494.315l2.306 1.794c.829.645.905 1.87.163 2.611l-1.034 1.034c-.74.74-1.846 1.065-2.877.702a18.634 18.634 0 0 1-7.01-4.42 18.634 18.634 0 0 1-4.42-7.009c-.362-1.03-.037-2.137.703-2.877L1.885.511z" />
                                    </svg>
                                </div>
                                <div className="annuaire-phone-content">
                                    {item.phones.map((phone, i) => {
                                        return (
                                            <span key={i}>
                                                {phone.label ? phone.label + ": " : ""}
                                                <a href={"tel:" + phone.number}>{phone.number}</a>
                                            </span>
                                        );
                                    })}
                                </div>
                            </div>
                        ) : (
                            ""
                        )}

                        {item.mails && item.mails.length > 0 ? (
                            <div className="annuaire-website-mails">
                                <div className="annuaire-website-mails-icon">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        fill="currentColor"
                                        viewBox="0 0 16 16"
                                    >
                                        <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z" />
                                    </svg>
                                </div>
                                <div className="annuaire-website-mails-content">
                                    {item.mails.map((mail, i) => {
                                        return (
                                            <span key={i}>
                                                {mail.label ? mail.label + ": " : ""}
                                                <a href={"mailto:" + mail.mail_address}>
                                                    {mail.mail_address}
                                                </a>
                                            </span>
                                        );
                                    })}
                                </div>
                            </div>
                        ) : (
                            ""
                        )}

                        {item.urls && item.urls.length > 0 ? (
                            <div className="annuaire-website-link">
                                <div className="annuaire-website-link-icon">
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="16"
                                        height="16"
                                        viewBox="0 0 16 16"
                                    >
                                        <path d="M2.5 2A1.5 1.5 0 0 0 1 3.5V12h14V3.5A1.5 1.5 0 0 0 13.5 2h-11zM0 12.5h16a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 12.5z" />
                                    </svg>
                                </div>
                                <ul className="annuaire-website-link-content">
                                    {item.urls
                                        .filter((url) => url.type === "website")
                                        .map((website, i) => {
                                            return (
                                                <>
                                                    <li key={i}>
                                                        <a
                                                            href={website.url}
                                                            target="_blank"
                                                            rel="noreferrer"
                                                        >
                                                            {website.url}
                                                        </a>
                                                    </li>
                                                </>
                                            );
                                        })}
                                </ul>
                            </div>
                        ) : (
                            ""
                        )}

                        {/* add social icons */}
                        {social && (
                            <div className="annuaire-social-link">
                                {social.length > 1 ? (
                                    <ul>
                                        {social.map((url, i) => {
                                            return (
                                                <li key={i}>
                                                    <a
                                                        href={url.url}
                                                        target="_blank"
                                                        rel="noreferrer"
                                                    >
                                                        {url.type === "facebook" ? (
                                                            <svg
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                width="25"
                                                                height="25"
                                                                fill="currentColor"
                                                                viewBox="0 0 16 16"
                                                            >
                                                                <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z" />
                                                            </svg>
                                                        ) : url.type === "instagram" ? (
                                                            <svg
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                width="25"
                                                                height="25"
                                                                fill="currentColor"
                                                                viewBox="0 0 16 16"
                                                            >
                                                                <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z" />
                                                            </svg>
                                                        ) : url.type === "twitter" ? (
                                                            <svg
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                width="25"
                                                                height="25"
                                                                fill="currentColor"
                                                                class="bi bi-twitter-x"
                                                                viewBox="0 0 16 16"
                                                            >
                                                                <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865z" />
                                                            </svg>
                                                        ) : url.type === "youtube" ? (
                                                            <svg
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                width="25"
                                                                height="25"
                                                                fill="currentColor"
                                                                viewBox="0 0 16 16"
                                                            >
                                                                <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z" />
                                                            </svg>
                                                        ) : url.type === "linkedin" ? (
                                                            <svg
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                width="25"
                                                                height="25"
                                                                fill="currentColor"
                                                                class="bi bi-linkedin"
                                                                viewBox="0 0 16 16"
                                                            >
                                                                <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z" />
                                                            </svg>
                                                        ) : url.type === "pinterest" ? (
                                                            <svg
                                                                xmlns="http://www.w3.org/2000/svg"
                                                                width="25"
                                                                height="25"
                                                                fill="currentColor"
                                                                viewBox="0 0 16 16"
                                                            >
                                                                <path d="M8 0a8 8 0 0 0-2.915 15.452c-.07-.633-.134-1.606.027-2.297.146-.625.938-3.977.938-3.977s-.239-.479-.239-1.187c0-1.113.645-1.943 1.448-1.943.682 0 1.012.512 1.012 1.127 0 .686-.437 1.712-.663 2.663-.188.796.4 1.446 1.185 1.446 1.422 0 2.515-1.5 2.515-3.664 0-1.915-1.377-3.254-3.342-3.254-2.276 0-3.612 1.707-3.612 3.471 0 .688.265 1.425.595 1.826a.24.24 0 0 1 .056.23c-.061.252-.196.796-.222.907-.035.146-.116.177-.268.107-1-.465-1.624-1.926-1.624-3.1 0-2.523 1.834-4.84 5.286-4.84 2.775 0 4.932 1.977 4.932 4.62 0 2.757-1.739 4.976-4.151 4.976-.811 0-1.573-.421-1.834-.919l-.498 1.902c-.181.695-.669 1.566-.995 2.097A8 8 0 1 0 8 0z" />
                                                            </svg>
                                                        ) : (
                                                            ""
                                                        )}
                                                    </a>
                                                </li>
                                            );
                                        })}
                                    </ul>
                                ) : (
                                    <div>
                                        <a
                                            href={social[0] && social[0].url}
                                            target="_blank"
                                            rel="noreferrer"
                                        >
                                            {social[0] && social[0].type === "facebook" ? (
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    width="25"
                                                    height="25"
                                                    fill="currentColor"
                                                    viewBox="0 0 16 16"
                                                >
                                                    <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z" />
                                                </svg>
                                            ) : social[0] && social[0].type === "instagram" ? (
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    width="25"
                                                    height="25"
                                                    fill="currentColor"
                                                    viewBox="0 0 16 16"
                                                >
                                                    <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z" />
                                                </svg>
                                            ) : social[0] && social[0].type === "twitter" ? (
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    width="25"
                                                    height="25"
                                                    fill="currentColor"
                                                    class="bi bi-twitter-x"
                                                    viewBox="0 0 16 16"
                                                >
                                                    <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865z" />
                                                </svg>
                                            ) : social[0] && social[0].type === "youtube" ? (
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    width="25"
                                                    height="25"
                                                    fill="currentColor"
                                                    viewBox="0 0 16 16"
                                                >
                                                    <path d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z" />
                                                </svg>
                                            ) : social[0] && social[0].type === "linkedin" ? (
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    width="25"
                                                    height="25"
                                                    fill="currentColor"
                                                    class="bi bi-linkedin"
                                                    viewBox="0 0 16 16"
                                                >
                                                    <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z" />
                                                </svg>
                                            ) : social[0] && social[0].type === "pinterest" ? (
                                                <svg
                                                    xmlns="http://www.w3.org/2000/svg"
                                                    width="25"
                                                    height="25"
                                                    fill="currentColor"
                                                    viewBox="0 0 16 16"
                                                >
                                                    <path d="M8 0a8 8 0 0 0-2.915 15.452c-.07-.633-.134-1.606.027-2.297.146-.625.938-3.977.938-3.977s-.239-.479-.239-1.187c0-1.113.645-1.943 1.448-1.943.682 0 1.012.512 1.012 1.127 0 .686-.437 1.712-.663 2.663-.188.796.4 1.446 1.185 1.446 1.422 0 2.515-1.5 2.515-3.664 0-1.915-1.377-3.254-3.342-3.254-2.276 0-3.612 1.707-3.612 3.471 0 .688.265 1.425.595 1.826a.24.24 0 0 1 .056.23c-.061.252-.196.796-.222.907-.035.146-.116.177-.268.107-1-.465-1.624-1.926-1.624-3.1 0-2.523 1.834-4.84 5.286-4.84 2.775 0 4.932 1.977 4.932 4.62 0 2.757-1.739 4.976-4.151 4.976-.811 0-1.573-.421-1.834-.919l-.498 1.902c-.181.695-.669 1.566-.995 2.097A8 8 0 1 0 8 0z" />
                                                </svg>
                                            ) : (
                                                ""
                                            )}
                                        </a>
                                    </div>
                                )}
                            </div>
                        )}

                        {item.logo_thumb_scale ? (
                            <img className="annuaire-logo" src={item.logo_thumb_scale} alt="" />
                        ) : (
                            ""
                        )}
                    </div>
                </div>
                {/* add files to download */}
                {files && (
                    <div className="r-content-files">
                        {files.map((file, i) => (
                            <div key={i} className="r-content-file">
                                <a
                                    href={file.targetUrl}
                                    className="r-content-file-link"
                                    rel="nofollow"
                                >
                                    <span className="r-content-file-title">{file.title}</span>
                                    <span className="r-content-file-icon">
                                        <svg
                                            width="21"
                                            height="21"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="#8899a4"
                                            stroke-width="2"
                                            stroke-linecap="square"
                                            stroke-linejoin="arcs"
                                        >
                                            <path d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"></path>
                                        </svg>
                                    </span>
                                </a>
                            </div>
                        ))}
                    </div>
                )}
                {/* add gallery */}
                {gallery && (
                    <div className="r-content-gallery">
                        <div className="spotlight-group flexbin r-content-gallery">
                            {gallery.map((image, i) => (
                                <a key={i} className="spotlight" href={image.image_full_scale}>
                                    <img src={image.image_preview_scale} alt="" />
                                </a>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};
export default ContactContent;
