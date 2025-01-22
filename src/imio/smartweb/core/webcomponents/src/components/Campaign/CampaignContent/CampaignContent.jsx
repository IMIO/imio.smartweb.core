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
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

const ContactContent = (props) => {
    let navigate = useNavigate();
    const { u, ...parsed } = Object.assign({
        id: queryString.parse(useFilterQuery().toString())["u"],
        b_start: 0,
    });
    const [params, setParams] = useState(parsed);
    const [item, setItem] = useState({});
    const [base64Image, setBase64Image] = useState("");
    const modalRef = useRef();
    const { response, error, isLoading } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.queryUrl,
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

    useEffect(() => {
        if (response !== null) {
            setItem(response);
            if (response.fields.images_raw && response.fields.images_raw.length > 0) {
                const imageContent = response.fields.images_raw[0].image.content;
                const contentType = response.fields.images_raw[0].image.content_type;
                setBase64Image(`data:${contentType};base64,${imageContent}`);
            }
        }
    }, [response]);
    const position = [50.4989185, 4.7184485];
    return (
        <div className="campaign-content r-content">
            <h2>{item.text}</h2>
            {base64Image && <img src={base64Image} alt="Base64 Image" />}
            <div className="votes">
                <span className="vote-pour">
                    {" "}
                    Vote pour {item.fields && item.fields.votes_pour}{" "}
                </span>
                <span className="vote-contre">
                    {" "}
                    Vote contre{item.fields && item.fields.votes_contre}{" "}
                </span>
            </div>
            <div
                className="campaign-description"
                dangerouslySetInnerHTML={{
                    __html: item.fields && item.fields.description,
                }}
            />
            <MapContainer center={position} zoom={13} scrollWheelZoom={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={position}>
                    <Popup>
                        A pretty CSS3 popup. <br /> Easily customizable.
                    </Popup>
                </Marker>
            </MapContainer>
        </div>
    );
};
export default ContactContent;
