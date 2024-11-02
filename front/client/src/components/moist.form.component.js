import React, { useState } from 'react';
import "./form.css";

const SoilMoistFormComponent = ({ onSubmit, language }) => {
  const [formData, setFormData] = useState({
    Bt_Horizon_30: '',
    Bt_Horizon_deep: '',
    Bulk_Density: '',
    Time_Category: '',
    DOY: '',
    Temperature: '',
    Month: ''
  });

  const [errors, setErrors] = useState({});

  const translations = {
    English: {
      title: "User Input",
      Bt_Horizon_30: "Bt_Horizon_30",
      Bt_Horizon_deep: "Bt_Horizon_deep",
      Bulk_Density: "Bulk Density",
      Time_Category: "Time Category",
      DOY: "Day of Year",
      Temperature: "Temperature",
      Month: "Month",
      submit: "Submit",
      errors: {
        Bt_Horizon_30: "Bt_Horizon_30 must be a numeric value between 0 and 0.025.",
        Bt_Horizon_deep: "Bt_Horizon_deep must be a numeric value between 0 and 0.8.",
        Bulk_Density: "Bulk Density must be a numeric value between 1 and 1.6.",
        Time_Category: "Time Category cannot be empty.",
        DOY: "Day of Year must be a numeric value between 1 and 366.",
        Temperature: "Temperature must be a numeric value between -36 and 36.",
        Month: "Month must be a numeric value between 1 and 12."
      }
    },
    Nepali: {
      // title: "प्रयोगकर्ता इनपुट",
      // Bt_Horizon_30: "बीटी क्षितिज ३०",
      // Bt_Horizon_deep: "बीटी क्षितिज गहिरो",
      // Bulk_Density: "थोक घनत्व",
      // Time_Category: "समय श्रेणी",
      // DOY: "वर्षको दिन",
      // Temperature: "तापमान",
      // Month: "महिना",
      title: "User Input",
      Bt_Horizon_30: "Bt_Horizon_30",
      Bt_Horizon_deep: "Bt_Horizon_deep",
      Bulk_Density: "Bulk Density",
      Time_Category: "Time Category",
      DOY: "Day of Year",
      Temperature: "Temperature",
      Month: "Month",
      submit: "पेश गर्नुहोस्",
      errors: {
        Bt_Horizon_30: "बीटी क्षितिज ३० ० र ०.०२५ बीचको संख्यात्मक मान हुनुपर्छ।",
        Bt_Horizon_deep: "बीटी क्षितिज गहिरो ० र ०.८ बीचको संख्यात्मक मान हुनुपर्छ।",
        Bulk_Density: "थोक घनत्व १ र १.६ बीचको संख्यात्मक मान हुनुपर्छ।",
        Time_Category: "समय श्रेणी खाली हुन सक्दैन।",
        DOY: "वर्षको दिन १ र ३६६ बीचको संख्यात्मक मान हुनुपर्छ।",
        Temperature: "तापमान -३६ र ३६ बीचको संख्यात्मक मान हुनुपर्छ।",
        Month: "महिना १ र १२ बीचको संख्यात्मक मान हुनुपर्छ।"
      }
    }
  };

  const t = translations[language];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const validateForm = () => {
    const newErrors = {};

    if (isNaN(formData.Bt_Horizon_30) || formData.Bt_Horizon_30.trim() === '' || 
        Number(formData.Bt_Horizon_30) < 0 || Number(formData.Bt_Horizon_30) > 0.025) {
      newErrors.Bt_Horizon_30 = t.errors.Bt_Horizon_30;
    }
    
    if (isNaN(formData.Bt_Horizon_deep) || formData.Bt_Horizon_deep.trim() === '' || 
        Number(formData.Bt_Horizon_deep) < 0 || Number(formData.Bt_Horizon_deep) > 0.8) {
      newErrors.Bt_Horizon_deep = t.errors.Bt_Horizon_deep;
    }
    
    if (isNaN(formData.Bulk_Density) || formData.Bulk_Density.trim() === '' || 
        Number(formData.Bulk_Density) < 1 || Number(formData.Bulk_Density) > 1.6) {
      newErrors.Bulk_Density = t.errors.Bulk_Density;
    }
    
    if (formData.Time_Category.trim() === '') {
      newErrors.Time_Category = t.errors.Time_Category;
    }
    
    if (isNaN(formData.DOY) || formData.DOY.trim() === '' || 
        Number(formData.DOY) < 1 || Number(formData.DOY) > 366) {
      newErrors.DOY = t.errors.DOY;
    }
    
    if (isNaN(formData.Temperature) || formData.Temperature.trim() === '' || 
        Number(formData.Temperature) < -36 || Number(formData.Temperature) > 36) {
      newErrors.Temperature = t.errors.Temperature;
    }
    
    if (isNaN(formData.Month) || formData.Month.trim() === '' || 
        Number(formData.Month) < 1 || Number(formData.Month) > 12) {
      newErrors.Month = t.errors.Month;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      console.log(formData);
      onSubmit(formData);
    }
  };

  return (
    <div className="user-input-form-container">
      <h2>{t.title}</h2>
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label>{t[key]}</label>
            <input
              type={key === 'Time_Category' ? 'text' : 'number'}
              name={key}
              placeholder={`Enter ${t[key]}`}
              value={formData[key]}
              onChange={handleChange}
            />
            {errors[key] && <p className="error">{errors[key]}</p>}
          </div>
        ))}
        <button type="submit">{t.submit}</button>
      </form>
    </div>
  );
};

export default SoilMoistFormComponent;