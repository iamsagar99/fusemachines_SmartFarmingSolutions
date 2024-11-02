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

def categorize_ndare_np(value):
    if value > 0.5:
        return 'तपाईंका फसलहरू राम्रो अवस्थामा छन्। हालको सिँचाइ र पोषण व्यवस्थापन अभ्यासहरू जारी राख्नुहोस्। भविष्यमा कुनै सम्भावित तनावको लागि अनुगमन गर्नुहोस्।'
    elif 0.2 < value <= 0.5:
        return 'वनस्पति स्वस्थ छ तर तनावका प्रारम्भिक संकेतहरू देखाउँछ। माटोको आर्द्रता स्तर जाँच गर्नुहोस् र विकासलाई समर्थन गर्न सन्तुलित मलको प्रयोग गर्न विचार गर्नुहोस्।'
    else:
        return 'तपाईंका फसलहरू तनावमा छन्। सिँचाइ बढाउने र कीटको संक्रमण जाँच गर्न विचार गर्नुहोस्। माटोमा नाइट्रोजन र फस्फोरस जस्ता आवश्यक पोषक तत्वहरूको पर्याप्त स्तर सुनिश्चित गर्नुहोस्।'

def categorize_ndre_np(value):
    if value > 0.5:
        return 'तपाईंका फसलहरू उत्कृष्ट क्लोरोफिल सामग्रीका साथ फुलिरहेका छन्। निरन्तर सिँचाइ र कीट अनुगमन समावेश गरेर हालको हेरचाहको स्तर कायम राख्नुहोस्।'
    elif 0.3 < value <= 0.5:
        return 'फसलको स्वास्थ्य राम्रो छ, तर पोषणको स्तर र पानीको उपलब्धताजस्ता कारकहरूको निगरानी गर्नुहोस्। विकासलाई कायम राख्नका लागि पातमा लगाउने मलको प्रयोग गर्न विचार गर्नुहोस्।'
    else:
        return 'फसलहरूले तनाव अनुभव गर्दैछन्। माटोका पोषक तत्वहरू, विशेष गरी नाइट्रोजन, पर्याप्त छन् कि छैनन् सुनिश्चित गर्नुहोस्। आवश्यक भएमा तपाईंको सिँचाइ तालिका समायोजन गर्नुहोस्।'

def categorize_ndvig_np(value):
    if value > 0.6:
        return 'तपाईंका फसलहरूले उत्कृष्ट विकास र क्यानोपी घनत्व देखाउँदैछन्। निरन्तर पोषण आपूर्तिको सुनिश्चित गर्दै हालको व्यवस्थापन अभ्यासहरू जारी राख्नुहोस्।'
    elif 0.4 < value <= 0.6:
        return 'वनस्पति स्वस्थ छ, तर थोरै कम प्रदर्शन गर्दैछ। विकास उत्तेजकको प्रयोग गर्न विचार गर्नुहोस् वा पानीको तनावका प्रारम्भिक संकेतहरूको जाँच गर्नुहोस्।'
    elif 0.2 < value <= 0.4:
        return 'तपाईंका फसलहरूले पानीको कमी वा पोषक तत्वको कमीका कारण तनाव अनुभव गर्दैछन्। माटोको आर्द्रता र आवश्यक पोषक तत्वहरू पर्याप्त रूपमा उपलब्ध छन् कि छैनन् सुनिश्चित गर्नुहोस्।'
    else:
        return 'यसले बिरुवाको स्वास्थ्य कमजोर संकेत गर्दछ। विकासलाई प्रोत्साहित गर्न सिँचाइ र मलको लागू गर्ने जस्ता तत्काल हस्तक्षेप आवश्यक छ।'

def categorize_ci_np(value):
    if value > 2.0:
        return 'तपाईंका फसलहरूमा उच्च क्लोरोफिल सामग्री छ, जसले उत्कृष्ट विकासको संकेत गर्दछ। पोषण र पानीको व्यवस्थापनको हालको स्तर कायम राख्नुहोस्। कीटको समस्या छैन भन्ने कुरा सुनिश्चित गर्नुहोस्।'
    elif 1.0 < value <= 2.0:
        return 'फसलहरू स्वस्थ छन्, तर नाइट्रोजन मलको प्रयोग गरेर विकासलाई वृद्धि गर्न सक्नुहुन्छ। उचित प्रकाश संश्लेषणको लागि माटोको pH र आर्द्रता जाँच गर्नुहोस्।'
    else:
        return 'तपाईंका फसलहरू क्लोरोफिलको कमीका संकेतहरू देखाउँदैछन्। नाइट्रोजन-आधारित मलको तत्काल प्रयोग सिफारिस गरिन्छ। पानीको आपूर्ति अनुगमन गर्नुहोस् र उचित वृद्धिका लागि अवस्थाहरू सुनिश्चित गर्नुहोस्।'


# Index being used
indexes = [
           'NDRE_L',
           'NDARE_L',
           'NDVIG_L',
        #  'CI_L'
           ]

# Step 2: Load models
path = 'crop_health/models'
for index in indexes:
    models[f'{index}_0'] = joblib.load(f'{path}/{index}_0.pkl')
    models[f'{index}_1'] = joblib.load(f'{path}/{index}_1.pkl')

models['CI_L_0'] =  joblib.load(f'{path}/CI_L_0.pkl')
models['CI_L_1'] =  joblib.load(f'{path}/CI_L_1.pkl')




def predict_indices(model_input):
    outputs = {}
    air_temp = np.float32(model_input['air_temp'])
    relative_humidity = np.float32(model_input['relative_humidity'])
    nitrogen_added = np.float32(model_input['nitrogen_added'])
    water_percent_added = np.float32(model_input['water_percent_added'])
    plant_age = np.float32(model_input['plant_age'])
    features = np.array([[
        air_temp,
        relative_humidity,
        nitrogen_added,
        water_percent_added,
        plant_age
    ]])

    for index in indexes:
        ref_0 = models[f'{index}_0'].predict(features)
        ref_1 = models[f'{index}_1'].predict(features)
        y_pred = (ref_1 - ref_0) / (ref_1 + ref_0)
        outputs[f"{index.strip('_L')}"] = y_pred

    ref_0 = models[f'CI_L_0'].predict(features)
    ref_1 = models[f'CI_L_1'].predict(features)
    y_pred = ref_1 / ref_0 - 1
    outputs['CI'] = y_pred

    return outputs

"""
result = {
        ndre:{
            value: 0.5,
            category: 'good'
        },
        ndare:{
            value: 0.5,
            category: 'good'
        },
        ndvig:{
            value: 0.5,
            category: 'good'
        },
        ci:{
            value: 0.5,
            category: 'good'
        }
    }


"""

def categorize_health(model_input):
    outputs = predict_indices(model_input)
    ndre_value = float(outputs['NDRE'][0])  # Convert to native Python float
    ndare_value = float(outputs['NDARE'][0])
    ndvig_value = float(outputs['NDVIG'][0])
    ci_value = float(outputs['CI'][0])
    
    result = {
        'NDRE': {
            'value': ndre_value,
            'category': categorize_ndre(ndre_value),
            'np': categorize_ndre_np(ndre_value)
        },
        'NDARE': {
            'value': ndare_value,
            'category': categorize_ndare(ndare_value),
            'np': categorize_ndare_np(ndare_value)
        },
        'NDVIG': {
            'value': ndvig_value,
            'category': categorize_ndvig(ndvig_value),
            'np': categorize_ndvig_np(ndvig_value)
        },
        'CI': {
            'value': ci_value,
            'category': categorize_ci(ci_value),
            'np': categorize_ci_np(ci_value)
        }
    }

    return result