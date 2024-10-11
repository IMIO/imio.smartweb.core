import React, { useEffect, useState, useContext } from "react";
const NewsCard = ({ item }) => {
    // console.log(item);
    return (
        <>
            <div className="campaign-card-container">
                <div className="campaign-img" />
                {/* <img src={item.fields.images_raw[0].image.url} alt={item.text} /> */}
                <div className="campaign-text">
                    <span className="r-item-title campaign-title">{item.text}</span>
                    {/* <div
                        className="campaign-description"
                        dangerouslySetInnerHTML={{ __html: item.fields.description }}
                    /> */}
                </div>
            </div>
        </>
    );
};

export default NewsCard;
