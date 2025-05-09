import React, { useEffect, useContext } from "react";
import ContactCard from "../ContactCard/ContactCard";
import { Link } from "react-router-dom";
import removeAccents from "remove-accents";
import { ScrollContext } from "../../../hooks/ScrollContext";
const ContactList = ({ contactArray, onChange, onHover, contextAuthenticatedUser }) => {
    const { scrollPos, updateScrollPos } = useContext(ScrollContext);

    function handleClick(event) {
        onChange(event);
        updateScrollPos(window.scrollY);
    }

    function handleHover(event) {
        onHover(event);
    }

    useEffect(() => {
        window.scrollTo({ top: scrollPos, left: 0, behavior: "instant" });
    }, [contactArray]);

    useEffect(() => {
        // Liste complète de toutes les balises possibles
        const allMetaProps = [
            { name: "description" },
            { property: "og:title" },
            { property: "og:description" },
            { property: "og:url" },
            { property: "og:type" },
            { property: "og:image" },
            { property: "og:image:type" },
            { property: "og:image:alt" },
            { property: "og:image:width" },
            { property: "og:image:height" },
        ];
    
        // Supprime les anciennes balises
        allMetaProps.forEach(({ name, property }) => {
            const selector = name ? `meta[name="${name}"]` : `meta[property="${property}"]`;
            const existing = document.head.querySelector(selector);
            if (existing) {
                document.head.removeChild(existing);
            }
        });

        const metaUpdates = [
            { name: "description", content: "Annuaire" },
            { property: "og:title", content: "Annuaire" },
            { property: "og:description", content: "Annuaire" },
            { property: "og:url", content: typeof window !== "undefined" ? window.location.href : "" },
            { property: "og:type", content: "website" },
        ];

        metaUpdates.forEach(({ name, property, content }) => {
            const selector = name ? `meta[name="${name}"]` : `meta[property="${property}"]`;
            let tag = document.head.querySelector(selector);

            if (!tag) {
                tag = document.createElement("meta");
                if (name) tag.setAttribute("name", name);
                if (property) tag.setAttribute("property", property);
                document.head.appendChild(tag);
            }

            tag.setAttribute("content", content);
        });
    }, []);
    return (
        <React.Fragment>
            <ul className="r-result-list annuaire-result-list">
                {contactArray.map((item, i) => (
                    <li
                        key={i}
                        className="r-list-item-group"
                        onMouseEnter={() => handleHover(item.UID)}
                        onMouseLeave={() => handleHover(null)}
                        onClick={() => handleClick(item.UID)}
                    >
                        <Link
                            className="r-list-item-link"
                            style={{ textDecoration: "none" }}
                            to={{
                                pathname:
                                    "/" +
                                    removeAccents(item.title)
                                        .replace(/[^a-zA-Z ]/g, "")
                                        .replace(/\s/g, "-")
                                        .toLowerCase(),
                                search: `?u=${item.UID}`,
                                state: {
                                    idItem: item.UID,
                                },
                            }}
                        ></Link>
                        <ContactCard
                            item={item}
                            contextAuthenticatedUser={contextAuthenticatedUser}
                            key={item.created}
                        />
                    </li>
                ))}
            </ul>
        </React.Fragment>
    );
};
export default ContactList;
