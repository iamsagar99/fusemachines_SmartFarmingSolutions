import React, { useState } from 'react';
import axios from 'axios';
import { useOutletContext } from 'react-router-dom';
import CropForm from '../components/form.component.js';
import './croppage.css'; // Make sure to create this CSS file

const translations = {
  English: {
    suitableCropMessage: " is the crop is suitable to cultivate in this environment.",
    loading: "Loading...",
    error: "There was an error making the request."
  },
  Nepali: {
    suitableCropMessage: "बालीलाई यो वातावरणमा खेती गर्न उपयुक्त छ।",
    loading: "लोड हुँदैछ...",
    error: "अनुरोध गर्दा त्रुटि भयो।"
  }
};

const CropPage = () => {
  const [crop, setCrop] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { language } = useOutletContext();
  const t = translations[language];

  const handleFormSubmit = (data) => {
    setLoading(true);
    setError(null);

    axios.post('http://127.0.0.1:5001/predict-crop', data)
      .then((response) => {
        setCrop(response.data.prediction);
        setLoading(false);
      })
      .catch((error) => {
        setError(t.error);
        setLoading(false);
      });
  };

  return (
    <div className={`crop-prediction-container ${crop ? 'has-result' : ''}`}>
      <div className="crop-form">
        <CropForm onSubmit={handleFormSubmit} language={language} />
      </div>
      <div className="crop-result">
        {loading && <p>{t.loading}</p>}
        {error && <p className="error">{error}</p>}
        {crop && (
          <>
            <p><strong>{crop.crop}</strong> {t.suitableCropMessage}</p>
            {/* Conditional rendering for crop information based on the language */}
            <p>{language === 'Nepali' ? crop.info : crop.info_en}</p>
          </>
        )}
      </div>
    </div>
  );
};

export default CropPage;
