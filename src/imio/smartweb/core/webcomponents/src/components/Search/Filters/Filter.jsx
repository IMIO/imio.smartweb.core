import React, { useEffect, useCallback, useState } from "react";
import Select from 'react-select';
import {useHistory } from "react-router-dom";
import useAxios from '../../../hooks/useAxios';
import axios from "axios";
function Filters(props) {
    let history = useHistory();
    const queryString = require("query-string");

    const [inputValues, setInputValues] = useState(props.activeFilter);
    const [searchValues, setSearchValues] = useState({});
    const [topicsFilter, setTopicsFilter] = useState(null);
    const [iamFilter, setIamFilter] = useState(null);
    // const {response, topicsError, topicsIsLoading } = useAxios({
    //     method: 'get',
    //     url: "",
    //     baseURL: props.url+'/@vocabularies/imio.smartweb.vocabulary.Topics',
    //     headers: {
    //         Accept: "application/json",
    //         Authorization: "Basic YWRtaW46YWRtaW4=",
    //     },
    // });


    // useEffect(() => {
    //     if (response !== null) {
    //         const optionsTopics = response.items.map(d => ({
    //             value: d.token,
    //             label: d.title
    //         }))
    //         setTopicsFilter(optionsTopics);
    //     }
    // }, [response]);





    const apiCall=()=>{
        const requestOne = axios.request({
            method: 'get',
            url: "",
            baseURL: props.url+'/@vocabularies/imio.smartweb.vocabulary.Topics',
            headers: {
                Accept: "application/json",
                Authorization: "Basic YWRtaW46YWRtaW4=",
        }})

        const requestTwo = axios.request({
            method: 'get',
            url: "",
            baseURL: props.url+'/@vocabularies/imio.smartweb.vocabulary.IAm',
            headers: {
                Accept: "application/json",
                Authorization: "Basic YWRtaW46YWRtaW4=",
        }})

        axios
        .all([requestOne, requestTwo])
        .then(
            axios.spread((...responses) => {
            const responseOne = responses[0];
            const responseTwo = responses[1];
            if (responseOne !== null) {
                const optionsTopics = responseOne.data.items.map(d => ({
                    value: d.token,
                    label: d.title
                }))
                setTopicsFilter(optionsTopics);
            }
            if (responseTwo !== null) {
                const optionsIam = responseTwo.data.items.map(d => ({
                    value: d.token,
                    label: d.title
                }))
                setIamFilter(optionsIam);
            }
            })
        )
        .catch(errors => {
            // react on errors.
            console.error('errors');
        });
    }
    
    useEffect(()=>{
        apiCall()
    },[])


    const HandlerText = (e) =>{
        setSearchValues({'SearchableText': e.target.value})
        if (e.target.value.length > 2) {
            setInputValues(state => ({ ...state, 'SearchableText':e.target.value}), [])
        } else {
            setInputValues(prevState => {
                const state = { ...prevState }
                const { 'SearchableText': remove, ...rest } = state;
                return rest
            })
        }
    }
    const handleSubmit = (e) => {
        e.preventDefault();
        if (searchValues.SearchableText) {
            setInputValues(state => ({ ...state, 'SearchableText':searchValues.SearchableText }), [])
        } else {
            setInputValues(prevState => {
                const state = { ...prevState }
                const { 'SearchableText': remove, ...rest } = state;
                return rest
            })
        }
    }
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
            pathname: "",
            search: queryString.stringify(inputValues),
        });
        props.onChange(inputValues);
    }, [inputValues]);

    const customStyles = {
        control: styles => ({ 
            ...styles,
            backgroundColor: 'white',
            borderRadius:'0',
            height:'50px',
        }),
        placeholder: styles =>({
            ...styles,
            color: '000',
            fontWeight:'bold',
            fontSize:'12px',
            textTransform:'uppercase',
            letterSpacing:'1.2px'
        }),
        option: (styles, { data, isDisabled, isFocused, isSelected }) => {
          return {
            ...styles,
          };
        },
      };

    return (
        <React.Fragment>
            <div className="col-md-6 r-search search-bar-filter">
                <form onSubmit={handleSubmit}>
                    <label>
                        <input
                            name="SearchableText" type="text"
                            onChange={HandlerText}
                            value={searchValues.SearchableText}
                            placeholder={'Recherche'}

                        />
                    </label>
                    <button type="submit">Chercher</button>
                </form>
            </div>
            <div className="col-md-2 r-search search-select-filter">
                <Select
                    styles={customStyles}
                    name={"iam"}
                    className="r-search-select"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={iamFilter && iamFilter}
                    placeholder={'Je suis'}
                />
            </div> 
            <div className="col-md-2 r-search search-select-filter">
                <Select
                    styles={customStyles}
                    name={"topics"}
                    className="r-search-select"
                    isClearable
                    onChange={onChangeHandlerSelect}
                    options={topicsFilter && topicsFilter}
                    placeholder={'Thématiques'}
                />
            </div>
        </React.Fragment>
    );
}

export default Filters;