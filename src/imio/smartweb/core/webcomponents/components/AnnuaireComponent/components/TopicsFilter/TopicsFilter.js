import React, { Component } from 'react'
import Select from 'react-select'
import { useEffect,useState } from "react";



const TopicsFilter = (props) => {
    const [topicsArray, setTopicsArray] = useState([]);

    useEffect(() => { // probably some shit for an array 
        if (props.contactArray.length > 0) {
          const arr = [];
          props.contactArray.map((item, i) => {
            if (item.topics != null) {
              arr.push(item.topics[0].title);
            }
          });
          const uniqueSet = new Set(arr);
          const backToArray = [...uniqueSet];
          const options = backToArray.map(d => ({
            "value": d,
            "label": d
          }))
          setTopicsArray(options)
        }
      }, [props.contactArray]);

    function handleChange(event) {
        props.onChange(event);
      }
    return (
        <div className="r-filter topics-Filter">
            <span>Thématiques</span>
            <Select
                className="select-custom-class library-topics"
                isClearable
                onChange={handleChange}
                // onInputChange={this.handleInputChange}
                options={topicsArray}
                placeholder={'Toutes'}
            /> 
        </div>
    )
}


export default TopicsFilter