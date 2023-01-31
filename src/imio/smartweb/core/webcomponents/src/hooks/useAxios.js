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
        if (Object.keys(params.params).length == 0) {
            setResponse(null);
            return;
        } else {
            try {
                const res = await axios.request(params);
                setResponse(res.data);
                setIsLoading(false);
                setError(null);
            } catch (err) {
                setError(err);
            }
        }
    };
    // console.log(isLoading);
    // console.log(response);

    useEffect(() => {
        fetchData({...params,signal: controller.signal});
        return() => controller.abort()
    }, [params.params]);
    return { response, error, isLoading, isMore };
};

export default useAxios;
