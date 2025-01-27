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

const CampaignContent = (props) => {
    let navigate = useNavigate();
    const { u, ...parsed } = Object.assign({
        id: queryString.parse(useFilterQuery().toString())["u"],
        b_start: 0,
    });
    const [params, setParams] = useState(parsed);
    const [item, setItem] = useState({});
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
        }
    }, [props.item]);

    const position = [50.4989185, 4.7184485];
    function handleClick() {
        navigate("..");
    }
    return item.fields ? (
        <div className="campaign-content r-content">
            <button type="button" onClick={handleClick}>
                <Translate text="Retour" />
            </button>
            <h2>{item.text}</h2>
            {item.fields.images_raw[0].image.b64 && (
                <img
                    src={`data:image/jpeg;base64,${item.fields.images_raw[0].image.b64}`}
                    alt={item.text}
                />
            )}
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
    ) : (
        <div>Loadings</div>
    );
};
export default CampaignContent;
