import React, { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";
import { useOutletContext } from 'react-router-dom';

import "./nav.css";

export const MenuComponent = ({language}) => {

  // const saga = useOutletContext(); 
  // console.log(saga)

  // const langua ge = nepLang;
  // const [language, setLanguage] = useState(() => {
  //   return localStorage.getItem('preferredLanguage') || 'English';
  // });

  // useEffect(() => {
  //   localStorage.setItem('preferredLanguage', language);
  // }, [language]);

  // const toggleLanguage = () => {
  //   setLanguage(prevLang => prevLang === 'English' ? 'Nepali' : 'English');
  // };

  return (
    <nav className="sidebar">
      <div className="sidebar-logo">
      </div>
      <div className="sidebar-links">
        <NavLink to="/" className="sidebar-link">
          {language === 'English' ? 'Crop Recommendation' : 'बाली सिफारिस'}
        </NavLink>
        <NavLink to="/crop-health-monitor" className="sidebar-link">
          {language === 'English' ? 'Crop Health Monitoring' : 'बाली स्वास्थ्य अनुगमन'}
        </NavLink>
        <NavLink to="/soil-moisture-prediction" className="sidebar-link">
          {language === 'English' ? 'Soil Moisture Prediction' : 'माटो नमी पूर्वानुमान'}
        </NavLink>
        <NavLink to="/pathogen-classifier" className="sidebar-link">
          {language === 'English' ? 'Pathogen Classifier' : 'रोगजनक वर्गीकरण'}
        </NavLink>
      </div>
      <div className="profile-dropdown">
        <div className="dropdown-content">
          <a href="/login">{language === 'English' ? 'Logout' : 'लग आउट'}</a>
        </div>
      </div>
      {/* <div className="language-toggle">
        <button onClick={toggleLanguage} className="toggle-button">
          <i className={`fas fa-toggle-${language === 'English' ? 'on' : 'off'}`}></i>
          {language === 'English' ? 'NP' : 'EN'}
        </button>
      </div> */}
    </nav>
  );
};