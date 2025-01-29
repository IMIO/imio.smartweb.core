import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";
import ReactMarkdown from "react-markdown";
import "spotlight.js";
import "../../../../node_modules/flexbin/flexbin.css";
import { Translate } from "react-translated";
import queryString from "query-string";

const CampaignContent = ({ queryUrl, onChange, contextAuthenticatedUser }) => {
    const navigate = useNavigate();
    const { u, ...parsed } = Object.assign({
        id: queryString.parse(useFilterQuery().toString())["u"],
        b_start: 0,
    });
    const [params, setParams] = useState(parsed);
    const [item, setitem] = useState(null);
    const [files, setFiles] = useState();
    const [image, setImage] = useState(new Image());
    const [imageClassName, setImageClassName] = useState("");
    const { response } = useAxios(
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

    // set all contacts state
    useEffect(() => {
        if (response !== null) {
            setitem(response.fields);
        }
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "instant",
        });
    }, [response]);

    // Set image and image className
    useEffect(() => {
        const loadImage = async () => {
            const img = new Image();
            const src = item.images_raw[0].image.b64 || "";

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

        if (item && item.images_raw[0].image.b64) {
            loadImage();
        }
    }, [item]);

    function handleClick() {
        navigate("..");
        onChange(null);
    }
    console.log(item);

    return (
        item && (
            <div className="annuaire-content r-content">
                <button type="button" onClick={handleClick}>
                    <Translate text="Retour" />
                </button>

                <article>
                    <header>
                        <h2 className="r-content-title">{item.nom}</h2>
                    </header>
                    {image ? (
                        <figure>
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
                        </figure>
                    ) : (
                        <>
                            <div className="r-item-img r-item-img-placeholder"></div>
                        </>
                    )}
                </article>
                <div className="contactCard">
                    <div className="contactText">
                        <div className="r-content-description">
                            {item.description && (
                                <div
                                    className="campaign-description"
                                    dangerouslySetInnerHTML={{
                                        __html: item.description,
                                    }}
                                />
                            )}
                        </div>
                        <div className="contactTextAll"></div>
                    </div>
                    {/* add files to download */}
                    {/* {files && (
                    <div className="r-content-files">
                        {files.map((file, i) => (
                            <div key={i} className="r-content-file">
                                <a
                                    href={file.targetUrl}
                                    className="r-content-file-link"
                                    rel="nofollow"
                                >
                                    <span className="r-content-file-title">{file.title}</span>
                                    <span className="r-content-file-icon">
                                        <svg
                                            width="21"
                                            height="21"
                                            viewBox="0 0 24 24"
                                            fill="none"
                                            stroke="#8899a4"
                                            stroke-width="2"
                                            stroke-linecap="square"
                                            stroke-linejoin="arcs"
                                        >
                                            <path d="M3 15v4c0 1.1.9 2 2 2h14a2 2 0 0 0 2-2v-4M17 9l-5 5-5-5M12 12.8V2.5"></path>
                                        </svg>
                                    </span>
                                </a>
                            </div>
                        ))}
                    </div>
                )} */}
                </div>
            </div>
        )
    );
};
export default CampaignContent;
