import React, { useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import removeAccents from "remove-accents";
import CampaignCard from "../CampaignCard/CampaignCard";

const CampaignList = (props) => {
    return (
        <React.Fragment>
            <ul className="r-result-list actu-result-list row">
                {props.itemsArray.map((item, i) => (
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
        </React.Fragment>
    );
};
export default CampaignList;
