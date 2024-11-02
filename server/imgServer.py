from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sys
import os
from werkzeug.utils import secure_filename

sys.path.append('pathogen')
from pathogen_classifier import predict_pathogen_func

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set upload folder
UPLOAD_FOLDER = 'uploads'  # Change this to your desired folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Add to app config
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.INFO)

@app.route('/predict-pathogen', methods=['POST'])
def predict_pathogen_route():
    try:
        print("hello-------------------")
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        print("Image saved")

        prediction = predict_pathogen_func(image_path)
        # print('prediction-sss',prediction)
        if prediction:
            print("Prediction successful")
            return jsonify({'prediction': prediction})
        else:
            print("Prediction error")
            return jsonify({'error': 'Prediction failed'}), 500

    except Exception as e:
        logging.error(f"Error during pathogen prediction: {e}")
        return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
