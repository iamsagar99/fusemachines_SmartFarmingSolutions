import React, { useState } from 'react';
import * as Yup from 'yup';
import "./form.css";

const translations = {
  English: {
    air_temp: 'Air Temperature (°C)',
    relative_humidity: 'Relative Humidity (%)',
    nitrogen_added: 'Nitrogen Added (g)',
    water_percent_added: 'Water Percent Added (%)',
    plant_age: 'Plant Age (days)',
    placeholder: {
      air_temp: 'Enter air temperature',
      relative_humidity: 'Enter relative humidity',
      nitrogen_added: 'Enter nitrogen added',
      water_percent_added: 'Enter water percent added',
      plant_age: 'Enter plant age',
    },
    validation: {
      air_temp: {
        min: 'Air temperature must be at least 15°C',
        max: 'Air temperature must be at most 35.32°C',
        required: 'Air temperature is required',
      },
      relative_humidity: {
        min: 'Relative humidity must be at least 4.102%',
        max: 'Relative humidity must be at most 37.81%',
        required: 'Relative humidity is required',
      },
      nitrogen_added: {
        min: 'Nitrogen added must be at least 0',
        max: 'Nitrogen added must be at most 224',
        required: 'Nitrogen added is required',
      },
      water_percent_added: {
        min: 'Water percent added must be at least 0',
        max: 'Water percent added must be at most 100',
        required: 'Water percent added is required',
      },
      plant_age: {
        min: 'Plant age must be at least 0 days',
        max: 'Plant age must be at most 84 days',
        required: 'Plant age is required',
      },
    },
    submit: 'Predict Health',
  },
  Nepali: {
    air_temp: 'हावा तापक्रम (°C)',
    relative_humidity: 'सापेक्ष आर्द्रता (%)',
    nitrogen_added: 'नाइट्रोजन थपियो (g)',
    water_percent_added: 'पानी प्रतिशत थपियो (%)',
    plant_age: 'बिरुवाको उमेर (दिनहरू)',
    placeholder: {
      air_temp: 'हावा तापक्रम प्रविष्ट गर्नुहोस्',
      relative_humidity: 'सापेक्ष आर्द्रता प्रविष्ट गर्नुहोस्',
      nitrogen_added: 'नाइट्रोजन थपियो प्रविष्ट गर्नुहोस्',
      water_percent_added: 'पानी प्रतिशत थपियो प्रविष्ट गर्नुहोस्',
      plant_age: 'बिरुवाको उमेर प्रविष्ट गर्नुहोस्',
    },
    validation: {
      air_temp: {
        min: 'हावा तापक्रम कम्तिमा १५°C हुनुपर्छ',
        max: 'हावा तापक्रम अधिकतम ३५.३२°C हुनुपर्छ',
        required: 'हावा तापक्रम आवश्यक छ',
      },
      relative_humidity: {
        min: 'सापेक्ष आर्द्रता कम्तिमा ४.१०२% हुनुपर्छ',
        max: 'सापेक्ष आर्द्रता अधिकतम ३७.८१% हुनुपर्छ',
        required: 'सापेक्ष आर्द्रता आवश्यक छ',
      },
      nitrogen_added: {
        min: 'नाइट्रोजन थपियो कम्तिमा ० हुनुपर्छ',
        max: 'नाइट्रोजन थपियो अधिकतम २२४ हुनुपर्छ',
        required: 'नाइट्रोजन थपियो आवश्यक छ',
      },
      water_percent_added: {
        min: 'पानी प्रतिशत थपियो कम्तिमा ० हुनुपर्छ',
        max: 'पानी प्रतिशत थपियो अधिकतम १०० हुनुपर्छ',
        required: 'पानी प्रतिशत थपियो आवश्यक छ',
      },
      plant_age: {
        min: 'बिरुवाको उमेर कम्तिमा ० दिन हुनुपर्छ',
        max: 'बिरुवाको उमेर अधिकतम ८४ दिन हुनुपर्छ',
        required: 'बिरुवाको उमेर आवश्यक छ',
      },
    },
    submit: 'स्वास्थ अनुमान गर्नुहोस्',
  },
};

const CropHealthMoniter = ({ onSubmit, language }) => {
  const [formData, setFormData] = useState({
    air_temp: '',
    relative_humidity: '',
    nitrogen_added: '',
    water_percent_added: '',
    plant_age: '',
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const validationSchema = Yup.object().shape({
    air_temp: Yup.number()
      .min(15, translations[language].validation.air_temp.min)
      .max(35.32, translations[language].validation.air_temp.max)
      .required(translations[language].validation.air_temp.required),
    relative_humidity: Yup.number()
      .min(4.102, translations[language].validation.relative_humidity.min)
      .max(37.81, translations[language].validation.relative_humidity.max)
      .required(translations[language].validation.relative_humidity.required),
    nitrogen_added: Yup.number()
      .min(0, translations[language].validation.nitrogen_added.min)
      .max(224, translations[language].validation.nitrogen_added.max)
      .required(translations[language].validation.nitrogen_added.required),
    water_percent_added: Yup.number()
      .min(0, translations[language].validation.water_percent_added.min)
      .max(100, translations[language].validation.water_percent_added.max)
      .required(translations[language].validation.water_percent_added.required),
    plant_age: Yup.number()
      .min(0, translations[language].validation.plant_age.min)
      .max(84, translations[language].validation.plant_age.max)
      .required(translations[language].validation.plant_age.required),
  });

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
      <h2>{language === 'English' ? 'Plant Health Prediction' : 'बिरुवा स्वास्थ अनुमान'}</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>{translations[language].air_temp}</label>
          <input
            type="number"
            name="air_temp"
            placeholder={translations[language].placeholder.air_temp}
            value={formData.air_temp}
            onChange={handleChange}
          />
          {errors.air_temp && <p className="error">{errors.air_temp}</p>}
        </div>
        <div>
          <label>{translations[language].relative_humidity}</label>
          <input
            type="number"
            name="relative_humidity"
            placeholder={translations[language].placeholder.relative_humidity}
            value={formData.relative_humidity}
            onChange={handleChange}
          />
          {errors.relative_humidity && <p className="error">{errors.relative_humidity}</p>}
        </div>
        <div>
          <label>{translations[language].nitrogen_added}</label>
          <input
            type="number"
            name="nitrogen_added"
            placeholder={translations[language].placeholder.nitrogen_added}
            value={formData.nitrogen_added}
            onChange={handleChange}
          />
          {errors.nitrogen_added && <p className="error">{errors.nitrogen_added}</p>}
        </div>
        <div>
          <label>{translations[language].water_percent_added}</label>
          <input
            type="number"
            name="water_percent_added"
            placeholder={translations[language].placeholder.water_percent_added}
            value={formData.water_percent_added}
            onChange={handleChange}
          />
          {errors.water_percent_added && <p className="error">{errors.water_percent_added}</p>}
        </div>
        <div>
          <label>{translations[language].plant_age}</label>
          <input
            type="number"
            name="plant_age"
            placeholder={translations[language].placeholder.plant_age}
            value={formData.plant_age}
            onChange={handleChange}
          />
          {errors.plant_age && <p className="error">{errors.plant_age}</p>}
        </div>
        <button type="submit">{translations[language].submit}</button>
      </form>
    </div>
  );
};

export default CropHealthMoniter;
