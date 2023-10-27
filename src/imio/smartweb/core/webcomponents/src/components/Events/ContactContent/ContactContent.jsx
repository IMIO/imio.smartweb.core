import { useHistory } from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";
import moment from "moment";
import Moment from "react-moment";
import ReactMarkdown from 'react-markdown'
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
	moment.locale('be');
	const start = moment.utc(contactItem.start).format('DD-MM-YYYY');
	const end = moment.utc(contactItem.end).format('DD-MM-YYYY');
	const startHours = moment.utc(contactItem.start).format('LT');
	const endHours = moment.utc(contactItem.end).format('LT');

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
		contactItem.city
	itineraryLink = itineraryLink.replaceAll('+null', '')

	return (
		<div className="envent-content r-content">
			<button type="button" onClick={handleClick}>
				<Translate text="Retour" />
			</button>
			<article>
				<header>
					<h2 className="r-content-title">{contactItem.title}</h2>
				</header>
				<figure>
					<div
						className="r-content-img"
						style={{
							backgroundImage: contactItem.image_affiche_scale
								? "url(" + contactItem.image_affiche_scale + ")"
								: "",
						}}
					/>
				</figure>
				<span className="news-info-title"><Translate text="Infos pratiques" /></span>
				<div className="r-content-news-info">
					<div className="r-content-news-info-container">
						{/* date */}
						<div className="r-content-news-info-schedul">
							<div className="icon-baseline">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									preserveAspectRatio="xMinYMin"
									viewBox="0 0 19.41 19.41"
								>
									<path d="M16.09,2.74H14.35V.85a.44.44,0,0,0-.43-.44H12.47A.44.44,0,0,0,12,.85V2.74H7.38V.85A.44.44,0,0,0,7,.41H5.5a.44.44,0,0,0-.44.44V2.74H3.32A1.74,1.74,0,0,0,1.58,4.48V17.26A1.74,1.74,0,0,0,3.32,19H16.09a1.74,1.74,0,0,0,1.75-1.74V4.48A1.74,1.74,0,0,0,16.09,2.74Zm-.21,14.52H3.54A.22.22,0,0,1,3.32,17h0V6.22H16.09V17a.21.21,0,0,1-.21.22Z" />
								</svg>
							</div>
							<div className="dpinlb">
								<div className="r-content-news-info--date">
									{start === end
										? (<div>
											{contactItem.whole_day
												? <div className="r-content-date-start">
													<span>Le&nbsp;</span>
													<div className="r-time">{start}</div>
												</div>
												: contactItem.open_end ?
													<>
														<div className="r-content-date-one-day">
															<div className="r-content-date-start">
																<span>Le&nbsp;</span>
																<div className="r-time">{start}</div>
																<span>&nbsp;à&nbsp;</span>
																<div className="r-time-hours">{startHours}</div>
															</div>

														</div>
													</>
													:
													<>
														<div className="r-content-date-one-day">
															<div className="r-content-date-start">
																<span>Le&nbsp;</span>
																<div className="r-time">{start}</div>
															</div>
															<div className="r-content-date-start-hours">
																<span>de&nbsp;</span>
																<div className="r-time-hours">{startHours}</div>
																<span>&nbsp;à&nbsp;</span>
																<div className="r-time-hours">{endHours}</div>
															</div>
														</div>
													</>
											}
										</div>)
										: (<div className="r-content-date-du-au">
											<div className="r-content-date-start">
												<span>Du&nbsp;</span>
												<div className="r-time">{start}</div>
											</div>
											<div className="r-content-date-end">
												<span>&nbsp;au&nbsp;</span>
												<div className="r-time">{end}</div>
											</div>
										</div>)
									}
								</div>
							</div>
						</div>
						{/* adress */}
						<div className="r-content-news-info-aera">
							{contactItem.street ? (
								<div className="icon-baseline">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 19.41 19.41"
									>
										<path d="M9,18.34C3.9,10.94,3,10.18,3,7.45a6.75,6.75,0,0,1,13.49,0c0,2.73-.94,3.49-6,10.89a.85.85,0,0,1-1.17.22A.77.77,0,0,1,9,18.34Zm.7-8.07A2.82,2.82,0,1,0,6.89,7.45a2.83,2.83,0,0,0,2.82,2.82Z" />
									</svg>
								</div>
							) : (
								""
							)}

							<div className="dpinlb">
								<div className="r-content-news-info--itinirary">
									{contactItem.street ? (
										<a href={itineraryLink} target="_blank">
											<span>Itinéraire</span>
										</a>
									) : (
										""
									)}
								</div>
								{contactItem.reduced_mobility_facilities === true ? (
									<div className="r-content-news-info--reduced">
										<span><Translate text="Accessible aux PMR" /></span>
									</div>
								) : (
									""
								)}
							</div>
						</div>
						{/* contact */}
						<div className="r-content-news-info-contact">
							<div className="dpinlb">
								<div className="r-content-news-info--name">
									<span>{contactItem.contact_name}</span>
								</div>
								<div className="r-content-news-info--phone">
									<span>
										<a href={`tel:${contactItem.contact_phone}`}>
											{contactItem.contact_phone}
										</a>
									</span>
								</div>
								<div className="r-content-news-info--email">
									<a href={`mailto:${contactItem.contact_email}`}>
										{contactItem.contact_email}
									</a>
								</div>
							</div>
						</div>
						{/* link  */}
						{contactItem.event_url === null &&
							contactItem.online_participation === null &&
							contactItem.video_url === null ? (
							""
						) : (
							<div className="r-content-news-info-link">
								<div className="icon-baseline">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 19.41 19.41"
									>
										<path d="M16.36,2.22H3.06a1.3,1.3,0,0,0-1.3,1.3h0v9a1.3,1.3,0,0,0,1.3,1.3H7.52v1.74h-.7a.8.8,0,0,0,0,1.6h5.79a.8.8,0,0,0,0-1.6h-.7V13.85h4.45a1.31,1.31,0,0,0,1.3-1.3v-9A1.3,1.3,0,0,0,16.36,2.22Zm-1.9,10.83a.37.37,0,1,1,.36-.37h0a.36.36,0,0,1-.36.36Zm1.6.08a.45.45,0,1,1,.44-.45h0a.44.44,0,0,1-.44.45h0Zm.53-1.35H2.82V3.52a.23.23,0,0,1,.23-.23H16.36a.23.23,0,0,1,.23.23h0v8.27Z" />
									</svg>
								</div>
								<div className="dpinlb">
									{contactItem.event_url === null ? (
										""
									) : (
										<div className="r-content-news-info-event_link">
											<a href={contactItem.event_url}><Translate text="Lien de l'événement" /></a>
										</div>
									)}
									{contactItem.online_participation === null ? (
										""
									) : (
										<div className="r-content-news-info--online_participation">
											<a href={contactItem.online_participation}>
												<Translate text="Participation en ligne" />
											</a>
										</div>
									)}
									{contactItem.video_url === null ? (
										""
									) : (
										<div className="r-content-news-info--video">
											<a href={contactItem.video_url}><Translate text="Lien vers la vidéo" /></a>
										</div>
									)}
								</div>
							</div>
						)}

						{/* Social */}
						{contactItem.facebook === null &&
							contactItem.instagram === null &&
							contactItem.twitter === null ? (
							""
						) : (
							<div className="r-content-news-info-social">
								<ul>
									{!contactItem.facebook ? (
										""
									) : (
										<li>
											<a href={contactItem.facebook} target="_blank">
												<svg
													xmlns="http://www.w3.org/2000/svg"
													height="800"
													width="1200"
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
											</a>
										</li>
									)}
									{!contactItem.instagram ? (
										""
									) : (
										<li>
											<a href={contactItem.instagram} target="_blank">
												<svg
													xmlns="http://www.w3.org/2000/svg"
													height="800"
													width="1200"
													viewBox="-100.7682 -167.947 873.3244 1007.682"
												>
													<g fill="#100f0d">
														<path d="M335.895 0c-91.224 0-102.663.387-138.49 2.021-35.752 1.631-60.169 7.31-81.535 15.612-22.088 8.584-40.82 20.07-59.493 38.743-18.674 18.673-30.16 37.407-38.743 59.495C9.33 137.236 3.653 161.653 2.02 197.405.386 233.232 0 244.671 0 335.895c0 91.222.386 102.661 2.02 138.488 1.633 35.752 7.31 60.169 15.614 81.534 8.584 22.088 20.07 40.82 38.743 59.495 18.674 18.673 37.405 30.159 59.493 38.743 21.366 8.302 45.783 13.98 81.535 15.612 35.827 1.634 47.266 2.021 138.49 2.021 91.222 0 102.661-.387 138.488-2.021 35.752-1.631 60.169-7.31 81.534-15.612 22.088-8.584 40.82-20.07 59.495-38.743 18.673-18.675 30.159-37.407 38.743-59.495 8.302-21.365 13.981-45.782 15.612-81.534 1.634-35.827 2.021-47.266 2.021-138.488 0-91.224-.387-102.663-2.021-138.49-1.631-35.752-7.31-60.169-15.612-81.534-8.584-22.088-20.07-40.822-38.743-59.495-18.675-18.673-37.407-30.159-59.495-38.743-21.365-8.302-45.782-13.981-81.534-15.612C438.556.387 427.117 0 335.895 0zm0 60.521c89.686 0 100.31.343 135.729 1.959 32.75 1.493 50.535 6.965 62.37 11.565 15.68 6.094 26.869 13.372 38.622 25.126 11.755 11.754 19.033 22.944 25.127 38.622 4.6 11.836 10.072 29.622 11.565 62.371 1.616 35.419 1.959 46.043 1.959 135.73 0 89.687-.343 100.311-1.959 135.73-1.493 32.75-6.965 50.535-11.565 62.37-6.094 15.68-13.372 26.869-25.127 38.622-11.753 11.755-22.943 19.033-38.621 25.127-11.836 4.6-29.622 10.072-62.371 11.565-35.413 1.616-46.036 1.959-135.73 1.959-89.694 0-100.315-.343-135.73-1.96-32.75-1.492-50.535-6.964-62.37-11.564-15.68-6.094-26.869-13.372-38.622-25.127-11.754-11.753-19.033-22.943-25.127-38.621-4.6-11.836-10.071-29.622-11.565-62.371-1.616-35.419-1.959-46.043-1.959-135.73 0-89.687.343-100.311 1.959-135.73 1.494-32.75 6.965-50.535 11.565-62.37 6.094-15.68 13.373-26.869 25.126-38.622 11.754-11.755 22.944-19.033 38.622-25.127 11.836-4.6 29.622-10.072 62.371-11.565 35.419-1.616 46.043-1.959 135.73-1.959" />
														<path d="M335.895 447.859c-61.838 0-111.966-50.128-111.966-111.964 0-61.838 50.128-111.966 111.966-111.966 61.836 0 111.964 50.128 111.964 111.966 0 61.836-50.128 111.964-111.964 111.964zm0-284.451c-95.263 0-172.487 77.224-172.487 172.487 0 95.261 77.224 172.485 172.487 172.485 95.261 0 172.485-77.224 172.485-172.485 0-95.263-77.224-172.487-172.485-172.487m219.608-6.815c0 22.262-18.047 40.307-40.308 40.307-22.26 0-40.307-18.045-40.307-40.307 0-22.261 18.047-40.308 40.307-40.308 22.261 0 40.308 18.047 40.308 40.308" />
													</g>
												</svg>
											</a>
										</li>
									)}
									{!contactItem.twitter ? (
										""
									) : (
										<li>
											<a href={contactItem.twitter} target="_blank">
												<svg
													xmlns="http://www.w3.org/2000/svg"
													height="800"
													width="1200"
													viewBox="-44.7006 -60.54775 387.4052 363.2865"
												>
													<path
														fill="#000"
														d="M93.719 242.19c112.46 0 173.96-93.168 173.96-173.96 0-2.646-.054-5.28-.173-7.903a124.338 124.338 0 0030.498-31.66c-10.955 4.87-22.744 8.148-35.11 9.626 12.622-7.57 22.313-19.543 26.885-33.817a122.62 122.62 0 01-38.824 14.841C239.798 7.433 223.915 0 206.326 0c-33.764 0-61.144 27.381-61.144 61.132 0 4.798.537 9.465 1.586 13.941-50.815-2.557-95.874-26.886-126.03-63.88a60.977 60.977 0 00-8.279 30.73c0 21.212 10.794 39.938 27.208 50.893a60.685 60.685 0 01-27.69-7.647c-.009.257-.009.507-.009.781 0 29.61 21.075 54.332 49.051 59.934a61.218 61.218 0 01-16.122 2.152 60.84 60.84 0 01-11.491-1.103c7.784 24.293 30.355 41.971 57.115 42.465-20.926 16.402-47.287 26.171-75.937 26.171-4.929 0-9.798-.28-14.584-.846 27.059 17.344 59.189 27.464 93.722 27.464"
													/>
												</svg>
											</a>
										</li>
									)}
								</ul>
							</div>
						)}
					</div>
					{/* booking */}
					<div className="r-content-news-info-action">
						{contactItem.ticket_url ? (
							<div className="r-content-booking">
								<a href={contactItem.ticket_url}>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										viewBox="0 0 19.41 19.41"
									>
										<circle cx="13.03" cy="14.61" r="0.63" fill="fill:#fff" />
										<circle cx="11.59" cy="6.52" r="0.63" fill="fill:#fff" />
										<path
											d="M17.11,11.47h.62V7.71h-1.6a1.25,1.25,0,0,1-1.25-1.25,1.27,1.27,0,0,1,.67-1.12l.54-.28-1.6-3.39-12.8,6h0v3.76h.63a1.26,1.26,0,0,1,0,2.51H1.68v3.76H17.73V14h-.62a1.26,1.26,0,1,1,0-2.51Zm-6.9-6.4a.63.63,0,0,0,1.14-.53l2.54-1.2.58,1.23A2.52,2.52,0,0,0,14,7.71H4.63Zm6.27,10.08v1.34H13.66a.63.63,0,1,0-1.26,0H2.93V15.16a2.51,2.51,0,0,0,0-4.86V9H12.4a.63.63,0,0,0,1.26,0h2.82V10.3a2.51,2.51,0,0,0,0,4.86Z"
											fill="fill:#fff"
										/>
										<circle cx="13.03" cy="10.85" r="0.63" fill="fill:#fff" />
										<circle cx="13.03" cy="12.73" r="0.63" fill="fill:#fff" />
									</svg>
									<Translate text="Billetterie" />
								</a>
							</div>
						) : (
							""
						)}
					</div>
				</div>
				<div className="r-content-description">
					<ReactMarkdown>{contactItem.description}</ReactMarkdown>
				</div>
				<div
					className="r-content-text"
					dangerouslySetInnerHTML={{
						__html: contactItem.text && contactItem.text.data,
					}}
				></div>
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
									<a className="spotlight" href={image.image_full_scale}>
										<img src={image.image_preview_scale} />
									</a>
								))}
							</div>
						</div>
					) : ("")
				}
			</article>
		</div>
	);
};
export default ContactContent;
