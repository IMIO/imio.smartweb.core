import React, { useEffect, useCallback, useState } from "react";
import Select from "react-select";
import { BrowserRouter as Router, Link, useHistory } from "react-router-dom";
import useAxios from "../../../hooks/useAxios";
import useFilterQuery from "../../../hooks/useFilterQuery";

function Filters(props) {
    let history = useHistory();
    const queryString = require("query-string");
    // const parsed = queryString.parse(useFilterQuery().toString());
    const [inputValues, setInputValues] = useState(props.activeFilter);
    const [topicsFilter, setTopicsFilter] = useState(null);
    const [taxonomyFilter, setTaxonomyFilter] = useState(null);
    const [facilitiesFilter, setFacilitiesFilter] = useState(null);
    const { response, error, isLoading } = useAxios({
        method: "get",
        url: "",
        baseURL: props.url,
        headers: {
            Accept: "application/json",
        },
        params: inputValues,
    });

    useEffect(() => {
        if (response !== null) {
            const optionsTopics =
                response.topics &&
                response.topics.map((d) => ({
                    value: d.token,
                    label: d.title,
                }));
            const optionsTaxonomy =
                response.category &&
                response.category.map((d) => ({
                    value: d.token,
                    label: d.title,
                }));
            const optionsFacilities =
                response.facilities &&
                response.facilities.map((d) => ({
                    value: d.token,
                    label: d.title,
                }));
            setTopicsFilter(optionsTopics);
            setTaxonomyFilter(optionsTaxonomy);
            setFacilitiesFilter(optionsFacilities);
        }
    }, [response]);

    const onChangeHandler = useCallback(({ target: { name, value } }) =>{
        if (value) {
            setInputValues((state) => ({ ...state, [name]: value }), [])
        } else{
            setInputValues((prevState) => {
                const state = { ...prevState };
                const { [name]: remove, ...rest } = state;
                return rest;
            });
        }
    }
    );
    const onChangeHandlerSelect = useCallback((value, action) => {
        const inputName = action.name;
        if (value) {
            setInputValues((state) => ({ ...state, [inputName]: value.value }), []);
        } else {
            setInputValues((prevState) => {
                const state = { ...prevState };
                const { [inputName]: remove, ...rest } = state;
                return rest;
            });
        }
    });

    useEffect(() => {
        history.push({
            pathname: "",
            search: queryString.stringify(inputValues),
        });

        props.onChange(inputValues);
    }, [inputValues]);

    function handleSubmit(e) {
        e.preventDefault();
        props.onChange(inputValues);
    }
    // set default input value
    let actTopi =
        topicsFilter && topicsFilter.filter((option) => option.value === props.activeFilter.topics);

    let actTaxo =
        taxonomyFilter &&
        taxonomyFilter.filter(
            (option) => option.value === props.activeFilter.category
        );
    // let actFaci =
    //     facilitiesFilter &&
    //     facilitiesFilter.filter((option) => option.value === props.activeFilter.facilities);
    // console.log(topicsFilter)
    return (
        <React.Fragment>
            <form onSubmit={handleSubmit}>
                <label>
                    Recherche
                    <input
                        name="SearchableText" type="text"
                        value={inputValues.SearchableText}
                        onChange={onChangeHandler} />
                </label>
                <button type="submit">Recherche</button>
            </form>

            <div className="r-filter topics-Filter">
                <span>Thématiques</span>
                <Select
                    name={"topics"}
                    className="select-custom-class library-topics"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={topicsFilter && topicsFilter}
                    placeholder={"Toutes"}
                    value={actTopi && actTopi[0]}
                />
            </div>
            <div className="r-filter  facilities-Filter">
                <span>Catégories</span>
                <Select
                    name={"category"}
                    className="select-custom-class library-facilities"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={taxonomyFilter && taxonomyFilter}
                    placeholder={"Toutes"}
                    value={actTaxo && actTaxo[0]}
                />
            </div>
            {/* <div className="r-filter  facilities-Filter">
                <span>Période</span>
                <Select
                    name={"facilities"}
                    className="select-custom-class library-facilities"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={facilitiesFilter && facilitiesFilter}
                    placeholder={"Toutes"}
                    value={actFaci && actFaci[0]}
                />
            </div> */}
        </React.Fragment>
    );
}

export default Filters;
