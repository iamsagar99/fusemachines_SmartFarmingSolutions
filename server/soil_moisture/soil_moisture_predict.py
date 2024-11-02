import joblib
import pandas as pd

#soil_moisture/best_gb_T_with_FI_100924.pkl
# Load the models and important features
model_pipeline_T = joblib.load('soil_moisture/best_gb_T_with_FI_100924.pkl')
important_features_T = joblib.load('soil_moisture/important_features_gb_t_100924.pkl')

model_pipeline_VW = joblib.load('soil_moisture/best_gb_VW_with_FI_100924.pkl')
important_features_VW = joblib.load('soil_moisture/important_features_gb_vw_100924.pkl')

# Extract preprocessors
preprocessor_T = model_pipeline_T.named_steps['preprocessor']
preprocessor_VW = model_pipeline_VW.named_steps['preprocessor']

# Get the list of important feature names for both models
important_feature_names_T = important_features_T['Feature'].tolist()
important_feature_names_VW = important_features_VW['Feature'].tolist()

# Define function to predict T_values using the first model
def predict_T_values(input_data):
    # Convert the input into a DataFrame
    input_df = pd.DataFrame([input_data])
    print("inputdf",input_df)
    # Preprocess the input data
    preprocessed_data_T = preprocessor_T.transform(input_df)
    transformed_feature_names_T = preprocessor_T.get_feature_names_out()

    # Create a DataFrame from the preprocessed data
    preprocessed_df_T = pd.DataFrame(preprocessed_data_T, columns=transformed_feature_names_T)
    
    # Select the important features for prediction
    important_features_data_T = preprocessed_df_T[important_feature_names_T]

    # Predict T_value using the model
    predicted_T_value = model_pipeline_T.named_steps['model'].predict(important_features_data_T)

    return predicted_T_value[0]

# Define function to predict VW using the predicted T_values and original inputs
def predict_VW(input_data, predicted_T_value):
    input_data['T_values'] = predicted_T_value
    input_df = pd.DataFrame([input_data])

    # Preprocess the input data for VW prediction
    preprocessed_data_VW = preprocessor_VW.transform(input_df)
    transformed_feature_names_VW = preprocessor_VW.get_feature_names_out()

    # Create a DataFrame from the preprocessed data
    preprocessed_df_VW = pd.DataFrame(preprocessed_data_VW, columns=transformed_feature_names_VW)
    
    # Select the important features for VW prediction
    important_features_data_VW = preprocessed_df_VW[important_feature_names_VW]

    # Predict VW_value using the model
    predicted_VW_value = model_pipeline_VW.named_steps['model'].predict(important_features_data_VW)

    return predicted_VW_value[0]

# Predict soil moisture based on input data
def predict_soil_moisture(input_data):
    predicted_T_value = predict_T_values(input_data)
    predicted_VW_value = predict_VW(input_data, predicted_T_value)
    
    return {'predicted_T_value': float(predicted_T_value), 'predicted_VW_value': float(predicted_VW_value)}
