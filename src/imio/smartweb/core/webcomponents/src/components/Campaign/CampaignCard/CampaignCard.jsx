import React, { useEffect, useState } from "react";
import { Translate } from "react-translated";

const CampaignCard = (props) => {
    const [image, setImage] = useState(new Image());
    const [imageClassName, setImageClassName] = useState("");

    // Set image and image className
    useEffect(() => {
        const loadImage = async () => {
            const img = new Image();
            const src = props.item.images_raw[0].image.content || "";

            img.src = "data:image/jpeg;base64," + src;

            try {
                await img.decode(); // Wait for the image to be decoded
                setImage(img);
                const imgClassName = img.width < img.height ? "img-contain" : "img-cover";
                setImageClassName(imgClassName);
            } catch (error) {
                // Handle image loading errors here
                console.error("Error loading image:", error);
            }
        };

        if (props.item.images_raw[0].image.content) {
            loadImage();
        }
    }, [props.item]);

    return (
        <>
            <div className="r-list-item">
                {image && image.src ? (
                    <>
                        <div className="r-item-img">
                            <div
                                className="r-content-figure-blur"
                                style={{ backgroundImage: "url(" + image.src + ")" }}
                            />
                            <img
                                className={"r-content-figure-img" + " " + imageClassName}
                                src={image.src}
                                alt=""
                            />
                        </div>
                    </>
                ) : (
                    <>
                        <div className="r-item-img r-item-img-placeholder"></div>
                    </>
                )}
                <div className="r-item-text">
                    <span className="r-item-title">{props.item.nom}</span>
                    <div className="campaign-vote">
                        <div className="campaign-vote-pour">
                            <i className="bi bi-hand-thumbs-up-fill"></i>
                            <span className="campaign-vote-pour-count">
                                {props.item.votes_pour}
                            </span>
                        </div>
                        <div className="campaign-vote-contre">
                            <i className="bi bi-hand-thumbs-down-fill"></i>
                            <span className="campaign-vote-contre-count">
                                {props.item.votes_contre}
                            </span>
                        </div>
                    </div>
                </div>
                <div className="r-item-arrow">
                    <i class="bi bi-chevron-right"></i>
                </div>
            </div>
        </>
    );
};

export default CampaignCard;
