import { useNavigate } from "react-router-dom";
import React, { useEffect, useState, useRef } from "react";
import useFilterQuery from "../../../hooks/useFilterQuery";
import queryString from "query-string";

const ContactContent = (props) => {
    let navigate = useNavigate();
    const [item, setitem] = useState({});
    const modalRef = useRef();

    function handleClick() {
        navigate("..");
        onChange(null);
    }

    return (
        <div className="envent-content r-content">
            <h2>le contenu</h2>
        </div>
    );
};
export default ContactContent;
