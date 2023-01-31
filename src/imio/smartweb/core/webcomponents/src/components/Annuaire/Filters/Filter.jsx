import React, { useEffect, useRef, useCallback, useState } from "react";
import Select from "react-select";
import { useHistory } from "react-router-dom";
import useAxios from "../../../hooks/useAxios";
import { Translator } from "react-translated";

function Filters(props) {
    let history = useHistory();
    const queryString = require("query-string");
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
                response.taxonomy_contact_category &&
                response.taxonomy_contact_category.map((d) => ({
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

    const onChangeHandler = useCallback(({ target: { name, value } }) => {
        if (value.length > 2) {
            setInputValues((state) => ({ ...state, [name]: value }), []);
        } else {
            setInputValues((prevState) => {
                const state = { ...prevState };
                const { [name]: remove, ...rest } = state;
                return rest;
            });
        }
    });
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

    // make to no launch useEffect first time
    const firstUpdate = useRef(true);
    useEffect(() => {
        if (firstUpdate.current) {
            firstUpdate.current = false;
            return;
        }
        history.push({
            pathname: "./",
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
            (option) => option.value === props.activeFilter.taxonomy_contact_category
        );
    let actFaci =
        facilitiesFilter &&
        facilitiesFilter.filter((option) => option.value === props.activeFilter.facilities);
    const customStyles = {
        control: (styles) => ({
            ...styles,
            backgroundColor: "white",
            borderRadius: "0",
            height: "50px",
        }),
        placeholder: (styles) => ({
            ...styles,
            color: "000",
            fontWeight: "bold",
            fontSize: "12px",
            textTransform: "uppercase",
            letterSpacing: "1.2px",
        }),
        option: (styles, { data, isDisabled, isFocused, isSelected }) => {
            return {
                ...styles,
            };
        },
    };

    return (
        <React.Fragment>
            <form className="r-filter" onSubmit={handleSubmit}>
                {/* <label>Recherche</label> */}
                <div className="r-filter-search">
                    <Translator>
                        {({ translate }) => (
                            <input
                                className="input-custom-class"
                                name="SearchableText"
                                type="text"
                                value={inputValues.SearchableText}
                                onChange={onChangeHandler}
                                placeholder={translate({
                                    text: 'Recherche'
                                })}
                            />
                        )}
                    </Translator>
                    <button type="submit"></button>
                </div>
            </form>

            <div className="r-filter topics-Filter">
                {/* <label>Thématiques</label> */}
                <Translator>
                    {({ translate }) => (
                        <Select
                            styles={customStyles}
                            name={"topics"}
                            className="select-custom-class library-topics"
                            isClearable
                            onChange={onChangeHandlerSelect}
                            options={topicsFilter && topicsFilter}
                            placeholder={translate({
                                text: 'Thématiques'
                            })}
                            value={actTopi && actTopi[0]}
                        />
                    )}
                </Translator>
            </div>
            <div className="r-filter  facilities-Filter">
                {/* <label>Catégories</label> */}
                <Translator>
                    {({ translate }) => (
                        <Select
                            styles={customStyles}
                            name={"taxonomy_contact_category_for_filtering"}
                            className="select-custom-class library-facilities"
                            isClearable
                            onChange={onChangeHandlerSelect}
                            options={taxonomyFilter && taxonomyFilter}
                            placeholder={translate({
                                text: 'Catégories'
                            })}
                            value={actTaxo && actTaxo[0]}
                        />
                    )}
                </Translator>
            </div>
            <div className="r-filter  facilities-Filter">
                {/* <label>Facilité</label> */}
                <Translator>
                    {({ translate }) => (
                <Select
                    styles={customStyles}
                    name={"facilities"}
                    className="select-custom-class library-facilities"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={facilitiesFilter && facilitiesFilter}
                    placeholder={translate({
                        text: 'Facilités'
                      })}
                    value={actFaci && actFaci[0]}
                />
                )}
                </Translator>
            </div>
        </React.Fragment>
    );
}

export default Filters;
