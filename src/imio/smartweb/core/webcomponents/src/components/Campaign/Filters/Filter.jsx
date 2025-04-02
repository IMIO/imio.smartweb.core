import React, { useEffect, useRef, useCallback, useState } from "react";
import Select from "react-select";
import { useNavigate } from "react-router-dom";
import useAxios from "../../../hooks/useAxios";
import { Translator, Translate } from "react-translated";
// import DateFilter from "../../Filters/DateFilter";
import moment from "moment";
import queryString from "query-string";
// import { taxonomy_event_public } from "./../../Filters/PublicTargetData";
// import { iam } from "./../../Filters/IamData";
import { menuStyles, moreFilterStyles } from "./../../Filters/SelectStyles";

function Filters(props) {
    let navigate = useNavigate();
    const [inputValues, setInputValues] = useState(props.activeFilter);
    const [searchValue, setSearchValue] = useState(null);
    const [topicsFilter, setTopicsFilter] = useState([]);
    const [zonesFilter, setZonesFilter] = useState([]);
    // Get data
    const { response, error, isLoading } = useAxios({
        method: "get",
        url: [
            { url: props.queryZonesUrl, identifier: "zones" },
            { url: props.queryTopicsUrl, identifier: "topics" },
        ],
        headers: {
            Accept: "application/json",
        },
        params: inputValues,
        paramsSerializer: { indexes: null },
    });

    // set fitlers data to state
    useEffect(() => {
        if (response !== null) {
            const optionsTopics =
                response.topics &&
                response.topics.items.map((d) => ({
                    value: d.value,
                    label: d.title,
                }));
            const optionsCategory =
                response.category &&
                response.category.map((d) => ({
                    value: d.token,
                    label: d.title,
                    queryString: "category",
                }));
            const optionsZones =
                response.zones &&
                response.zones.items.map((d) => ({
                    value: d.id,
                    label: d.digest,
                    queryString: "zones",
                }));
            setTopicsFilter(optionsTopics);
            setZonesFilter(optionsZones);
        }
    }, [response]);

    const onChangeHandler = useCallback(({ target: { name, value } }) => {
        if (value.length > 2) {
            setSearchValue(value);
            props.onChangeSearch(value);
        } else {
            setSearchValue(null);
            props.onChangeSearch(null);
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
        navigate({
            pathname: "./",
            search: queryString.stringify(inputValues),
        });
        props.onChange(inputValues);
    }, [inputValues, searchValue]);

    function handleSubmit(e) {
        e.preventDefault();
        props.onChange(inputValues);
        props.onChangeSearch(searchValue);
    }
    // set default input value
    let actTopi =
        topicsFilter && topicsFilter.filter((option) => option.value === props.activeFilter.topics);

    let actZones =
        zonesFilter && zonesFilter.filter((option) => option.value === props.activeFilter.zones);
    return (
        <React.Fragment>
            <div className="react-filters-menu">
                <div className="react-filters-container">
                    <form className="r-filter r-filter-search" onSubmit={handleSubmit}>
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

                    {/* <div className="react-sep-menu"></div> */}
                    {/* Filtre Thématique */}
                    {/* Filtre Thématique */}
                    <div className="r-filter top-filter topics-Filter">
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={menuStyles}
                                    name={"filter-themes"}
                                    className="select-custom-no-border"
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

                    <div className="r-filter top-filter topics-Filter">
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={menuStyles}
                                    name={"filter-zones"}
                                    className="select-custom-no-border"
                                    isClearable
                                    onChange={onChangeHandlerSelect}
                                    options={zonesFilter && zonesFilter}
                                    placeholder={translate({
                                        text: "Zones",
                                    })}
                                    value={actZones && actZones[0]}
                                />
                            )}
                        </Translator>
                    </div>
                </div>
            </div>
        </React.Fragment>
    );
}

export default Filters;
