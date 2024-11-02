import numpy as np
from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
#% finalflask/bin/python flaskserverapp.py

app = Flask(__name__)
CORS(app)


model = joblib.load('/Users/sagarpoudel/Desktop/FuseMachines/project/crop-prediction/crop-prediction/final/modelxgb.pkl')
sc = joblib.load('/Users/sagarpoudel/Desktop/FuseMachines/project/crop-prediction/crop-prediction/final/scalerxgb.pkl')
le = joblib.load('/Users/sagarpoudel/Desktop/FuseMachines/project/crop-prediction/crop-prediction/final/labelencoderxgb.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Create a DataFrame from the input data
    df = pd.DataFrame([data])
    df = df.astype(float)

    # print(df.info())
    # Ensure the columns are in the correct order
    df = df[['N', 'P', 'temperature', 'humidity', 'ph', 'rainfall']]
    
    # Apply transformations
    df[['N', 'P', 'temperature', 'humidity', 'ph', 'rainfall']] = np.log1p(df[['N', 'P', 'temperature', 'humidity', 'ph', 'rainfall']])
    df[['N', 'P', 'temperature', 'humidity', 'ph', 'rainfall']] = sc.transform(df[['N', 'P', 'temperature', 'humidity', 'ph', 'rainfall']])
    print(df.shape)
    print(df)
    # Make prediction
    prediction = model.predict(df)
    
    # Inverse transform the prediction to get the original label
    prediction = le.inverse_transform(prediction)
    
    return jsonify({'prediction': prediction[0]})
    # print("jdafa")

if __name__ == '__main__':
    app.run(debug=True)