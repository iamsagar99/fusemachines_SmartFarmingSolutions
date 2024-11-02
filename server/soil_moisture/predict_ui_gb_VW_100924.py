import joblib
import pandas as pd

# Step 1: Load the model, preprocessor, and important features
model_pipeline_T = joblib.load('./model/best_gb_T_with_FI_100924.pkl')
important_features_T = joblib.load('./important_features/important_features_gb_t_100924.pkl')

model_pipeline_VW = joblib.load('./model/best_gb_VW_with_FI_100924.pkl')
important_features_VW = joblib.load('./important_features/important_features_gb_vw_100924.pkl')

# Extract preprocessors from both models
preprocessor_T = model_pipeline_T.named_steps['preprocessor']
preprocessor_VW = model_pipeline_VW.named_steps['preprocessor']

# Get the list of important feature names for both models
important_feature_names_T = important_features_T['Feature'].tolist()
important_feature_names_VW = important_features_VW['Feature'].tolist()

# Step 2: Define a function to get user input for the first model
def get_user_input():
    print("Please enter the feature values:")
    Bt_Horizon_30 = float(input("Bt_Horizon_30 (range:0 - 0.025, e.g., 0.05): "))
    Bt_Horizon_deep = float(input("Bt_Horizon_deep (range: 0 - 0.8, e.g., 0.5): "))
    Bulk_Density = float(input("Bulk Density (range: 1-1.6, e.g: 1.2): "))
    Time_Category = input("Time Category (e.g., 'Morning to Midday', 'Late Morning', 'Evening to Midnight', 'Early Morning', 'Late Afternoon to Early Evening'): ")
    DOY = int(input("Day of Year (e.g., 45): "))
    Temperature = float(input("Temperature (range: -36 - 36, e.g., 18.5): "))
    Month = int(input("Month (e.g., 5 for May): "))

    return {
        'Bt_Horizon_30': Bt_Horizon_30,
        'Bt_Horizon_deep': Bt_Horizon_deep,
        'BulkDensity': Bulk_Density,
        'Time_Category': Time_Category,
        'DOY': DOY,
        'Temperature': Temperature,
        'Month': Month,
        'ECa': 0,  # Default value
        'Precipitation': 0  # Default value
    }


# Step 3: Define a function to predict T_values using the first model
def predict_T_values(input_data):
    # Convert the input into a DataFrame
    input_df = pd.DataFrame([input_data])

    # Preprocess the input data using the preprocessor from the first model
    preprocessed_data = preprocessor_T.transform(input_df)

    # Get the transformed feature names from the preprocessor
    transformed_feature_names_T = preprocessor_T.get_feature_names_out()

    # Create a DataFrame from the preprocessed data
    preprocessed_df_T = pd.DataFrame(preprocessed_data, columns=transformed_feature_names_T)

    # Reorder columns to match the order used during model training
    important_features_data_T = preprocessed_df_T[important_feature_names_T]

    # Make the prediction using the trained model
    predicted_T_value = model_pipeline_T.named_steps['model'].predict(important_features_data_T)

    print(f"The predicted T_value is: {predicted_T_value[0]:.2f}")
    return predicted_T_value[0]

# Step 4: Define a function to predict VW using the predicted T_values and original inputs
def predict_VW(input_data, predicted_T_value):
    # Add the predicted T_value to the input data
    input_data['T_values'] = predicted_T_value

    # Convert the input into a DataFrame
    input_df = pd.DataFrame([input_data])

    # Preprocess the input data using the preprocessor from the second model
    preprocessed_data_VW = preprocessor_VW.transform(input_df)

    # Get the transformed feature names from the second model's preprocessor
    transformed_feature_names_VW = preprocessor_VW.get_feature_names_out()

    # Create a DataFrame from the preprocessed data
    preprocessed_df_VW = pd.DataFrame(preprocessed_data_VW, columns=transformed_feature_names_VW)

    # Reorder columns to match the order used during model training for VW
    important_features_data_VW = preprocessed_df_VW[important_feature_names_VW]

    # Make the prediction for VW using the second model
    predicted_VW_value = model_pipeline_VW.named_steps['model'].predict(important_features_data_VW)

    print(f"The predicted moisture level (VW_value) is: {predicted_VW_value[0]:.2f}")

# Step 5: Main logic for getting user input and making predictions
if __name__ == "__main__":
    # Get user input for the first model
    user_input = get_user_input()

    # Predict T_value using the first model
    predicted_T_value = predict_T_values(user_input)

    # Use the predicted T_value along with original inputs to predict VW_value
    predict_VW(user_input, predicted_T_value)