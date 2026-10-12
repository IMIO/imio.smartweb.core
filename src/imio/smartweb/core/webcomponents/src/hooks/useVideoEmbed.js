import { useEffect, useState } from "react";
import axios from "axios";

const VIMEO_OEMBED_URL = "https://vimeo.com/api/oembed.json";

// Hôtes autorisés pour le src de l'iframe, quoi que renvoie l'API distante.
const ALLOWED_EMBED_HOSTS = [
    "player.vimeo.com",
    "vimeo.com",
    "youtube.com",
    "www.youtube.com",
    "www.youtube-nocookie.com",
];

// Une entrée par URL de vidéo : on mémorise la promesse pour ne pas
// réinterroger l'API à chaque remontage du composant.
const cache = new Map();

const getProvider = (url) => {
    let host;
    try {
        host = new URL(url).hostname.replace(/^www\./, "");
    } catch (e) {
        return null;
    }
    if (host === "vimeo.com" || host.endsWith(".vimeo.com")) {
        return "vimeo";
    }
    if (host === "youtube.com" || host.endsWith(".youtube.com") || host === "youtu.be") {
        return "youtube";
    }
    return null;
};

// L'oEmbed renvoie un iframe tout fait : on en extrait uniquement le src pour
// garder la maîtrise du markup (classes, dimensions, attributs allow).
const extractIframeSrc = (html) => {
    if (typeof html !== "string") {
        return null;
    }
    const iframe = new DOMParser().parseFromString(html, "text/html").querySelector("iframe");
    const src = iframe && iframe.getAttribute("src");
    if (!src) {
        return null;
    }
    try {
        const parsed = new URL(src, "https://vimeo.com");
        if (parsed.protocol !== "https:" || !ALLOWED_EMBED_HOSTS.includes(parsed.hostname)) {
            return null;
        }
        return parsed.href;
    } catch (e) {
        return null;
    }
};

// Reconstruction "à la main", utilisée pour YouTube et en secours si
// l'oEmbed Vimeo est injoignable (vidéo privée, réseau, quota...).
export const getFallbackEmbedSrc = (url) => {
    const provider = getProvider(url);
    let parsed;
    try {
        parsed = new URL(url);
    } catch (e) {
        return null;
    }
    const segments = parsed.pathname.split("/").filter(Boolean);

    if (provider === "youtube") {
        const videoId = parsed.searchParams.get("v") || segments.pop();
        return videoId ? `https://www.youtube.com/embed/${videoId}` : null;
    }

    if (provider === "vimeo") {
        // Événement live : vimeo.com/event/<id>
        if (segments[0] === "event" && segments[1]) {
            return `https://vimeo.com/event/${segments[1]}/embed`;
        }
        // Vidéo classique, éventuellement non listée : vimeo.com/<id>[/<hash>]
        const idIndex = segments.findIndex((segment) => /^\d+$/.test(segment));
        if (idIndex === -1) {
            return null;
        }
        const id = segments[idIndex];
        const hash = segments[idIndex + 1];
        return hash
            ? `https://player.vimeo.com/video/${id}?h=${hash}`
            : `https://player.vimeo.com/video/${id}`;
    }

    return null;
};

const fetchEmbedSrc = (url) => {
    if (getProvider(url) !== "vimeo") {
        return Promise.resolve(getFallbackEmbedSrc(url));
    }
    if (!cache.has(url)) {
        cache.set(
            url,
            axios
                .get(VIMEO_OEMBED_URL, { params: { url } })
                .then((res) => extractIframeSrc(res.data && res.data.html))
                .catch(() => null)
                .then((src) => src || getFallbackEmbedSrc(url))
        );
    }
    return cache.get(url);
};

/**
 * Résout l'URL d'embed d'une vidéo YouTube ou Vimeo.
 *
 * Pour Vimeo on interroge l'oEmbed (https://vimeo.com/api/oembed.json) : c'est
 * lui qui sait si l'URL pointe vers une vidéo (player.vimeo.com/video/<id>) ou
 * vers un événement live (vimeo.com/event/<id>/embed), sans avoir à deviner à
 * partir de la forme de l'URL.
 */
const useVideoEmbed = (url) => {
    const [state, setState] = useState({ src: null, isLoading: Boolean(url) });

    useEffect(() => {
        if (!url) {
            setState({ src: null, isLoading: false });
            return;
        }
        let cancelled = false;
        setState({ src: null, isLoading: true });
        fetchEmbedSrc(url).then((src) => {
            if (!cancelled) {
                setState({ src, isLoading: false });
            }
        });
        return () => {
            cancelled = true;
        };
    }, [url]);

    return state;
};

export default useVideoEmbed;
