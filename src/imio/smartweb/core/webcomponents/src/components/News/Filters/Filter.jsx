import React, { useEffect, useCallback, useRef, useState } from "react";
import Select from "react-select";
import { useNavigate } from "react-router-dom";
import useAxios from "../../../hooks/useAxios";
import { Translator, Translate} from "react-translated";
import queryString from "query-string";
import { iam } from "./../../Filters/IamData";
import { menuStyles } from "./../../Filters/SelectStyles";

function Filters(props) {
    let navigate = useNavigate();
    const [inputValues, setInputValues] = useState(props.activeFilter);
    const [topicsFilter, setTopicsFilter] = useState(null);
    const [taxonomyFilter, setTaxonomyFilter] = useState(null);
    const [localsCategoryFilter, setLocalsCategoryFilter] = useState([]);
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
            const optionsTopics = response.topics.map((d) => ({
                value: d.token,
                label: d.title,
            }));
            const optionsTaxonomy = response.category
                ? response.category.map((d) => ({
                      value: d.token,
                      label: d.title,
                      queryString: "category",
                  }))
                : "";
            const optionsLocalsCategory =
                response.local_category &&
                response.local_category.map((d) => ({
                    value: d.token,
                    label: d.title,
                    queryString: "local_category",
                }));
            setTopicsFilter(optionsTopics);
            setTaxonomyFilter(optionsTaxonomy);
            setLocalsCategoryFilter(optionsLocalsCategory)
        }
    }, [response]);

    // const to group category and local category
    const groupedOptions = [
        {
            label: <Translate text="Catégories spécifiques" />,
            options: localsCategoryFilter,
        },
        {
            label: <Translate text="Catégories" />,
            options: taxonomyFilter,
        },
    ];

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

    const onChangeGroupSelect = useCallback((value, action) => {
        if (value) {
            setInputValues((state) => ({ ...state, [value.queryString]: value.value }), []);
        } else {
            setInputValues((prevState) => {
                const state = { ...prevState };
                const { [action.removedValues[0].queryString]: remove, ...rest } = state;
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
        taxonomyFilter.filter((option) => option.value === props.activeFilter.category);
    
    let actIam = iam && iam.filter((option) => option.value === props.activeFilter.topics);

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
                    <div className="react-sep-menu"></div>
                    <div className="r-filter top-filter topics-Filter">
                        {/* <label>Thématiques</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={menuStyles}
                                    name={"topics"}
                                    className="select-custom-no-border library-topics"
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
                    <div className="react-sep-menu"></div>
                    <div className="r-filter top-filter facilities-Filter">
                        {/* <label>Catégories</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={menuStyles}
                                    name={"category"}
                                    className="select-custom-no-border library-facilities"
                                    isClearable
                                    onChange={onChangeGroupSelect}
                                    options={localsCategoryFilter.length === 0 ? taxonomyFilter &&  taxonomyFilter : groupedOptions}
                                    placeholder={translate({
                                        text: "Catégories",
                                    })}
                                    value={actTaxo && actTaxo[0]}
                                />
                            )}
                        </Translator>
                    </div>
                    <div className="react-sep-menu"></div>
                    {/* Filtre iam */}
                    <div className="r-filter top-filter iam-Filter">
                        {/* <label>Thématiques</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={menuStyles}
                                    name={"iam"}
                                    className="select-custom-no-border library-topics"
                                    isClearable
                                    onChange={onChangeHandlerSelect}
                                    options={iam && iam}
                                    placeholder={translate({
                                        text: "Profil",
                                    })}
                                    value={actIam && actIam[0]}
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
