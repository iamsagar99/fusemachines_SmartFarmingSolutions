import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './pathogenPage.css'; // Import CSS for styling
import { useOutletContext } from 'react-router-dom';

const PathogenPage = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const {language} = useOutletContext(); 
  console.log("sarrrga",language)
    
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedFile(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setPreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!selectedFile) {
            setError(language === 'English' ? 'Please select a file first!' : 'कृपया पहिले फाइल छान्नुहोस्!');
            return;
        }
//अनुमानित
        setError('');
        setPrediction(null);
        setLoading(true);

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await axios.post('http://127.0.0.1:5000/predict-pathogen', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            setLoading(false);
            if (response.data && response.data.prediction) {
                if (response.data.prediction.confidence > 0.99) {
                    setPrediction(response.data.prediction);
                } else {
                    setPrediction({ 
                        predicted_class: language === 'English' 
                            ? "Failed to get prediction. Please provide a clear leaf image." 
                            : "अनुमान प्राप्त गर्न असफल। कृपया स्पष्ट पातको तस्वीर प्रदान गर्नुहोस्।"
                    });
                }
            } else {
                setError(language === 'English' 
                    ? 'Failed to get prediction from the server.' 
                    : 'सर्वरबाट अनुमान प्राप्त गर्न असफल।');
            }
        } catch (err) {
            setLoading(false);
            setError(language === 'English' 
                ? 'Error occurred while uploading the image or receiving prediction.' 
                : 'तस्वीर अपलोड गर्दा वा अनुमान प्राप्त गर्दा त्रुटि भयो।');
        }
    };

    return (
        <div className='pathogen-page'>

            <div className='page-container'>
                <div className='form-column'>
                    <form onSubmit={handleSubmit}>
                        <h3>
                            {language === 'English' 
                                ? 'Please upload an image of the plant leaf' 
                                : 'कृपया बिरुवाको पातको तस्वीर अपलोड गर्नुहोस्'}
                        </h3>
                        {preview && (
                            <div>
                                <img src={preview} alt="Preview" style={{ width: '300px', marginTop: '10px' }} />
                            </div>
                        )}
                        <input type="file" accept="image/*" onChange={handleFileChange} />
                        <br />
                        <button className='mb-5' type="submit" disabled={loading}>
                            {loading 
                                ? (language === 'English' ? 'Predicting...' : 'अनुमान गर्दै...') 
                                : (language === 'English' ? 'Upload & Predict' : 'अपलोड र अनुमान गर्नुहोस्')}
                        </button>
                    </form>
                    {error && <p style={{ color: 'red' }}>{error}</p>}
                </div>
                
                {prediction && (
                    <div className='result-column'>
                        <h2>{language === 'English' ? 'Prediction Results' : 'अनुमान परिणामहरू'}</h2>
                        <h3>
                            {language === 'English' 
                                ? `This image is classified as: ` 
                                : `यो तस्वीरलाई यसरी वर्गीकृत गरिएको छ: `}
                            <strong>{prediction.predicted_class}</strong>
                        </h3>
                        <h4>
                            {language === 'English' ? 'Confidence: ' : 'विश्वास: '}
                            {prediction.confidence.toFixed(2)}
                        </h4>
                        
                        <div className='solutions'>
                            <h3>{language === 'English' ? 'Solutions:' : 'समाधानहरू:'}</h3>
                            <div>
                                <h4>{language === 'English' ? 'Chemical Alternatives:' : 'रासायनिक विकल्पहरू:'}</h4>
                                <ul>
                                    {prediction.solutions[language]["Chemical Alternatives"].map((solution, index) => (
                                        <li key={index}>{solution}</li>
                                    ))}
                                </ul>
                                <h4>{language === 'English' ? 'Practices:' : 'अभ्यासहरू:'}</h4>
                                <ul>
                                    {prediction.solutions[language].Practices.map((practice, index) => (
                                        <li key={index}>{practice}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PathogenPage;