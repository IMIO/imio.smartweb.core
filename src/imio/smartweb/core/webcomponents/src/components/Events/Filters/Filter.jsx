import React, { useEffect, useRef, useCallback, useState } from "react";
import Select from "react-select";
import { useNavigate } from "react-router-dom";
import useAxios from "../../../hooks/useAxios";
import { Translator } from "react-translated";
import DateFilter from "../../Filters/DateFilter";
import moment from "moment";
import queryString from "query-string";
import { taxonomy_event_public } from "./../../Filters/PublicTargetData";
import { iam } from "./../../Filters/IamData";
import { menuStyles, moreFilterStyles } from "./../../Filters/SelectStyles";

function Filters(props) {
    let navigate = useNavigate();
    const [inputValues, setInputValues] = useState(props.activeFilter);
    const [topicsFilter, setTopicsFilter] = useState(null);
    const [categoryFilter, setCategoryFilter] = useState(null);
    const [dates, setDates] = useState(null);
    // Get data
    const { response, error, isLoading } = useAxios({
        method: "get",
        url: "",
        baseURL: props.url,
        headers: {
            Accept: "application/json",
        },
        params: inputValues,
        paramsSerializer: { indexes: null },
    });

    useEffect(() => {
        if (response !== null) {
            const optionsTopics =
                response.topics &&
                response.topics.map((d) => ({
                    value: d.token,
                    label: d.title,
                }));
            const optionsCategory =
                response.category &&
                response.category.map((d) => ({
                    value: d.token,
                    label: d.title,
                }));
            setTopicsFilter(optionsTopics);
            setCategoryFilter(optionsCategory);
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

    const onChangeCheckbox = useCallback((value, action) => {
        console.log(value.target.checked);
        if (value.target.checked) {
            setInputValues((state) => ({ ...state, free_entry: true }), []);
        } else {
            setInputValues((state) => {
                const newState = { ...state };
                delete newState["free_entry"];
                return newState;
            }, []);
        }
    });

    // make to no launch useEffect first time
    const firstUpdate = useRef(true);
    useEffect(() => {
        if (firstUpdate.current) {
            firstUpdate.current = false;
            return;
        }
        navigate({
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

    let actCategory =
        categoryFilter &&
        categoryFilter.filter((option) => option.value === props.activeFilter.category);

    let actTarget =
        taxonomy_event_public &&
        taxonomy_event_public.filter((option) => option.value === props.activeFilter.topics);

    useEffect(() => {
        if (dates) {
            setInputValues((prevState) => {
                if (dates["event_dates.query"].length > 1) {
                    const { "event_dates.range": _, ...rest } = dates;
                    const newValue = "min:max";
                    return { ...prevState, ...rest, "event_dates.range": newValue };
                } else if (dates["event_dates.query"].every((item) => item === null)) {
                    return {
                        ...prevState,
                        "event_dates.query": [moment().format("YYYY-MM-DD")],
                        "event_dates.range": "min",
                    };
                } else {
                    return { ...prevState, ...dates, "event_dates.range": "min" };
                }
            });
        }
    }, [dates]);

    return (
        <React.Fragment>
            <div className="react-filters-menu">
                <div className="react-filters-container">
                    <form className="r-filter r-filter-search" onSubmit={handleSubmit}>
                        {/* <label>Recherche</label> */}
                        <div className="relative">
                            <Translator>
                                {({ translate }) => (
                                    <input
                                        className="input-custom-class"
                                        name="SearchableText"
                                        type="text"
                                        value={inputValues.SearchableText}
                                        onChange={onChangeHandler}
                                        placeholder={translate({
                                            text: "Recherche",
                                        })}
                                    />
                                )}
                            </Translator>
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                stroke="#9f9f9f"
                                strokeWidth="4"
                                aria-hidden="true"
                                display="block"
                                overflow="visible"
                                style={{ height: 16, width: 16 }}
                                viewBox="0 0 32 32"
                            >
                                <path d="M13 24a11 11 0 1 0 0-22 11 11 0 0 0 0 22zm8-3 9 9" />
                            </svg>
                        </div>
                    </form>
                    {/* More filter*/}
                    <button
                        className="more-filter-btn collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#collapseOne"
                        aria-expanded="false"
                        aria-controls="collapseOne"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 32 32"
                            style={{ height: 16, width: 16 }}
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="3"
                            aria-hidden="true"
                            display="block"
                            overflow="visible"
                        >
                            <path d="M7 16H3m26 0H15M29 6h-4m-8 0H3m26 20h-4M7 16a4 4 0 108 0 4 4 0 00-8 0zM17 6a4 4 0 108 0 4 4 0 00-8 0zm0 20a4 4 0 108 0 4 4 0 00-8 0zm0 0H3"></path>
                        </svg>
                    </button>
                    <div className="react-sep-menu"></div>
                    {props.onlyPastEvents === "False" && (
                        <div className="r-filter  schedul-Filter">
                            <DateFilter language={props.language} setDates={setDates} />
                        </div>
                    )}
                    <div className="react-sep-menu"></div>

                    <div className="r-filter  facilities-Filter">
                        {/* <label>Catégories</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={menuStyles}
                                    name={"category"}
                                    className="select-custom-no-border library-facilities"
                                    isClearable
                                    onChange={onChangeHandlerSelect}
                                    options={categoryFilter && categoryFilter}
                                    placeholder={translate({
                                        text: "Quoi",
                                    })}
                                    value={actCategory && actCategory[0]}
                                />
                            )}
                        </Translator>
                    </div>
                </div>
            </div>

            {/* More filter */}

            <div
                id="collapseOne"
                className="accordion-collapse collapse more-filter-container "
                aria-labelledby="headingOne"
                data-bs-parent="#accordionExample"
            >
                <div className="accordion-body">
                    {/* Filtre thématique */}
                    <div className="r-filter topics-Filter">
                        {/* <label>Thématiques</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={moreFilterStyles}
                                    name={"topics"}
                                    className="library-topics"
                                    isClearable
                                    onChange={onChangeHandlerSelect}
                                    options={topicsFilter && topicsFilter}
                                    placeholder={translate({
                                        text: "Thématiques",
                                    })}
                                    value={actTopi && actTopi[0]}
                                />
                            )}
                        </Translator>
                    </div>
                    {/* Filtre Public cible */}
                    <div className="r-filter public-target-Filter">
                        {/* <label>Thématiques</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={moreFilterStyles}
                                    name={"taxonomy_event_public"}
                                    className="library-topics"
                                    isClearable
                                    onChange={onChangeHandlerSelect}
                                    options={taxonomy_event_public && taxonomy_event_public}
                                    placeholder={translate({
                                        text: "Public cible",
                                    })}
                                    value={actTarget && actTarget[0]}
                                />
                            )}
                        </Translator>
                    </div>

                    {/* Filtre iam */}
                    <div className="r-filter iam-Filter">
                        {/* <label>Thématiques</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={moreFilterStyles}
                                    name={"iam"}
                                    className="library-topics"
                                    isClearable
                                    onChange={onChangeHandlerSelect}
                                    options={iam && iam}
                                    placeholder={translate({
                                        text: "Profil",
                                    })}
                                    value={actTarget && actTarget[0]}
                                />
                            )}
                        </Translator>
                    </div>

                    {/* Filtre Gratuit */}
                    <div className="r-filter free-Filter">
                        {/* <label>Thématiques</label> */}
                        <div className="form-check form-switch">
                            <label className="form-check-label" htmlFor="flexSwitchCheckDefault">
                                Gratuit
                            </label>
                            <input
                                className="form-check-input"
                                onChange={onChangeCheckbox}
                                type="checkbox"
                                id="flexSwitchCheckDefault"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </React.Fragment>
    );
}

export default Filters;
