import React from 'react';
import axios from 'axios';
import { useOutletContext } from 'react-router-dom';
import CropHealthMoniter from '../components/health.component.js'; // Adjust the import path if necessary
import './plant.css'; // Import CSS for styling

const translations = {
  English: {
    title: "Prediction Results",
    predictedValue: "Predicted Value:",
    loading: "Loading...",
    error: "There was an error making the request."
  },
  Nepali: {
    title: "भविष्यवाणी परिणामहरू",
    predictedValue: "अनुमानित मान:",
    loading: "लोड हुँदैछ...",
    error: "अनुरोध गर्दा त्रुटि भयो।"
  }
};

const PlantPage = () => {
  const [plant, setPlant] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const { language } = useOutletContext();
  const t = translations[language];

  const handleFormSubmit = (data) => {
    console.log('Form data:', data);
    setLoading(true);
    setError(null);

    axios
      .post('http://127.0.0.1:5001/crop-health-moniter', data) 
      .then((response) => {
        console.log('Prediction response:', response.data);
        setPlant(response.data.prediction);
        setLoading(false);
      })
      .catch((error) => {
        console.error('There was an error making the request:', error);
        setError(t.error);
        setLoading(false);
      });
  };

  return (
    <div className='p-2'>
      <div className='plant-page-container'>
        <div className='form-column'>
          <CropHealthMoniter onSubmit={handleFormSubmit} language={language} />
        </div>
        {loading && <p className='text-center'>{t.loading}</p>}
        {error && <p className='text-center text-red-500'>{error}</p>}
        {plant && (
          <div className='result-column'>
            <h4 className='text-center'>{t.title}</h4>
            {Object.keys(plant).map((key) => (
              <div key={key} className='result-item'>
                <h5>{key}</h5>
                <p><strong>{t.predictedValue}</strong> {plant[key].value.toFixed(2)}</p>
                <p>{language === 'English' ? plant[key].category : plant[key].np}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PlantPage;