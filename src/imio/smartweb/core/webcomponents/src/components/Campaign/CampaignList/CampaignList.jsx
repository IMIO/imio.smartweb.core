import React, { useEffect, useState, useContext, createContext } from "react";
import useAxios from "../../../hooks/useAxios";
import { Link } from "react-router-dom";
import removeAccents from "remove-accents";
import CampaignCard from "../CampaignCard/CampaignCard";
const CampaignList = (props) => {
    const [filters, setFilters] = useState({ b_start: 0 });
    const [itemsArray, setItemsArray] = useState([]);
    const { response, error, isLoading, isMore } = useAxios(
        {
            method: "get",
            url: "",
            baseURL: props.queryUrl,
            headers: {
                Accept: "application/json",
            },
            params: filters,
        },
        []
    );

    useEffect(() => {
        response && setItemsArray(response.items);
    }, [response]);

    return (
        <>
            {isLoading ? (
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
            ) : (
                <ul className="r-result-list campaign-result-list row">
                    {itemsArray.map((item, i) => (
                        <li className="col-sm-6 col-md-4 col-lg-3 compaign-li" key={i}>
                            <Link
                                className="r-list-item-link"
                                style={{ textDecoration: "none" }}
                                to={{
                                    pathname:
                                        "/" +
                                        removeAccents(item.text)
                                            .replace(/[^a-zA-Z ]/g, "")
                                            .replace(/\s/g, "-")
                                            .toLowerCase(),
                                    search: `?u=${item.id}`,
                                    state: {
                                        idItem: item.id,
                                    },
                                }}
                            ></Link>
                            <CampaignCard item={item} />
                        </li>
                    ))}
                </ul>
            )}
        </>
    );
};
export default CampaignList;
