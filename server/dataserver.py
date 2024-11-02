from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
import os
from werkzeug.utils import secure_filename

# # Add the path where crop_recommendation.py and soil_moisture_predict.py are located
# path = '/Users/sagarpoudel/Desktop/FuseMachines/project/crop-prediction/crop-prediction/final/server'
# sys.path.append(f'{path}/crop')
# sys.path.append(f'{path}/soil_moisture')
# sys.path.append(f'{path}/crop_health')

sys.path.append("crop")
sys.path.append("crop_health")
sys.path.append("soil_moisture")
# sys.path.append('/Users/sagarpoudel/Desktop/FuseMachines/project/crop-prediction/crop-prediction/final/server/pathogen')

# Import the functions
from crop_recommendation import recommend_crop
from soil_moisture_predict import predict_soil_moisture
from crop_health_moniter import categorize_health


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set upload folder
UPLOAD_FOLDER = 'uploads'  # Change this to your desired folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Add to app config
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)

@app.route('/predict-crop', methods=['POST'])
def predict_crop():
    try:
        data = request.json
        required_fields = ['N', 'P', 'temperature', 'humidity', 'ph', 'rainfall']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Call the crop recommendation function
        prediction = recommend_crop(data)
        
        if prediction:
            return jsonify({'prediction': prediction})
        else:
            return jsonify({'error': 'Prediction failed'}), 500
    
    except Exception as e:
        logging.error(f"Error during crop prediction: {e}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/predict-soil-moisture', methods=['POST'])
def predict_soil_moisture_route():
    try:
        data = request.json
        #{'Bt_Horizon_30': 0.01, 'Bt_Horizon_deep': 0.03, 'Bulk_Density': 1.1, 'Time_Category': 'Late Morning', 'DOY': 33, 'Temperature': 33, 'Month': 3, 'ECa': 0, 'Precipitation': 0}
        required_fields = ['Bt_Horizon_30', 'Bt_Horizon_deep', 'BulkDensity', 'Time_Category', 'DOY', 'Temperature', 'Month']
        data.setdefault('ECa', 0)
        data.setdefault('Precipitation', 0)
        print(data)
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Call the soil moisture prediction function
        result = predict_soil_moisture(data)
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Prediction failed'}), 500
    
    except Exception as e:
        logging.error(f"Error during soil moisture prediction: {e}")
        return jsonify({'error': 'Server error'}), 500
    
@app.route('/crop-health-moniter', methods=['POST'])
def predict_crop_health():
    try:
        data = request.json
        required_fields = ['air_temp', 'relative_humidity', 'nitrogen_added', 'water_percent_added', 'plant_age']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Call the crop health prediction function
        prediction = categorize_health(data)
        
        if prediction:
            return jsonify({'prediction': prediction})
        else:
            return jsonify({'error': 'Prediction failed'}), 500
    except Exception as e:
        logging.error(f"Error during crop health prediction: {str(e)}")
        return jsonify({'error': 'Server error', 'details': str(e)}), 500
if __name__ == '__main__':
    app.run(port=5001,debug=True)
