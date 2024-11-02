import React, { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import { MenuComponent } from "../../src/components/topnav";
import "./layout.css"


const HomeLayout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [nepLang,setNepLang] = useState(false)

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };
  const [language, setLanguage] = useState(() => {
    let lang = localStorage.getItem("preferredLanguage") || "English";
    console.log("curr-lang",lang)
    return lang;
  });

  useEffect(() => {
    localStorage.setItem("preferredLanguage", language);
    console.log("setlang-",language)
  }, [language]);

  const toggleLanguage = () => {
    setNepLang(!nepLang);
    setLanguage((prevLang) => (prevLang === "English" ? "Nepali" : "English"));
    // console.log(prevLang)
  };
  let saga = "sagar"
  return (
    <>
      <div className="top-bar">
        <div className="left-items">
          <h1 className="text-center" style={{color:'white'}}>Smart Farming Solutions</h1>
        </div>
        <div className="right-items">
          <button onClick={toggleLanguage} className="toggle-button">
            <i
              className={`fas fa-toggle-${
                nepLang ? "on" : "off"
              }`}
            ></i>
            {nepLang ? "NP" : "EN"}
          </button>
        </div>
      </div>

      <div style={{ display: "flex" }}>
        <div
          style={{
            width: isSidebarOpen ? "250px" : "0",
            transition: "width 0.3s",
            overflow: "hidden",
            backgroundColor: "rgb(23,23,23)",
            color: "white",
          }}
        >
          <button onClick={toggleSidebar}>
            {isSidebarOpen ? "Close Sidebar" : "Open Sidebar"}
          </button>
          <MenuComponent language={language}/>
        </div>
        <div
          style={{
            flexGrow: 1,
            padding: "20px",
            backgroundColor: "white",
          }}
        >
          <Outlet context={{ language }}/>
        </div>
      </div>
    </>
  );
};

export default HomeLayout;
