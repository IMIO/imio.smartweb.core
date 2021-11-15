import React from "react";
import { BrowserRouter as Router, Link, useLocation } from "react-router-dom";

function useFilterQuery() {
    return new URLSearchParams(useLocation().search);
}

export default useFilterQuery;
