import React, { useEffect, useCallback, useState } from "react";
import Select from 'react-select';
import useAxios from '../../../hooks/useAxios';

function Filters(props) {
    const [inputValues, setInputValues] = useState({});
    const [searchValues, setSearchValues] = useState({});
    const [topicsFilter, setTopicsFilter] = useState(null);
    const [iamFilter, setIamFilter] = useState(null);
    const {response, topicsError, topicsIsLoading } = useAxios({
        method: 'get',
        url: "",
        baseURL: props.url+'/@vocabularies/imio.smartweb.vocabulary.Topics',
        headers: {
            'Accept': 'application/json',
            'Authorization': 'Basic YWRtaW46c2VjcmV0',
        },
        

    });

    useEffect(() => {
        if (response !== null) {
            const optionsTopics = response.items.map(d => ({
                "value": d.token,
                "label": d.title
            }))
            setTopicsFilter(optionsTopics);
        }
    }, [response]);

    const HandlerText = (e) =>{
        setSearchValues({'SearchableText': e.target.value})
        if (e.target.value) {
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

      console.log(inputValues)
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