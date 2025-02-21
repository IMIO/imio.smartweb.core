import { useNavigate } from "react-router-dom";
import React, { useEffect, useState } from "react";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";
import "spotlight.js";
import "../../../../node_modules/flexbin/flexbin.css";
import { Translate } from "react-translated";
import queryString from "query-string";

export default function CampaignContent({ queryUrl, onChange }) {
    const navigate = useNavigate();
    const { u, ...parsed } = Object.assign({
        id: queryString.parse(useFilterQuery().toString())["u"],
        b_start: 0,
    });
    const [params, setParams] = useState(parsed);
    const [item, setitem] = useState(null);
    const [urlVotePour, setUrlVotePour] = useState(null);
    const [urlVoteContre, setUrlVoteContre] = useState(null);

    const [files, setFiles] = useState();
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

    // set all contacts state
    useEffect(() => {
        if (response !== null) {
            setitem(response.fields);
            const parsedUrl = new URL(response.url);
            const baseUrl = `${parsedUrl.protocol}//${parsedUrl.hostname}`;
            const fullUrlPour = `${baseUrl}/ideabox-voter-pour-un-projet/?projet=${response.id}`;
            const fullUrlContre = `${baseUrl}/ideabox-voter-contre-un-projet/?projet=${response.id}`;

            setUrlVotePour(fullUrlPour);
            setUrlVoteContre(fullUrlContre);
        }

        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "instant",
        });
    }, [response]);

    function handleClick() {
        navigate("..");
        onChange(null);
    }
    return !isLoading ? (
        <div className="campaign-content r-content">
            <button type="button" onClick={handleClick}>
                <Translate text="Retour" />
            </button>
            <ContentText item={item} urlVotePour={urlVotePour} urlVoteContre={urlVoteContre} />
        </div>
    ) : (
        <div className="lds-roller-container">
            <div className="lds-roller">
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
            </div>
        </div>
    );
}

function ContentText({ item, urlVotePour, urlVoteContre }) {
    const [image, setImage] = useState(new Image());
    const [imageClassName, setImageClassName] = useState("");

    useEffect(() => {
        if (item) {
            // Set image and image className
            const src = item.images_raw[0].image.content || "";
            const img = new Image();
            img.src = "data:image/jpeg;base64," + src;

            img.onload = () => {
                setImage(img);
                const imgClassName = img.width < img.height ? "img-contain" : "img-cover";
                setImageClassName(imgClassName);
            };

            img.onerror = (error) => {
                // Handle image loading errors here
                console.error("Error loading image:", error);
            };
        }
    }, [item]);
    return (
        <>
            <article>
                <header>
                    <h2 className="r-content-title">{item.nom}</h2>
                </header>
                <figure>
                    <div className="campaign-vote" style={{ marginTop: "1.5rem" }}>
                        <a href={urlVotePour} target="_blank" className="campaign-vote-pour">
                            <i className="bi bi-hand-thumbs-up-fill"></i>
                            <span className="campaign-vote-pour-count">({item.votes_pour})</span>
                            <span className="campaign-vote-contre-text"> Je vote pour</span>
                        </a>
                        <a href={urlVoteContre} target="_blank" className="campaign-vote-contre">
                            <i className="bi bi-hand-thumbs-down-fill"></i>
                            <span className="campaign-vote-contre-count">
                                ({item.votes_contre})
                            </span>
                            <span className="campaign-vote-contre-text"> Je vote contre</span>
                        </a>
                    </div>
                    {image ? (
                        <div className="r-content-img">
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
                    ) : (
                        <>
                            <div className="r-item-img r-item-img-placeholder"></div>
                        </>
                    )}
                </figure>
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
        </>
    );
}
