import ContactCard from "../ContactCard/ContactCard";
import {Link} from 'react-router-dom';
import React from 'react';
const ContactList = ({contactArray,onChange, onHover}) => {
  
    function handleClick(event) {
      onChange(event);
    }
    function handleHover(event) {
      onHover(event);
    }
  return (
      <ul className="r-result-list annuaire-result-list">
        {contactArray.map((contactItem,i)=>(
            <li className="r-list-item-group" 
                onMouseEnter={() => handleHover(contactItem.UID)} 
                onMouseLeave={() => handleHover(null)} 
                onClick={() => handleClick(contactItem.UID)} >
            {/* <Link className="r-list-item-link" style={{ textDecoration: 'none' }} to={{
              pathname: `/${contactItem.UID}`,
              state : {
                idItem : contactItem.UID
              }
              }}
            >
            </Link> */}
              <ContactCard contactItem={contactItem} key={contactItem.created} />
            </li>
          ))
        }   
      </ul>
  );
};
export default ContactList;