import React, { useEffect, useState } from "react";
import { Translate } from "react-translated";

const CampaignCard = (props) => {
    const [image, setImage] = useState(new Image());
    const [imageClassName, setImageClassName] = useState("");

    // Set image and image className
    useEffect(() => {
        const loadImage = async () => {
            const img = new Image();
            const src = props.item.images_raw[0].image.b64 || "";

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

        if (props.item.images_raw[0].image.b64) {
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
                    <span className="r-item-title campaign-title">{props.item.text}</span>
                    <span className="r-item-title">{props.item.nom}</span>
                </div>
            </div>
        </>
    );
};

export default CampaignCard;
