import React, { useEffect, useCallback, useState } from "react";
import Select from "react-select";
import useAxios from "../../../hooks/useAxios";

function Filters(props) {
    const [inputValues, setInputValues] = useState({});
    const [topicsFilter, setTopicsFilter] = useState(null);
    const [taxonomyFilter, setTaxonomyFilter] = useState(null);
    const { response, error, isLoading } = useAxios({
        method: "get",
        url: "",
        baseURL: props.url,
        headers: {
            Accept: "application/json",
        },
        params: "",
    });

    useEffect(() => {
        if (response !== null) {
            const optionsTopics = response.topics.map((d) => ({
                value: d.token,
                label: d.title,
            }));
            const optionsTaxonomy = response.taxonomy_contact_category
                ? response.taxonomy_contact_category.map((d) => ({
                      value: d.token,
                      label: d.title,
                  }))
                : "";
            setTopicsFilter(optionsTopics);
            setTaxonomyFilter(optionsTaxonomy);
        }
    }, [response]);

    const onChangeHandler = useCallback(({ target: { name, value } }) =>
        setInputValues((state) => ({ ...state, [name]: value }), [])
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
        props.onChange(inputValues);
    }, [inputValues]);

    function handleSubmit(e) {
        e.preventDefault();
        props.onChange(inputValues);
    }

    // console.log(inputValues);

    return (
        <React.Fragment>
            {/* <form onSubmit={handleSubmit}>
                <label>
                    Recherche
                    <input
                        name="search" type="text"
                        value={inputValues.search}
                        onChange={onChangeHandler} />
                </label>
                <button type="submit">Do the thing</button>
            </form> */}
            <div className="r-filter  facilities-Filter">
                <span>Catégories</span>
                <Select
                    name={"taxonomy_contact_category"}
                    className="select-custom-class library-facilities"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={taxonomyFilter && taxonomyFilter}
                    placeholder={"Toutes"}
                />
            </div>
            <div className="r-filter topics-Filter">
                <span>Thématiques</span>
                <Select
                    name={"topics"}
                    className="select-custom-class library-topics"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={topicsFilter && topicsFilter}
                    placeholder={"Toutes"}
                />
            </div>
        </React.Fragment>
    );
}

export default Filters;
