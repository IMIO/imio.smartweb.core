import { useHistory, useParams, useLocation } from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";
import ReactMarkdown from 'react-markdown'
import Spotlight from "spotlight.js";
import "../../../../node_modules/flexbin/flexbin.css"
import { Translate } from "react-translated";

const ContactContent = ({ queryUrl, onChange }) => {
    let history = useHistory();
    const queryString = require("query-string");
    const { u, ...parsed } = Object.assign(
        { UID : queryString.parse(useFilterQuery().toString())['u'], fullobjects: 1 },
    );
    const [params, setParams] = useState(parsed);
    const [contactItem, setcontactItem] = useState({});
    const [files, setFiles] = useState(0);
    const [gallery, setGallery] = useState(0);
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
                {contactItem.logo ? (
                    <figure>
                        <img
                            className="r-content-img"
                            src={contactItem.logo.scales.thumb.download}
                            alt={contactItem.logo.filename}
                        />
                    </figure>
                ) : (
                    ""
                )}
            </article>
            <div className="contactCard">
                <div className="contactText">
                <div className="r-content-description">
					<ReactMarkdown>{contactItem.description}</ReactMarkdown>
				</div>
                    <div className="contactTextAll">
                        {contactItem.category ? <span>{contactItem.category}</span> : ""}
                        <div className="adresse">
                            {contactItem.number ? <span>{contactItem.number + " "}</span> : ""}
                            {contactItem.street ? <span>{contactItem.street + ", "}</span> : ""}
                            {contactItem.complement ? (
                                <span>{contactItem.complement + ", "}</span>
                            ) : (
                                ""
                            )}
                            {contactItem.zipcode ? <span>{contactItem.zipcode + " "}</span> : ""}
                            {contactItem.city ? <span>{contactItem.city}</span> : ""}
                        </div>
                        <div className="itineraty">
                            {contactItem.street ? (
                                <a href={itineraryLink} target="_blank">
                                    Itinéraire
                                </a>
                            ) : (
                                ""
                            )}
                        </div>
                        <div className="phones">
                            {contactItem.phones
                                ? contactItem.phones.map((phone) => {
                                      return (
                                            <span>
                                                <a href={"tel:"+phone.number}>
                                                    {phone.number}
                                                </a>
                                            </span>
                                            );
                                  })
                                : ""}
                        </div>
                        <div className="mails">
                            {contactItem.mails
                                ? contactItem.mails.map((mail) => {
                                      return (
                                        <span>
                                            <a href={"mailto:"+mail.mail_address}>
                                                {mail.mail_address}
                                            </a>
                                        </span>
                                        );
                                  })
                                : ""}
                        </div>
                        <div className="urls">
                            {contactItem.urls
                                ? contactItem.urls.map((url) => {
                                      return (
                                            <>
                                            <span>
                                                <a href={url.url} target="_blank">
                                                    { url.type === "facebook" ?  (
                                                        <svg
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            height="40"
                                                            width="60"
                                                            viewBox="-204.79995 -341.33325 1774.9329 2047.9995"
                                                        >
                                                            <path
                                                                d="M1365.333 682.667C1365.333 305.64 1059.693 0 682.667 0 305.64 0 0 305.64 0 682.667c0 340.738 249.641 623.16 576 674.373V880H402.667V682.667H576v-150.4c0-171.094 101.917-265.6 257.853-265.6 74.69 0 152.814 13.333 152.814 13.333v168h-86.083c-84.804 0-111.25 52.623-111.25 106.61v128.057h189.333L948.4 880H789.333v477.04c326.359-51.213 576-333.635 576-674.373"
                                                                fill="#100f0d"
                                                            />
                                                            <path
                                                                d="M948.4 880l30.267-197.333H789.333V554.609C789.333 500.623 815.78 448 900.584 448h86.083V280s-78.124-13.333-152.814-13.333c-155.936 0-257.853 94.506-257.853 265.6v150.4H402.667V880H576v477.04a687.805 687.805 0 00106.667 8.293c36.288 0 71.91-2.84 106.666-8.293V880H948.4"
                                                                fill="#fff"
                                                            />
                                                        </svg>
                                                    )
                                                    : url.type === "instagram" ?  (
                                                        <svg
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            height="40"
                                                            width="60"
                                                            viewBox="-100.7682 -167.947 873.3244 1007.682"
												        >
                                                            <g fill="#100f0d">
                                                                <path d="M335.895 0c-91.224 0-102.663.387-138.49 2.021-35.752 1.631-60.169 7.31-81.535 15.612-22.088 8.584-40.82 20.07-59.493 38.743-18.674 18.673-30.16 37.407-38.743 59.495C9.33 137.236 3.653 161.653 2.02 197.405.386 233.232 0 244.671 0 335.895c0 91.222.386 102.661 2.02 138.488 1.633 35.752 7.31 60.169 15.614 81.534 8.584 22.088 20.07 40.82 38.743 59.495 18.674 18.673 37.405 30.159 59.493 38.743 21.366 8.302 45.783 13.98 81.535 15.612 35.827 1.634 47.266 2.021 138.49 2.021 91.222 0 102.661-.387 138.488-2.021 35.752-1.631 60.169-7.31 81.534-15.612 22.088-8.584 40.82-20.07 59.495-38.743 18.673-18.675 30.159-37.407 38.743-59.495 8.302-21.365 13.981-45.782 15.612-81.534 1.634-35.827 2.021-47.266 2.021-138.488 0-91.224-.387-102.663-2.021-138.49-1.631-35.752-7.31-60.169-15.612-81.534-8.584-22.088-20.07-40.822-38.743-59.495-18.675-18.673-37.407-30.159-59.495-38.743-21.365-8.302-45.782-13.981-81.534-15.612C438.556.387 427.117 0 335.895 0zm0 60.521c89.686 0 100.31.343 135.729 1.959 32.75 1.493 50.535 6.965 62.37 11.565 15.68 6.094 26.869 13.372 38.622 25.126 11.755 11.754 19.033 22.944 25.127 38.622 4.6 11.836 10.072 29.622 11.565 62.371 1.616 35.419 1.959 46.043 1.959 135.73 0 89.687-.343 100.311-1.959 135.73-1.493 32.75-6.965 50.535-11.565 62.37-6.094 15.68-13.372 26.869-25.127 38.622-11.753 11.755-22.943 19.033-38.621 25.127-11.836 4.6-29.622 10.072-62.371 11.565-35.413 1.616-46.036 1.959-135.73 1.959-89.694 0-100.315-.343-135.73-1.96-32.75-1.492-50.535-6.964-62.37-11.564-15.68-6.094-26.869-13.372-38.622-25.127-11.754-11.753-19.033-22.943-25.127-38.621-4.6-11.836-10.071-29.622-11.565-62.371-1.616-35.419-1.959-46.043-1.959-135.73 0-89.687.343-100.311 1.959-135.73 1.494-32.75 6.965-50.535 11.565-62.37 6.094-15.68 13.373-26.869 25.126-38.622 11.754-11.755 22.944-19.033 38.622-25.127 11.836-4.6 29.622-10.072 62.371-11.565 35.419-1.616 46.043-1.959 135.73-1.959" />
                                                                <path d="M335.895 447.859c-61.838 0-111.966-50.128-111.966-111.964 0-61.838 50.128-111.966 111.966-111.966 61.836 0 111.964 50.128 111.964 111.966 0 61.836-50.128 111.964-111.964 111.964zm0-284.451c-95.263 0-172.487 77.224-172.487 172.487 0 95.261 77.224 172.485 172.487 172.485 95.261 0 172.485-77.224 172.485-172.485 0-95.263-77.224-172.487-172.485-172.487m219.608-6.815c0 22.262-18.047 40.307-40.308 40.307-22.26 0-40.307-18.045-40.307-40.307 0-22.261 18.047-40.308 40.307-40.308 22.261 0 40.308 18.047 40.308 40.308" />
                                                            </g>
												        </svg>
                                                    )
                                                    : url.type === "twitter" ? (
                                                        <svg
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            height="40"
                                                            width="60"
                                                            viewBox="-44.7006 -60.54775 387.4052 363.2865"
												        >
                                                            <path
                                                                fill="#000"
                                                                d="M93.719 242.19c112.46 0 173.96-93.168 173.96-173.96 0-2.646-.054-5.28-.173-7.903a124.338 124.338 0 0030.498-31.66c-10.955 4.87-22.744 8.148-35.11 9.626 12.622-7.57 22.313-19.543 26.885-33.817a122.62 122.62 0 01-38.824 14.841C239.798 7.433 223.915 0 206.326 0c-33.764 0-61.144 27.381-61.144 61.132 0 4.798.537 9.465 1.586 13.941-50.815-2.557-95.874-26.886-126.03-63.88a60.977 60.977 0 00-8.279 30.73c0 21.212 10.794 39.938 27.208 50.893a60.685 60.685 0 01-27.69-7.647c-.009.257-.009.507-.009.781 0 29.61 21.075 54.332 49.051 59.934a61.218 61.218 0 01-16.122 2.152 60.84 60.84 0 01-11.491-1.103c7.784 24.293 30.355 41.971 57.115 42.465-20.926 16.402-47.287 26.171-75.937 26.171-4.929 0-9.798-.28-14.584-.846 27.059 17.344 59.189 27.464 93.722 27.464"
                                                            />
												        </svg>
                                                    )
                                                    : url.type === "youtube" ? (
                                                        <svg
                                                            xmlns="http://www.w3.org/2000/svg"
                                                            height="40"
                                                            width="60"
                                                            viewBox="-18 -8 60 40"
												        >
                                                            <path
                                                                fill="#000"
                                                                d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"
                                                            />
                                                        </svg>												        
                                                    )  
                                                    : (url.type)    
                                                }
                                                </a>
                                            </span>
                                            </>
                                            );
                                  })
                                : ""}
                        </div>
                        <div className="topics">
                            {contactItem.topics
                                ? contactItem.topics.map((mail) => {
                                      return <span>{mail.title}</span>;
                                  })
                                : ""}
                        </div>
                    </div>
                </div>
                				{/* add files to download */}
				{
					files ? (
						<div className="r-content-files">
							<h2 className="r-content-files-title"><Translate text="Téléchargements" /></h2>
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
								<a className="spotlight" href={image.image.scales.extralarge.download} data-description="Lorem ipsum dolor sit amet, consetetur sadipscing.">
									<img src={image.image.scales.preview.download} alt="Lorem ipsum dolor sit amet" />
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
