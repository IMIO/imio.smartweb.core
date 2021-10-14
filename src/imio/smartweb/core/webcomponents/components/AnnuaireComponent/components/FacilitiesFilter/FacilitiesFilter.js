import React, { Component } from 'react'
import Select from 'react-select'
import { useEffect,useState } from "react";



const FacilitiesFilter = (props) => {
    const [facilitiesArray, setFacilitiesArray] = useState([]);

    useEffect(() => { // probably some shit for an array 
        if (props.contactArray.length > 0) {
          const arr = [];
          props.contactArray.map((item, i) => {
            if (item.facilities != null) {
              arr.push(item.facilities[0].title);
            }
          });
          const uniqueSet = new Set(arr);
          const backToArray = [...uniqueSet];
          const options = backToArray.map(d => ({
            "value": d,
            "label": d
          }))
          setFacilitiesArray(options)
        }
      }, [props.contactArray]);

    function handleChange(event) {
        props.onChange(event);
      }
    return (
        <div className="r-filter facilities-Filter">
            <span>Facilité</span>
            <Select
            className="select-custom-class library-facilities"
            isClearable
            onChange={handleChange}
            // onInputChange={this.handleInputChange}
            options={facilitiesArray}
            placeholder={'Toutes'}
        /> 
      </div>
    )
}


export default FacilitiesFilter