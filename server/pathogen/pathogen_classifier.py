import sys
import traceback

try:
    import torch
    import numpy as np
    from PIL import Image
    from build_feature import load_transform, load_model, predict_image
    from config import model_save_path
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please ensure all required libraries are installed.")
    sys.exit(1)

class_names = ['Bacterial infection', 'Fungal infection', 'Healthy plant', 'Pest infestation', 'Viral infection']

def load_trained_model():
    try:
        model = load_model(model_save_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        print(traceback.format_exc())
        return None
 



pathogen_solutions = {
    'Bacterial infection': {
        'English': {
            'Practices': [
                "Remove and destroy infected plants or plant parts.",
                "Avoid overhead watering to reduce leaf wetness.",
                "Use certified disease-free seeds or planting material.",
                "Ensure proper crop rotation, especially with non-host crops.",
                "Practice proper sanitation (cleaning tools, equipment, and hands between plant handling)."
            ],
            'Chemical Alternatives': [
                "Copper-based bactericides (e.g., Copper Oxychloride, Copper Sulfate).",
                "Streptomycin or Oxytetracycline under severe bacterial infestations."
            ]
        },
        'Nepali': {
            'Practices': [
                "संक्रमित बिरुवा वा बिरुवाका भागहरू हटाउनुहोस् र नष्ट गर्नुहोस्।",
                "पातलाई चिस्यान कम गर्न माथिबाट पानी नहाल्नुहोस्।",
                "प्रमाणित रोग-मुक्त बीउ वा रोपण सामग्री प्रयोग गर्नुहोस्।",
                "उचित बाली परिवर्तनको अभ्यास गर्नुहोस्, विशेषगरी गैर-होस्ट बालीसँग।",
                "उपकरणहरू र हातहरू सफा गरेर उचित सरसफाइको अभ्यास गर्नुहोस्।"
            ],
            'Chemical Alternatives': [
                "तामा आधारित ब्याक्टेरिसाइड्स (Copper Oxychloride, Copper Sulfate).",
                "गम्भीर संक्रमणमा Streptomycin वा Oxytetracycline प्रयोग गर्न सकिन्छ।"
            ]
        }
    },
    'Viral infection': {
        'English': {
            'Practices': [
                "Remove and destroy infected plants immediately to prevent the spread.",
                "Control insect vectors (e.g., aphids, whiteflies) that transmit viral diseases.",
                "Use virus-resistant varieties whenever possible.",
                "Maintain good field hygiene to reduce vector populations."
            ],
            'Chemical Alternatives': [
                "Insecticides like Imidacloprid or Pyriproxyfen for insect vector control.",
                "Mineral oils or insecticidal soaps can reduce virus transmission by vectors."
            ]
        },
        'Nepali': {
            'Practices': [
                "संक्रमित बिरुवाहरू तुरुन्तै हटाएर नष्ट गर्नुहोस् ताकि रोग नफैलियोस्।",
                "भाइरस रोग फैलाउने कीराहरू (एफिड, ह्वाइटफ्लाई) नियन्त्रण गर्नुहोस्।",
                "भाइरस-प्रतिरोधी जातिहरू प्रयोग गर्नुहोस्।",
                "खेतमा सफाइको राम्रो अभ्यास गरेर कीराहरूको संख्या घटाउनुहोस्।"
            ],
            'Chemical Alternatives': [
                "Imidacloprid वा Pyriproxyfen जस्ता कीटनाशकहरू प्रयोग गरेर कीराहरू नियन्त्रण गर्नुहोस्।",
                "Mineral oils वा Insecticidal soaps प्रयोगले भाइरस फैलिनबाट रोक्न सक्छ।"
            ]
        }
    },
    'Fungal infection': {
        'English': {
            'Practices': [
                "Remove affected plant parts to reduce spore production.",
                "Ensure proper plant spacing to allow good air circulation.",
                "Avoid overhead irrigation; use drip irrigation instead.",
                "Apply organic mulches to prevent fungal growth."
            ],
            'Chemical Alternatives': [
                "Fungicides such as Mancozeb, Chlorothalonil, and Propiconazole.",
                "Sulfur and Copper-based fungicides (Copper Hydroxide)."
            ]
        },
        'Nepali': {
            'Practices': [
                "संक्रमित बिरुवाका भागहरू हटाउनुहोस् ताकि बीउ उत्पादन घटोस्।",
                "बिरुवाहरूको उचित दूरी राख्नुहोस् जसले राम्रो हावाको संचलन सुनिश्चित गर्छ।",
                "माथिबाट सिँचाइ नगर्नुहोस्; ड्रिप सिँचाइ प्रयोग गर्नुहोस्।",
                "जैविक मलको प्रयोग गरेर फंगसको वृद्धि रोक्नुहोस्।"
            ],
            'Chemical Alternatives': [
                "Mancozeb, Chlorothalonil, र Propiconazole जस्ता फङ्गिसाइडहरू।",
                "Sulfur र Copper-based fungicides (Copper Hydroxide)."
            ]
        }
    },
    'Pest infestation': {
        'English': {
            'Practices': [
                "Use natural predators (ladybugs, parasitic wasps) to control pest populations.",
                "Introduce crop rotation and intercropping to reduce pest infestations.",
                "Remove weeds and debris to reduce pest habitats.",
                "Use sticky traps or pheromone traps to monitor and control pest populations."
            ],
            'Chemical Alternatives': [
                "Insecticides like Spinosad, Neem Oil, Lambda-Cyhalothrin, and Imidacloprid.",
                "Miticides like Abamectin for controlling mites.",
                "Insecticidal soaps or horticultural oils for soft-bodied insects (aphids, whiteflies)."
            ]
        },
        'Nepali': {
            'Practices': [
                "प्राकृतिक शिकारीहरू (जस्तै लेडीबग्स, परजीवी बयब्लाहरू) प्रयोग गर्नुहोस्।",
                "बाली परिवर्तन र सह-बालीको अभ्यास गरेर कीराहरूको संक्रमण घटाउनुहोस्।",
                "घाँस र फोहोर हटाउनुहोस् जसले कीराहरूको आश्रयस्थल हुन सक्छ।",
                "कीराहरूको नियन्त्रणका लागि स्टिकी ट्र्यापहरू वा फेरोमोन ट्र्यापहरूको प्रयोग गर्नुहोस्।"
            ],
            'Chemical Alternatives': [
                "Spinosad, Neem Oil, Lambda-Cyhalothrin, र Imidacloprid जस्ता कीटनाशकहरू।",
                "Abamectin जस्ता माइटिसाइडहरू माइट्स नियन्त्रणका लागि।",
                "नरम शरीर भएका कीराहरूको लागि Insecticidal soaps वा Horticultural oils प्रयोग गर्नुहोस्।"
            ]
        }
    },
    'Healthy plant': {
    'English': {
        'Practices': ["The plant is healthy and looks great. Therefore, no treatment is required."],
        'Chemical Alternatives': ["The plant is healthy and looks great. Therefore, no treatment is required."]
    },
    'Nepali': {
        'Practices': ["बिरुवा स्वस्थ देखिन्छ र राम्रो देखिन्छ। त्यसैले, कुनै उपचार आवश्यक छैन।"],
        'Chemical Alternatives': [" "]
    }
}

   
}
 # 'Healthy plant': {
    #     'English': {
    #         'Message': "The plant is healthy and looks great. Therefore, no treatment is required."
    #     },
    #     'Nepali': {
    #         'Message': "बिरुवा स्वस्थ देखिन्छ र राम्रो देखिन्छ। त्यसैले, कुनै उपचार आवश्यक छैन।"
    #     }
    # }

def predict_pathogen_func(image_path):
    print(f"Processing image: {image_path}")
    
    try:
        model = load_trained_model()
        if model is None:
            return {'error': "Failed to load the model"}

        transform = load_transform()
        print("Transform loaded")

        image = Image.open(image_path)
        print("Image loaded successfully")

        predicted_class, confidence_score = predict_image(image, model, transform)
        predicted_class_name = class_names[predicted_class]
        print(f"Prediction made: {predicted_class_name}")

        # Prepare the response dictionary
        response = {
            'predicted_class': predicted_class_name,
            'confidence': confidence_score,
            'solutions': {}
        }

        if predicted_class_name in pathogen_solutions:
            if predicted_class_name == 'Healthy plant':
                # response['solutions']['English'] = pathogen_solutions['Healthy plant']['English']['Message']
                # response['solutions']['Nepali'] = pathogen_solutions['Healthy plant']['Nepali']['Message']
                response['solutions']['English'] = {
                    'Practices': pathogen_solutions[predicted_class_name]['English']['Practices'],
                    'Chemical Alternatives': pathogen_solutions[predicted_class_name]['English']['Chemical Alternatives']
                }
                response['solutions']['Nepali'] = {
                    'Practices': pathogen_solutions[predicted_class_name]['Nepali']['Practices'],
                    'Chemical Alternatives': pathogen_solutions[predicted_class_name]['Nepali']['Chemical Alternatives']
                }
            else:
                response['solutions']['English'] = {
                    'Practices': pathogen_solutions[predicted_class_name]['English']['Practices'],
                    'Chemical Alternatives': pathogen_solutions[predicted_class_name]['English']['Chemical Alternatives']
                }
                response['solutions']['Nepali'] = {
                    'Practices': pathogen_solutions[predicted_class_name]['Nepali']['Practices'],
                    'Chemical Alternatives': pathogen_solutions[predicted_class_name]['Nepali']['Chemical Alternatives']
                }
        else:
            response['solutions'] = {'English': "The plant appears to be healthy, no action needed.", 
                                     'Nepali': "बिरुवा स्वस्थ देखिन्छ, कुनै कदम आवश्यक छैन।"}

        return response

    except Exception as e:
        error_msg = f"Error during prediction: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return {'error': error_msg}

# Add this at the end of the file
if __name__ == "__main__":
    print("NumPy version:", np.__version__)
    print("PyTorch version:", torch.__version__)
    print("PIL version:", Image.__version__)