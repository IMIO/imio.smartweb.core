import React, { useEffect, useRef, useCallback, useState } from "react";
import Select from "react-select";
import { useNavigate } from "react-router-dom";
import useAxios from "../../../hooks/useAxios";
import { Translator } from "react-translated";
import queryString from "query-string";
// import TaxonomyFilter from "../../Filters/TaxonomyFilter";
import { iam } from "./../../Filters/IamData";
import { menuStyles, moreFilterStyles } from "./../../Filters/SelectStyles";

function formatData(data) {
    let result = [];

    data.forEach((item) => {
        let titles = item.title.split(" » ");
        let token = item.token;

        let level = result;
        titles.forEach((title) => {
            let existingItem = level.find((x) => x.title === title);
            if (existingItem) {
                if (!existingItem.sub) {
                    existingItem.sub = [];
                }
                level = existingItem.sub;
            } else {
                let newItem = { title: title, token: token, sub: [] };
                level.push(newItem);
                level = newItem.sub;
            }
        });
    });

    // Remove empty 'sub' arrays
    const cleanResult = JSON.parse(JSON.stringify(result).replace(/,"sub":\[\]/g, ""));

    return cleanResult;
}

function Filters(props) {
    let navigate = useNavigate();
    const [inputValues, setInputValues] = useState(props.activeFilter);
    const [topicsFilter, setTopicsFilter] = useState([]);
    // const [taxonomyData, setTaxonomyData] = useState(null);
    const [taxonomyFilter, setTaxonomyFilter] = useState(null);
    const [facilitiesFilter, setFacilitiesFilter] = useState(null);
    const [cat, setCat] = useState(false);
    const [activeComponent, setActiveComponent] = useState(null);
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

            // const taxodonnee = formatData(response.taxonomy_contact_category);
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
            // setTaxonomyData(taxodonnee);
            setTaxonomyFilter(optionsTaxonomy);
            setFacilitiesFilter(optionsFacilities);
        }
    }, [response]);

    // set values from search input
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

    // set values from select
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

    let actIam = iam && iam.filter((option) => option.value === props.activeFilter.topics);

    const handleClick = (index) => {
        setActiveComponent(index);
    };

    return (
        <React.Fragment>
            <div className="react-filters-menu">
                <div className="react-filters-container">
                    <form className="r-filter r-filter-search" onSubmit={handleSubmit}>
                        {/* Filtre Recherche */}
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
                    {/* Filtre Thématique */}
                    <div className="r-filter top-filter topics-Filter">
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={menuStyles}
                                    name={"topics"}
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
                    {/* Filtre iam */}
                    <div className="r-filter top-filter iam-Filter">
                        {/* <label>Thématiques</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={menuStyles}
                                    name={"iam"}
                                    className="select-custom-no-border"
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
                    {/* Filtre Facilités */}
                    <div className="r-filter  top-filter facilities-Filter">
                        {/* <label>Facilité</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={menuStyles}
                                    name={"facilities"}
                                    className="select-custom-no-border"
                                    isClearable
                                    onChange={onChangeHandlerSelect}
                                    options={facilitiesFilter && facilitiesFilter}
                                    placeholder={translate({
                                        text: "Facilités",
                                    })}
                                    value={actFaci && actFaci[0]}
                                />
                            )}
                        </Translator>
                    </div>
                </div>
            </div>
            {/* More filter */}

            {/* Affichage dynamique des liens avec divs associées */}
            <div
                id="collapseOne"
                className="accordion-collapse collapse more-filter-container "
                aria-labelledby="headingOne"
                data-bs-parent="#accordionExample"
            >
                <div className="accordion-body">
                    {/* <div className="taxonomy-Filter">
                        {taxonomyData &&
                            taxonomyData.map((donnees, i) => (
                                <TaxonomyFilter
                                    key={i}
                                    {...donnees}
                                    setCat={setCat}
                                    isActive={i === activeComponent}
                                    onClick={() => handleClick(i)}
                                    onChange={onChangeHandlerSelect}
                                    test={i}
                                />
                            ))}
                    </div> */}
                    <div className="r-filter  facilities-Filter">
                        {/* <label>Catégories</label> */}
                        <Translator>
                            {({ translate }) => (
                                <Select
                                    styles={moreFilterStyles}
                                    name={"taxonomy_contact_category_for_filtering"}
                                    className="select-custom-class library-facilities"
                                    isClearable
                                    onChange={onChangeHandlerSelect}
                                    options={taxonomyFilter && taxonomyFilter}
                                    placeholder={translate({
                                        text: "Catégories",
                                    })}
                                    value={actTaxo && actTaxo[0]}
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
