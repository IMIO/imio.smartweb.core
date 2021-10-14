import React, { Component } from 'react'
import Select from 'react-select'
import { useEffect, useState } from "react";


const CategoriesFilter = (props) => {
  const [categoriesArray, setCategoriesArray] = useState([]);


  useEffect(() => { // probably some shit for an array 
    if (props.contactArray.length > 0) {
      const arr = [];
      props.contactArray.map((item, i) => {
        if (item.taxonomy_contact_category != null) {
          arr.push(item.taxonomy_contact_category[0].title);
        }
      });
      const uniqueSet = new Set(arr);
      const backToArray = [...uniqueSet];
      const options = backToArray.map(d => ({
        "value": d,
        "label": d
      }))
      setCategoriesArray(options)
    }
  }, [props.contactArray]);

  function handleChange(event) {
    props.onChange(event);
  }

  const customStyles = {
    control: () => ({
      // none of react-select's styles are passed to <Control />
      width: 200,
    }),
  }
  return (
    <div className="r-filter categories-Filter">
      <span>Catégories</span>
      <Select
        className="select-custom-class library-categories"
        isClearable
        onChange={handleChange}
        // onInputChange={this.handleInputChange}
        options={categoriesArray}
        placeholder={'Toutes'}
      />
    </div>
  )
}


export default CategoriesFilter