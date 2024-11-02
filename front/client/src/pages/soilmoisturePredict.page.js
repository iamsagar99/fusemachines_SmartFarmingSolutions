import React, { useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import axios from 'axios';
import { useOutletContext } from 'react-router-dom';
import "./moist.css"
const translations = {
  English: {
    title: "Soil Moisture Prediction",
    Bt_Horizon_30: "Bt_Horizon_30 (range: 0 - 0.025)",
    Bt_Horizon_deep: "Bt_Horizon_deep (range: 0 - 0.8)",
    BulkDensity: "Bulk Density (range: 1 - 1.6)",
    Time_Category: "Time Category",
    DOY: "Day of Year (range: 1 - 366)",
    Temperature: "Temperature (range: -36 - 36)",
    Month: "Month (range: 1 - 12)",
    submit: "Submit",
    submitting: "Submitting...",
    loading: "Loading...",
    soilTempPrediction: "The prediction of soil temperature based on your input is:",
    soilMoisturePrediction: "The prediction of soil moisture based on your input is:",
    recommendation: "Recommendation for farmers:",
    selectTimeCategory: "Select a time category",
    timeCategories: [
      'Morning to Midday',
      'Late Morning',
      'Evening to Midnight',
      'Early Morning',
      'Late Afternoon to Early Evening'
    ],
    validationMessages: {
      required: "Required",
      min: "Must be at least ${min}",
      max: "Must be at most ${max}",
      integer: "Must be an integer"
    }
  },
  Nepali: {
    title: "माटोको आर्द्रता अनुमान",
    Bt_Horizon_30: "बीटी क्षितिज ३० (दायरा: ० - ०.०२५)",
    Bt_Horizon_deep: "बीटी क्षितिज गहिरो (दायरा: ० - ०.८)",
    BulkDensity: "थोक घनत्व (दायरा: १ - १.६)",
    Time_Category: "समय श्रेणी",
    DOY: "वर्षको दिन (दायरा: १ - ३६६)",
    Temperature: "तापमान (दायरा: -३६ - ३६)",
    Month: "महिना (दायरा: १ - १२)",
    submit: "पेश गर्नुहोस्",
    submitting: "पेश गर्दै...",
    loading: "लोड हुँदैछ...",
    soilTempPrediction: "तपाईंको इनपुटको आधारमा माटोको तापमानको अनुमान:",
    soilMoisturePrediction: "तपाईंको इनपुटको आधारमा माटोको आर्द्रताको अनुमान:",
    recommendation: "किसानहरूका लागि सिफारिस:",
    selectTimeCategory: "समय श्रेणी चयन गर्नुहोस्",
    timeCategories: [
      'बिहानदेखि मध्याह्नसम्म',
      'ढिलो बिहान',
      'साँझदेखि मध्यरातसम्म',
      'बिहान सबेरै',
      'दिउँसो ढल्कदोदेखि साँझ पर्नु अगाडिसम्म'
    ],
    validationMessages: {
      required: "आवश्यक",
      min: "कम्तिमा ${min} हुनुपर्छ",
      max: "बढीमा ${max} हुनुपर्छ",
      integer: "पूर्णाङ्क हुनुपर्छ"
    }
  }
};

const SoilMoisturePredict = () => {
  const [prediction, setPrediction] = useState({});
  const { language } = useOutletContext();
  const t = translations[language];

  const validationSchema = Yup.object().shape({
    Bt_Horizon_30: Yup.number()
      .min(0, t.validationMessages.min)
      .max(0.025, t.validationMessages.max)
      .required(t.validationMessages.required),
    Bt_Horizon_deep: Yup.number()
      .min(0, t.validationMessages.min)
      .max(0.8, t.validationMessages.max)
      .required(t.validationMessages.required),
    BulkDensity: Yup.number()
      .min(1, t.validationMessages.min)
      .max(1.6, t.validationMessages.max)
      .required(t.validationMessages.required),
    Time_Category: Yup.string().required(t.validationMessages.required),
    DOY: Yup.number()
      .integer(t.validationMessages.integer)
      .min(1, t.validationMessages.min)
      .max(366, t.validationMessages.max)
      .required(t.validationMessages.required),
    Temperature: Yup.number()
      .min(-36, t.validationMessages.min)
      .max(36, t.validationMessages.max)
      .required(t.validationMessages.required),
    Month: Yup.number()
      .integer(t.validationMessages.integer)
      .min(1, t.validationMessages.min)
      .max(12, t.validationMessages.max)
      .required(t.validationMessages.required),
  });

  const initialValues = {
    Bt_Horizon_30: '',
    Bt_Horizon_deep: '',
    BulkDensity: '',
    Time_Category: '',
    DOY: '',
    Temperature: '',
    Month: '',
  };

  const getRecommendation = (vw_value) => {
    if (vw_value < 0.2) {
      return language === 'English' 
        ? "Too dry. Needs watering ASAP."
        : "धेरै सुक्खा छ। तुरुन्तै सिंचाइको आवश्यकता छ।";
    } else if (0.2 <= vw_value && vw_value < 0.4) {
      return language === 'English'
        ? "Schedule water irrigation soon."
        : "चाँडै सिंचाइको योजना बनाउनुहोस्।";
    } else if (0.4 <= vw_value && vw_value < 0.6) {
      return language === 'English'
        ? "Optimal moisture level. No need of watering."
        : "माटोको आद्रता स्तर उत्तम छ।";
    } else if (0.6 <= vw_value && vw_value < 0.8) {
      return language === 'English'
        ? "Wet enough. Will be optimal in a few days."
        : "पर्याप्त भिजेको छ। केही दिनमा उत्तम हुनेछ।";
    } else {
      return language === 'English'
        ? "Excess moisture. No watering needed for a few days."
        : "अधिक आद्रता छ। केही दिनसम्म पानी हाल्न आवश्यक छैन।";
    }
  };

  // const handleSubmit = async (values, { setSubmitting }) => {
  //   try {
  //     console.log(values);
  //     const response = await axios.post('http://127.0.0.1:5001/predict-soil-moisture', values);
  //     console.log('Prediction response:', response.data);
  //     setPrediction(response.data);
  //   } catch (error) {
  //     console.error('There was an error making the request:', error);
  //   } finally {
  //     setSubmitting(false);
  //   }
  // };
  const handleSubmit = async (values, { setSubmitting }) => {
    // Mapping from Nepali to English Time Categories
    const timeCategoryMapping = {
      'बिहानदेखि मध्याह्नसम्म': 'Morning to Midday',
      'ढिलो बिहान': 'Late Morning',
      'साँझदेखि मध्यरातसम्म': 'Evening to Midnight',
      'बिहान सबेरै': 'Early Morning',
      'दिउँसो ढल्कदोदेखि साँझ पर्नु अगाडिसम्म': 'Late Afternoon to Early Evening'
    };
  
    // Map the Nepali Time_Category to English before submission
    if (language === 'Nepali') {
      values.Time_Category = timeCategoryMapping[values.Time_Category] || values.Time_Category;
    }
  
    try {
      console.log(values);
      const response = await axios.post('http://127.0.0.1:5001/predict-soil-moisture', values);
      console.log('Prediction response:', response.data);
      setPrediction(response.data);
    } catch (error) {
      console.error('There was an error making the request:', error);
    } finally {
      setSubmitting(false);
    }
  };
  

  return (
    <div className="container">
      <div className="form-container">
        <h2 className="title">{t.title}</h2>
        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form className="form">
              {Object.keys(initialValues).map((fieldName) => (
                <div key={fieldName} className="form-field">
                  <label htmlFor={fieldName} className="form-label">
                    {t[fieldName]}
                  </label>
                  {fieldName === 'Time_Category' ? (
                    <Field as="select" name={fieldName} id={fieldName} className="form-select">
                      <option value="">{t.selectTimeCategory}</option>
                      {t.timeCategories.map((option) => (
                        <option key={option} value={option}>{option}</option>
                      ))}
                    </Field>
                  ) : (
                    <Field type="number" name={fieldName} id={fieldName} className="form-input" />
                  )}
                  <ErrorMessage name={fieldName} component="div" className="error-message" />
                </div>
              ))}
              <button type="submit" disabled={isSubmitting} className="submit-button">
                {isSubmitting ? t.submitting : t.submit}
              </button>
            </Form>
          )}
        </Formik>
      </div>

      <div className="prediction-container">
        {!prediction && <h3 className="loading">{t.loading}</h3>}
        {prediction && prediction.predicted_T_value && (
          <p className="prediction">
            {t.soilTempPrediction} <strong>{prediction.predicted_T_value}</strong>
          </p>
        )}
        {prediction && prediction.predicted_VW_value && (
          <>
            <p className="prediction">
              {t.soilMoisturePrediction} <strong>{prediction.predicted_VW_value}</strong>
            </p>
            <p className="recommendation">
              {t.recommendation} <strong>{getRecommendation(prediction.predicted_VW_value)}</strong>
            </p>
          </>
        )}
      </div>
    </div>
  );
};

export default SoilMoisturePredict;