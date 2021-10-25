import React, { useEffect, useCallback, useState } from "react";
import Select from 'react-select'
import {
    BrowserRouter as Router,
    Link,
    useHistory
} from "react-router-dom";
import useAxios from '../../../hooks/useAxios';
import useFilterQuery from "../../../hooks/useFilterQuery";


function Filters(props) {
    let history = useHistory();
    const queryString = require('query-string');
    const parsed = queryString.parse(useFilterQuery().toString());
    const [inputValues, setInputValues] = useState(parsed);
    const [topicsFilter, setTopicsFilter] = useState(null);
    const [taxonomyFilter, setTaxonomyFilter] = useState(null);
    const [facilitiesFilter, setFacilitiesFilter] = useState(null);
    const { response, error, isLoading } = useAxios({
        method: 'get',
        url: '',
        baseURL: props.url,
        headers: {
            'Accept': 'application/json',
        },
        params: inputValues,

    });

    useEffect(() => {
        if (response !== null) {
            const optionsTopics = response.topics && response.topics.map(d => ({
                "value": d.token,
                "label": d.title
            }))
            const optionsTaxonomy = response.taxonomy_contact_category && response.taxonomy_contact_category.map(d => ({
                "value": d.token,
                "label": d.title
            }))
            const optionsFacilities = response.facilities && response.facilities.map(d => ({
                "value": d.token,
                "label": d.title
            }))
            setTopicsFilter(optionsTopics);
            setTaxonomyFilter(optionsTaxonomy);
            setFacilitiesFilter(optionsFacilities);
        }
    }, [response]);


    const onChangeHandler = useCallback(
        ({ target: { name, value } }) => setInputValues(state => ({ ...state, [name]: value }), [])
    );
    const onChangeHandlerSelect = useCallback(
        (value, action) => {
            const inputName = action.name
            if (value) {
                setInputValues(state => ({ ...state, [inputName]: value.value }), [])

            } else {
                setInputValues(prevState => {
                    const state = { ...prevState }
                    const { [inputName]: remove, ...rest } = state;
                    return rest
                })
            }

        }
    );

    useEffect(() => {
        history.push({
            pathname: '',
            search: queryString.stringify(inputValues),
        })

        props.onChange(inputValues);
    }, [inputValues]);

    function handleSubmit(e) {
        e.preventDefault();
        props.onChange(inputValues);
    }

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
            <Link to="/?facilities=defibrillator">Netflix</Link>

            <div className="r-filter topics-Filter">
                <span>Thématiques</span>
                <Select
                    name={"topics"}
                    className="select-custom-class library-topics"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={topicsFilter && topicsFilter}
                    placeholder={'Toutes'}
                />
            </div>
            <div className="r-filter  facilities-Filter">
                <span>Catégories</span>
                <Select
                    name={"taxonomy_contact_category"}
                    className="select-custom-class library-facilities"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={taxonomyFilter && taxonomyFilter}
                    placeholder={'Toutes'}
                />
            </div>
            <div className="r-filter  facilities-Filter">
                <span>Facilité</span>
                <Select
                    name={"facilities"}
                    className="select-custom-class library-facilities"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={facilitiesFilter && facilitiesFilter}
                    placeholder={'Toutes'}
                />
            </div>



        </React.Fragment>
    );
}

export default Filters;