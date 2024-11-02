import React, { useState } from 'react';
import * as Yup from 'yup';
import './form.css';

const translations = {
  English: {
    title: "Crop Prediction",
    nitrogen: "Nitrogen",
    phosphorous: "Phosphorous",
    temperature: "Temperature",
    humidity: "Humidity",
    ph: "pH",
    rainfall: "Rainfall",
    placeholder: {
      nitrogen: "Enter Nitrogen",
      phosphorous: "Enter Phosphorous",
      temperature: "Enter Temperature",
      humidity: "Enter Humidity",
      ph: "Enter pH",
      rainfall: "Enter Rainfall",
    },
    submit: "Predict Crop",
    validation: {
      nitrogenMin: "Nitrogen must be at least 0",
      nitrogenMax: "Nitrogen must be at most 140",
      nitrogenRequired: "Nitrogen is required",
      phosphorousMin: "Phosphorous must be at least 0",
      phosphorousMax: "Phosphorous must be at most 145",
      phosphorousRequired: "Phosphorous is required",
      temperatureMin: "Temperature must be at least 1",
      temperatureMax: "Temperature must be at most 43.68",
      temperatureRequired: "Temperature is required",
      humidityMin: "Humidity must be at least 1",
      humidityMax: "Humidity must be at most 99.98",
      humidityRequired: "Humidity is required",
      phMin: "pH must be at least 0.1",
      phMax: "pH must be at most 14",
      phRequired: "pH is required",
      rainfallMin: "Rainfall must be at least 0",
      rainfallMax: "Rainfall must be at most 298.56",
      rainfallRequired: "Rainfall is required",
    },
  },
  Nepali: {
    title: "उपयुक्त बाली अनुमान",
    nitrogen: "नाइट्रोजन",
    phosphorous: "फस्फोरस",
    temperature: "तापक्रम",
    humidity: "आर्द्रता",
    ph: "पि.एच.",
    rainfall: "वर्षा",
    placeholder: {
      nitrogen: "नाइट्रोजन प्रविष्ट गर्नुहोस्",
      phosphorous: "फस्फोरस प्रविष्ट गर्नुहोस्",
      temperature: "तापक्रम प्रविष्ट गर्नुहोस्",
      humidity: "आर्द्रता प्रविष्ट गर्नुहोस्",
      ph: "पि.एच. प्रविष्ट गर्नुहोस्",
      rainfall: "वर्षा प्रविष्ट गर्नुहोस्",
    },
    submit: "उपयुक्त बाली अनुमान गर्नुहोस्",
    validation: {
      nitrogenMin: "नाइट्रोजन कम्तिमा 0 हुनु पर्छ",
      nitrogenMax: "नाइट्रोजन अधिकतम 140 हुनु पर्छ",
      nitrogenRequired: "नाइट्रोजन आवश्यक छ",
      phosphorousMin: "फस्फोरस कम्तिमा 0 हुनु पर्छ",
      phosphorousMax: "फस्फोरस अधिकतम 145 हुनु पर्छ",
      phosphorousRequired: "फस्फोरस आवश्यक छ",
      temperatureMin: "तापक्रम कम्तिमा 1 हुनु पर्छ",
      temperatureMax: "तापक्रम अधिकतम 43.68 हुनु पर्छ",
      temperatureRequired: "तापक्रम आवश्यक छ",
      humidityMin: "आर्द्रता कम्तिमा 1 हुनु पर्छ",
      humidityMax: "आर्द्रता अधिकतम 99.98 हुनु पर्छ",
      humidityRequired: "आर्द्रता आवश्यक छ",
      phMin: "पि.एच. कम्तिमा 0.1 हुनु पर्छ",
      phMax: "पि.एच. अधिकतम 14 हुनु पर्छ",
      phRequired: "पि.एच. आवश्यक छ",
      rainfallMin: "वर्षा कम्तिमा 0 हुनु पर्छ",
      rainfallMax: "वर्षा अधिकतम 298.56 हुनु पर्छ",
      rainfallRequired: "वर्षा आवश्यक छ",
    },
  },
};

const CropForm = ({ onSubmit, language }) => {
  const [formData, setFormData] = useState({
    N: '',
    P: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });

  const [errors, setErrors] = useState({});
  const t = translations[language]; // Select the appropriate translations based on language

  // Validation schema using translated messages
  const validationSchema = Yup.object().shape({
    N: Yup.number()
      .min(0, t.validation.nitrogenMin)
      .max(140, t.validation.nitrogenMax)
      .required(t.validation.nitrogenRequired),
    P: Yup.number()
      .min(0, t.validation.phosphorousMin)
      .max(145, t.validation.phosphorousMax)
      .required(t.validation.phosphorousRequired),
    temperature: Yup.number()
      .min(1, t.validation.temperatureMin)
      .max(43.68, t.validation.temperatureMax)
      .required(t.validation.temperatureRequired),
    humidity: Yup.number()
      .min(1, t.validation.humidityMin)
      .max(99.98, t.validation.humidityMax)
      .required(t.validation.humidityRequired),
    ph: Yup.number()
      .min(0.1, t.validation.phMin)
      .max(14, t.validation.phMax)
      .required(t.validation.phRequired),
    rainfall: Yup.number()
      .min(0, t.validation.rainfallMin)
      .max(298.56, t.validation.rainfallMax)
      .required(t.validation.rainfallRequired),
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const validateForm = async () => {
    try {
      await validationSchema.validate(formData, { abortEarly: false });
      setErrors({});
      return true;
    } catch (validationErrors) {
      const newErrors = {};
      validationErrors.inner.forEach((error) => {
        newErrors[error.path] = error.message;
      });
      setErrors(newErrors);
      return false;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const isValid = await validateForm();
    if (isValid) {
      onSubmit(formData);
    }
  };

  return (
    <div className="crop-form-container">
      <h2>{t.title}</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>{t.nitrogen}</label>
          <input
            type="number"
            name="N"
            placeholder={t.placeholder.nitrogen}
            value={formData.N}
            onChange={handleChange}
          />
          {errors.N && <p className="error">{errors.N}</p>}
        </div>
        <div>
          <label>{t.phosphorous}</label>
          <input
            type="number"
            name="P"
            placeholder={t.placeholder.phosphorous}
            value={formData.P}
            onChange={handleChange}
          />
          {errors.P && <p className="error">{errors.P}</p>}
        </div>
        <div>
          <label>{t.temperature}</label>
          <input
            type="number"
            name="temperature"
            placeholder={t.placeholder.temperature}
            value={formData.temperature}
            onChange={handleChange}
          />
          {errors.temperature && <p className="error">{errors.temperature}</p>}
        </div>
        <div>
          <label>{t.humidity}</label>
          <input
            type="number"
            name="humidity"
            placeholder={t.placeholder.humidity}
            value={formData.humidity}
            onChange={handleChange}
          />
          {errors.humidity && <p className="error">{errors.humidity}</p>}
        </div>
        <div>
          <label>{t.ph}</label>
          <input
            type="number"
            name="ph"
            placeholder={t.placeholder.ph}
            value={formData.ph}
            onChange={handleChange}
          />
          {errors.ph && <p className="error">{errors.ph}</p>}
        </div>
        <div>
          <label>{t.rainfall}</label>
          <input
            type="number"
            name="rainfall"
            placeholder={t.placeholder.rainfall}
            value={formData.rainfall}
            onChange={handleChange}
          />
          {errors.rainfall && <p className="error">{errors.rainfall}</p>}
        </div>
        <button type="submit">{t.submit}</button>
      </form>
    </div>
  );
};

export default CropForm;
