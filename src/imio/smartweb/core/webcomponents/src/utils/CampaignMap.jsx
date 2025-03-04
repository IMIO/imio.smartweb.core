import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import useFilterQuery from "../hooks/useFilterQuery";
import L from "leaflet";
import iconSvg from "../assets/pin-react.svg";
import iconSvgActivated from "../assets/pin-react-active.svg";
import { Link } from "react-router-dom";
import "./Map.scss";
import "leaflet/dist/leaflet.css";
import removeAccents from "remove-accents";
import queryString from "query-string";
import { el } from "date-fns/locale";

function ChangeMapView({ activeItem, arrayOfLatLngs }) {
    const map = useMap();
    if (activeItem) {
        const activeCoord = [];
        activeCoord.push(activeItem.fields.geolocalisation.lat);
        activeCoord.push(activeItem.fields.geolocalisation.lon);
        map.setView(activeCoord, 15);
    } else {
        let bounds = new L.LatLngBounds(arrayOfLatLngs);
        map.fitBounds(bounds);
    }
    return null;
}

function Map(props) {
    const [activeItem, setActiveItem] = useState(null);
    const [filterGeoArray, setFilterGeoArray] = useState([]);
    const [allPosition, setAllPosition] = useState(null);
    const { u, ...parsed } = Object.assign({
        id: queryString.parse(useFilterQuery().toString())["u"],
    });
    // Delete Imio positions
    useEffect(() => {
        if (!props.items) {
            return;
        }
        const filterArray = props.items.filter((isgeo) => {
            if (isgeo.fields) {
                return (
                    isgeo.fields.geolocalisation.lat &&
                    isgeo.fields.geolocalisation.lat !== 50.4989185 &&
                    isgeo.fields.geolocalisation.lon !== 4.7184485
                );
            } else {
                return (
                    isgeo.geolocation.latitude &&
                    isgeo.geolocation.latitude !== 50.4989185 &&
                    isgeo.geolocation.longitude !== 4.7184485
                );
            }
        });
        setFilterGeoArray(filterArray);
    }, [props.items]);

    // Setup Maker Icon
    const mapIcon = (url) => {
        return new L.Icon({
            iconUrl: url,
            iconSize: [29, 37],
        });
    };
    // Get Marker Icon and Z-index
    const getMarkerIcon = (index) => {
        if (index === parsed.id) {
            return mapIcon(iconSvgActivated);
        }
        if (index === props.hoverId) {
            return mapIcon(iconSvgActivated);
        }
        return mapIcon(iconSvg);
    };
    const getMarkerZindex = (index) => {
        if (index === props.clickId) {
            return 999;
        }
        if (index === props.hoverId) {
            return 999;
        }
        return 1;
    };

    useEffect(() => {
        var result =
            filterGeoArray &&
            filterGeoArray.filter((obj) => {
                return obj.id === parsed.id;
            });
        setActiveItem(result[0]);
    }, [filterGeoArray]);

    useEffect(() => {
        if (filterGeoArray.length > 0) {
            let posArray = [];
            filterGeoArray.map((pos, i) => {
                let lat = pos.fields.geolocalisation.lat;
                let long = pos.fields.geolocalisation.lon;
                posArray.push([lat, long]);
            });
            setAllPosition(posArray);
        }
    }, [filterGeoArray]);
    const position = [50.85034, 4.35171];

    const markers = filterGeoArray.map((mark, i) => (
        <Marker
            key={i}
            icon={getMarkerIcon(mark.id)}
            zIndexOffset={getMarkerZindex(mark.id)}
            position={[
                mark.fields.geolocalisation ? mark.fields.geolocalisation.lat : "",
                mark.fields.geolocalisation ? mark.fields.geolocalisation.lon : "",
            ]}
            eventHandlers={{
                mouseover: (e) => {
                    // Gérer les événements ici
                },
            }}
        >
            <Popup closeButton={false}>
                <Link
                    className="r-map-popup"
                    style={{ textDecoration: "none" }}
                    to={{
                        pathname:
                            "/" +
                            removeAccents(mark.text)
                                .replace(/[^a-zA-Z ]/g, "")
                                .replace(/\s/g, "-")
                                .toLowerCase(),
                        search: `?u=${mark.id}`,
                        state: {
                            idItem: mark.id,
                        },
                    }}
                >
                    <span className="r-map-popup-title">{mark.text}</span>
                </Link>
                <a
                    href={`https://www.google.com/maps/dir/?api=1&destination=${mark.fields.rue ? mark.fields.rue + " " + mark.fields.numero : ""}`}
                    className="r-map-popup-adress"
                >
                    {mark.fields.rue && mark.fields.rue + " " + mark.fields.numero}
                </a>
            </Popup>
        </Marker>
    ));

    return (
        <div>
            <MapContainer
                style={{ height: `calc(100vh - ${props.headerHeight}px)`, minHeight: "600px" }}
                center={position}
                zoom={35}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {allPosition != null ? (
                    <ChangeMapView
                        activeItem={activeItem}
                        activeItemUID={parsed.id}
                        arrayOfLatLngs={allPosition && allPosition}
                    />
                ) : (
                    ""
                )}
                {filterGeoArray && markers}
            </MapContainer>
        </div>
    );
}

export default Map;
