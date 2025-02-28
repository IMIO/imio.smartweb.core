import { useState, useEffect } from "react";
import axios from "axios";

const useAxios = (params) => {
    const [response, setResponse] = useState(null);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(true);
    const [isMore, setIsMore] = useState(false);
    const controller = new AbortController();

    const fetchData = async (params) => {
        setIsLoading(true);

        if (params.load) {
            setIsMore(true);
        } else {
            setIsMore(false);
        }

        if (Object.keys(params.params).length === 0) {
            setResponse(null);
            return;
        }

        try {
            // Handle multiple URLs with identifiers
            if (Array.isArray(params.url)) {
                const requests = params.url.map((urlConfig, index) => {
                    const { url, identifier } =
                        typeof urlConfig === "string"
                            ? { url: urlConfig, identifier: `request_${index}` }
                            : urlConfig;

                    return axios
                        .request({
                            ...params,
                            url,
                            signal: controller.signal,
                        })
                        .then((res) => ({
                            identifier,
                            data: res.data,
                        }));
                });

                const responses = await Promise.all(requests);
                // Convert array to object with identifiers as keys
                const responseObject = responses.reduce((acc, { identifier, data }) => {
                    acc[identifier] = data;
                    return acc;
                }, {});

                setResponse(responseObject);
            }
            // Handle single URL
            else {
                const res = await axios.request(params);
                setResponse(res.data);
            }
            setIsLoading(false);
            setError(null);
        } catch (err) {
            setError(err);
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchData({ ...params, signal: controller.signal });
        return () => controller.abort();
    }, [params.params]);

    return { response, error, isLoading, isMore };
};

export default useAxios;
