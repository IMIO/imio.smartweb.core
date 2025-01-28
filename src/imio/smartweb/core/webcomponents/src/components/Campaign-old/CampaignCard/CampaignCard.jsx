import React, { useEffect, useState, useContext } from "react";
const CampaignCard = ({ item }) => {
    return (
        <>
            <div className="campaign-card-container">
                <div className="campaign-img">
                    {item.fields.images_raw[0].image.b64 && (
                        <img
                            src={`data:image/jpeg;base64,${item.fields.images_raw[0].image.b64}`}
                            alt={item.text}
                        />
                    )}
                </div>
                <div className="campaign-text">
                    <span className="r-item-title campaign-title">{item.text}</span>
                </div>
            </div>
        </>
    );
};

export default CampaignCard;
