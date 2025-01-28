import { useNavigate } from "react-router-dom";
import React, { useEffect, useState, useRef } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";
import moment from "moment";
import ReactMarkdown from "react-markdown";
import Spotlight from "spotlight.js";
import "../../../../node_modules/flexbin/flexbin.css";
import { Translate } from "react-translated";
import queryString from "query-string";

const CampaignContent = ({ queryUrl, onChange, onlyPastCampaign, contextAuthenticatedUser }) => {
    let navigate = useNavigate();
    const { u, ...parsed } = Object.assign({
        UID: queryString.parse(useFilterQuery().toString())["u"],
        fullobjects: 1,
        "event_dates.query": moment().format("YYYY-MM-DD"),
        "event_dates.range": onlyPastCampaign === "True" ? "max" : "min",
    });
    const [params, setParams] = useState(parsed);
    const [item, setitem] = useState({});
    const [recurence, setRecurence] = useState([]);
    const [files, setFiles] = useState();
    const [gallery, setGallery] = useState();
    const [isSchedulVisible, setSchedulVisibility] = useState(false);
    const modalRef = useRef();
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
        setParams(parsed);
    }, [queryString.parse(useFilterQuery().toString())["u"]]);
    // set all campaigns state
    useEffect(() => {
        if (response !== null) {
            setitem(response.items[0]);
            // set recurrence
            if (response.items.length > 1) {
                response.items.map((item, i) => {
                    const currentDate = new Date();
                    const itemDate = new Date(item.start);
                    if (itemDate >= currentDate) {
                        setRecurence((prevRecurrence) => [...prevRecurrence, item.start]);
                    }
                });
            } else {
                setRecurence(null);
            }
        }
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "instant",
        });
    }, [response]);
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

    // ref to toggle

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (modalRef.current && !modalRef.current.contains(event.target)) {
                closeSchedul();
            }
        };

        document.addEventListener("mousedown", handleClickOutside);

        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    //  moment
    moment.locale("be");
    const start = moment.utc(item.start).format("DD-MM-YYYY");
    const end = moment.utc(item.end).format("DD-MM-YYYY");
    const startHours = moment.utc(item.start).format("LT");
    const endHours = moment.utc(item.end).format("LT");

    // Trouver la date la plus proche dans le futur
    const now = moment();
    const futureDates = recurence && recurence.filter((date) => moment(date).isAfter(now));

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
        item.city;
    itineraryLink = itineraryLink.replaceAll("+null", "");

    const openSchedul = () => {
        setSchedulVisibility(true);
    };
    const closeSchedul = () => {
        setSchedulVisibility(false);
    };
    return (
        <div className="envent-content r-content">
            <button type="button" onClick={handleClick}>
                <Translate text="Retour" />
            </button>

            <article>
                <header className="r-content-header">
                    <h2 className="r-content-title">{item.title}</h2>
                </header>
                <figure>
                    <div
                        className="r-content-img"
                        style={{
                            backgroundImage: item.image_affiche_scale
                                ? "url(" + item.image_affiche_scale + ")"
                                : "",
                        }}
                    />
                </figure>

                <div className="r-content-description">
                    <ReactMarkdown>{item.description}</ReactMarkdown>
                </div>
                <div
                    className="r-content-text"
                    dangerouslySetInnerHTML={{
                        __html: item.text && item.text.data,
                    }}
                ></div>
            </article>
        </div>
    );
};
export default CampaignContent;
