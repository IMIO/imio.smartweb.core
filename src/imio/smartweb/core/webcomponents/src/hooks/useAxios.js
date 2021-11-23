import { useState, useEffect } from "react";
import axios from "axios";

const useAxios = (params) => {
    const [response, setResponse] = useState(null);
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(true);

    const fetchData = async (params) => {
        setIsLoading(true);
        try {
            const res = await axios.request(params);
            // console.log(params);
            setResponse(res.data);
            setError(null);
        } catch (err) {
            setError(err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchData(params);
    }, [params.params]);
    return { response, error, isLoading };
};

export default useAxios;
