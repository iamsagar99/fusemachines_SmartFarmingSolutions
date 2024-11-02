import numpy as np
import xgboost as xgb
import joblib

# Step 1: Initialization
models= {}

def categorize_ndare(value):
    if value > 0.5:
        return 'Your crops are in good condition. Continue current irrigation and nutrient management practices. Monitor for any potential future stress.'
    elif 0.2 < value <= 0.5:
        return 'The vegetation is healthy but shows early signs of stress. Check soil moisture levels and consider applying balanced fertilizers to support growth.'
    else:
        return 'Your crops are under stress. Consider increasing irrigation and checking for pest infestations. Ensure soil has adequate levels of essential nutrients like nitrogen and phosphorus.'


def categorize_ndre(value):
    if value > 0.5:
        return 'Your crops are thriving with excellent chlorophyll content. Maintain the current level of care, including consistent irrigation and pest monitoring.'
    elif 0.3 < value <= 0.5:
        return 'The crop health is good, but keep an eye on factors like nutrient levels and water availability. Consider applying foliar fertilizers to sustain growth.'
    else:
        return 'The crops may be experiencing stress. Ensure that soil nutrients, particularly nitrogen, are sufficient. Adjust your irrigation schedule if necessary.'


def categorize_ndvig(value):
    if value > 0.6:
        return 'Your crops are showing excellent growth and canopy density. Continue with current management practices, ensuring a consistent nutrient supply.'
    elif 0.4 < value <= 0.6:
        return 'The vegetation is healthy, but slightly underperforming. Consider applying a growth stimulant or checking for early signs of water stress.'
    elif 0.2 < value <= 0.4:
        return 'Your crops may be experiencing stress due to water scarcity or nutrient deficiencies. Ensure that soil moisture and essential nutrients are adequately supplied.'
    else:
        return 'This suggests poor plant health. Urgent intervention is required, such as irrigation and application of fertilizers to promote growth.'


def categorize_ci(value):
    if value > 2.0:
        return 'Your crops have a high chlorophyll content, indicating excellent growth. Maintain the current level of nutrient and water management. Ensure there are no pest issues.'
    elif 1.0 < value <= 2.0:
        return ' The crops are healthy, but you can enhance growth with the application of nitrogen fertilizers. Check soil pH and moisture to support optimal photosynthesis.'
    else:
        return 'Your crops are showing signs of chlorophyll deficiency. Immediate application of nitrogen-based fertilizers is recommended. Monitor water supply and ensure optimal growing conditions.'


# Index being used
indexes = [
           'NDRE_L',
           'NDARE_L',
           'NDVIG_L',
        #  'CI_L'
           ]

# Step 2: Load models
for index in indexes:
    models[f'{index}_0'] = joblib.load(f'./weights/{index}_0.pkl')
    models[f'{index}_1'] = joblib.load(f'./weights/{index}_1.pkl')

models['CI_L_0'] =  joblib.load(f'./weights/CI_L_0.pkl')
models['CI_L_1'] =  joblib.load(f'./weights/CI_L_1.pkl')


# Step 3: Define user inputs and function for prediction
def get_user_inputs():
    air_temp = float(input('Air Temperature:'))
    relative_humidity = float(input('Relative Humidity: '))
    nitrogen_added = float(input('Nitrogen added: '))
    water_percent_added = float(input('Water Percent: '))
    plant_age = float(input('Plant Age: '))

    model_input = np.array([[air_temp, relative_humidity, nitrogen_added, water_percent_added, plant_age]])

    return model_input

def predict_indices(model_input):
    outputs = {}

    for index in indexes:
        ref_0 = models[f'{index}_0'].predict(model_input)
        ref_1 = models[f'{index}_1'].predict(model_input)
        y_pred = (ref_1 - ref_0) / (ref_1 + ref_0)
        outputs[f'{index.strip('_L')}'] = y_pred

    ref_0 = models[f'CI_L_0'].predict(model_input)
    ref_1 = models[f'CI_L_1'].predict(model_input)
    y_pred = ref_1 / ref_0 - 1
    outputs['CI'] = y_pred

    return outputs


# Step 4: Simulation
if __name__ == "__main__":
    user_input = get_user_inputs()

    outputs = predict_indices(user_input)

    ndre_value = outputs['NDRE'][0]
    ndare_value = outputs['NDARE'][0]
    ndvig_value = outputs['NDVIG'][0]
    ci_value = outputs['CI'][0]

    print(f'Suggestions:')
    print(f'NDARE({ndare_value:.3f}): {categorize_ndare(ndare_value)}')
    print(f'NDRE({ndre_value:.3f}): {categorize_ndre(ndre_value)}')
    print(f'NDVIG({ndvig_value:.3f}): {categorize_ndvig(ndvig_value)}')
    print(f'NDRE({ci_value:.3f}): {categorize_ci(ci_value)}')
