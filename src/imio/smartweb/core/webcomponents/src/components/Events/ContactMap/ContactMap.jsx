import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import L from "leaflet";
import iconSvg from "../../../assets/location-bla.svg";
import iconSvgActivated from "../../../assets/location-active-bla.svg";

import "./ContactMap.scss";
import "leaflet/dist/leaflet.css";

function ChangeMapView({ activeItem, arrayOfLatLngs }) {
    const map = useMap();
    if (activeItem) {
        const activeCoord = [];
        activeCoord.push(activeItem.geolocation.latitude);
        activeCoord.push(activeItem.geolocation.longitude);
        map.setView(activeCoord, 15);
    } else {
        let bounds = new L.LatLngBounds(arrayOfLatLngs);
        map.fitBounds(bounds);
    }
    return null;
}

function ContentMap(props) {
    const [activeItem, setActiveItem] = useState(null);
    const [hoverItem, setHoverItem] = useState(null);
    const [filterGeoArray, setFilterGeoArray] = useState([]);
    const [allPosition, setAllPosition] = useState(null);

    useEffect(() => {
        const filterArray = props.items.filter((isgeo) => isgeo.geolocation.latitude);
        setFilterGeoArray(filterArray);
    }, [props]);

    function mapIcon(url) {
        return new L.Icon({
            iconUrl: url,
            iconSize: [29, 37],
        });
    }

    const getMarkerIcon = (index) => {
        if (index === props.clickId) {
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
        if (props.clickId !== null) {
            var result =
                filterGeoArray &&
                filterGeoArray.filter((obj) => {
                    return obj.UID === props.clickId;
                });
            setActiveItem(result[0]);
        } else setActiveItem(null);
    }, [props.clickId]);

    useEffect(() => {
        if (props.hoverId) {
            var result =
                filterGeoArray &&
                filterGeoArray.filter((obj) => {
                    return obj.UID === props.hoverId;
                });
            setHoverItem(result[0]);
        } else setHoverItem(null);
    }, [props.hoverId]);

    useEffect(() => {
        if (filterGeoArray.length > 0) {
            let posArray = [];
            filterGeoArray.map((pos, i) => {
                let lat = pos.geolocation.latitude;
                let long = pos.geolocation.longitude;
                posArray.push([lat, long]);
            });
            setAllPosition(posArray);
        }
    }, [filterGeoArray]);

    const position = [50.6755292, 4.3806354];
    return (
        <div>
            <MapContainer
                style={{ height: `calc(100vh - ${props.headerHeight}px)`, minHeight: "600px" }}
                center={position}
                zoom={15}
            >
                <TileLayer
                    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {allPosition != null ? (
                    <ChangeMapView
                        activeItem={activeItem}
                        arrayOfLatLngs={allPosition && allPosition}
                    />
                ) : (
                    ""
                )}
                {filterGeoArray &&
                    filterGeoArray.map((mark, id) => (
                        <Marker
                            key={mark.UID}
                            icon={getMarkerIcon(mark.UID)}
                            zIndexOffset={getMarkerZindex(mark.UID)}
                            position={[
                                mark.geolocation ? mark.geolocation.latitude : "",
                                mark.geolocation ? mark.geolocation.longitude : "",
                            ]}
                            onClick={() => {
                                setActiveItem(mark);
                            }}
                        />
                    ))}
                ;
            </MapContainer>
        </div>
    );
}

export default ContentMap;
