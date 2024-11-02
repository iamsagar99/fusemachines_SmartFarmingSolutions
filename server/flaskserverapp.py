from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
import os
from werkzeug.utils import secure_filename
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

# Add the path where your prediction files are located
sys.path.append('/Users/sagarpoudel/Desktop/FuseMachines/project/crop-prediction/crop-prediction/final/server/crop')
sys.path.append('/Users/sagarpoudel/Desktop/FuseMachines/project/crop-prediction/crop-prediction/final/server/soil_moisture')
sys.path.append('/Users/sagarpoudel/Desktop/FuseMachines/project/crop-prediction/crop-prediction/final/server/pathogen')

# Import the prediction functions
from crop_recommendation import recommend_crop
from soil_moisture_predict import predict_soil_moisture
from pathogen_classifier import predict_pathogen_func

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set upload folder for images
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create upload folder if it doesn't exist

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)

# Load models once at startup to avoid reloading during API calls
pathogen_model = load_model()  # Assuming the pathogen model requires loading
executor = ProcessPoolExecutor(max_workers=3)  # Handling multiple API calls

# Function to check allowed file extensions
def allowed_file(filename):
    """Check if the file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for crop prediction
@app.route('/predict-crop', methods=['POST'])
def predict_crop():
    """Predict crop based on provided parameters."""
    try:
        data = request.json
        required_fields = ['N', 'P', 'temperature', 'humidity', 'ph', 'rainfall']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Use ProcessPoolExecutor for concurrent task execution
        future = executor.submit(recommend_crop, data)
        prediction = future.result()  # Wait for result
        
        if prediction:
            return jsonify({'prediction': prediction})
        else:
            return jsonify({'error': 'Prediction failed'}), 500
    
    except Exception as e:
        logging.error(f"Error during crop prediction: {e}")
        return jsonify({'error': 'Server error'}), 500

# Route for soil moisture prediction
@app.route('/predict-soil-moisture', methods=['POST'])
def predict_soil_moisture_route():
    """Predict soil moisture based on provided parameters."""
    try:
        data = request.json
        required_fields = ['Bt_Horizon_30', 'Bt_Horizon_deep', 'BulkDensity', 'Time_Category', 'DOY', 'Temperature', 'Month']
        data.setdefault('ECa', 0)
        data.setdefault('Precipitation', 0)
        
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Use ProcessPoolExecutor for concurrent task execution
        future = executor.submit(predict_soil_moisture, data)
        result = future.result()  # Wait for result
        
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Prediction failed'}), 500
    
    except Exception as e:
        logging.error(f"Error during soil moisture prediction: {e}")
        return jsonify({'error': 'Server error'}), 500

# Route for pathogen prediction
@app.route('/predict-pathogen', methods=['POST'])
def predict_pathogen_route():
    """Predict pathogen based on image."""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'File extension not allowed'}), 400

        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        logging.info(f"Image saved at {image_path}")

        # Use ProcessPoolExecutor for concurrent task execution
        future = executor.submit(predict_pathogen_func, image_path)
        prediction = future.result()  # Wait for result

        if prediction:
            logging.info("Pathogen prediction successful")
            return jsonify({'prediction': prediction})
        else:
            logging.error("Pathogen prediction failed")
            return jsonify({'error': 'Prediction failed'}), 500

    except Exception as e:
        logging.error(f"Error during pathogen prediction: {e}")
        return jsonify({'error': 'Server error'}), 500

# Ensure proper multiprocessing handling in MacOS
if __name__ == '__main__':
    mp.set_start_method('spawn')  # Fix for multiprocessing issues on MacOS
    app.run(port=5000, debug=True)
