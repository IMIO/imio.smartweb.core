import React, { useEffect, useCallback, useRef, useState } from "react";
import Select from "react-select";
import { useHistory } from "react-router-dom";
import axios from "axios";
function Filters(props) {
    let history = useHistory();
    const queryString = require("query-string");

    const [inputValues, setInputValues] = useState(props.activeFilter);
    const [searchValues, setSearchValues] = useState({});
    const [topicsFilter, setTopicsFilter] = useState(null);
    const [iamFilter, setIamFilter] = useState(null);
    const apiCall = () => {
        const requestOne = axios.request({
            method: "get",
            url: "",
            baseURL: props.url + "/@vocabularies/imio.smartweb.vocabulary.Topics",
            headers: {
                Accept: "application/json",
            },
        });

        const requestTwo = axios.request({
            method: "get",
            url: "",
            baseURL: props.url + "/@vocabularies/imio.smartweb.vocabulary.IAm",
            headers: {
                Accept: "application/json",
            },
        });

        axios
            .all([requestOne, requestTwo])
            .then(
                axios.spread((...responses) => {
                    const responseOne = responses[0];
                    const responseTwo = responses[1];
                    if (responseOne !== null) {
                        const optionsTopics = responseOne.data.items.map((d) => ({
                            value: d.token,
                            label: d.title,
                        }));
                        setTopicsFilter(optionsTopics);
                    }
                    if (responseTwo !== null) {
                        const optionsIam = responseTwo.data.items.map((d) => ({
                            value: d.token,
                            label: d.title,
                        }));
                        setIamFilter(optionsIam);
                    }
                })
            )
            .catch((errors) => {
                // react on errors.
                console.error("errors");
            });
    };

    useEffect(() => {
        apiCall();
    }, []);

    const HandlerText = (e) => {
        setSearchValues({ SearchableText: e.target.value });
        if (e.target.value) {
            setInputValues((state) => ({ ...state, SearchableText: e.target.value }), []);
        } else {
            setInputValues((prevState) => {
                const state = { ...prevState };
                const { SearchableText: remove, ...rest } = state;
                return rest;
            });
        }
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        if (searchValues.SearchableText) {
            setInputValues(
                (state) => ({ ...state, SearchableText: searchValues.SearchableText }),
                []
            );
        } else {
            setInputValues((prevState) => {
                const state = { ...prevState };
                const { SearchableText: remove, ...rest } = state;
                return rest;
            });
        }
    };
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

    // set default input value
    let actTopi =
        topicsFilter && topicsFilter.filter((option) => option.value === props.activeFilter.topics);
    let actIam = iamFilter && iamFilter.filter((option) => option.value === props.activeFilter.iam);
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
            <div className="col-md-6 py-1 r-search search-bar-filter">
                <form onSubmit={handleSubmit}>
                    <label>
                        <input
                            name="SearchableText"
                            type="text"
                            onChange={HandlerText}
                            value={searchValues.SearchableText}
                            placeholder={"Recherche"}
                        />
                    </label>
                    <button type="submit"></button>
                </form>
            </div>
            <div className="col-md-3 col-lg-2 py-1 r-search search-select-filter">
                <Select
                    styles={customStyles}
                    name={"iam"}
                    className="r-search-select"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={iamFilter && iamFilter}
                    placeholder={"Je suis"}
                    value={actIam && actIam[0]}
                />
            </div>
            <div className="col-md-3 col-lg-2 py-1 r-search search-select-filter">
                <Select
                    styles={customStyles}
                    name={"topics"}
                    className="r-search-select"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={topicsFilter && topicsFilter}
                    placeholder={"Thématiques"}
                    value={actTopi && actTopi[0]}
                />
            </div>
        </React.Fragment>
    );
}

export default Filters;
