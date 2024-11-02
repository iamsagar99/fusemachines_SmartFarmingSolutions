import torch
from torchvision import transforms, models
from config import MEAN, STD, DEVICE, DROPOUT_RATE, WEIGHTS, NUM_CLASSES
import torch.nn.functional as F

def load_transform():
    return transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
        transforms.Normalize(mean=MEAN, std=STD),
    ])

class PathogenClassifier(torch.nn.Module):
    def __init__(self, num_classes):
        super(PathogenClassifier, self).__init__()
        self.base_model = models.resnet50(weights=WEIGHTS)
        self.base_model.fc = torch.nn.Linear(self.base_model.fc.in_features, num_classes)
        self.dropout = torch.nn.Dropout(DROPOUT_RATE)

    def forward(self, x):
        x = self.base_model(x)
        return x

def load_model(model_path):
    print("Loading model...")
    model = PathogenClassifier(num_classes=NUM_CLASSES)
    state_dict = torch.load(model_path, map_location='cpu')
    model.load_state_dict(state_dict)
    model.to(DEVICE)
    model.eval()
    print("Model loaded and set to evaluation mode.")
    return model

def predict_image(image, model, transform):
    image = image.convert('RGB')
    image = transform(image).unsqueeze(0).to(DEVICE)
    
    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output, dim=1)  # Apply softmax to get probabilities
        confidence, predicted = torch.max(probabilities, 1)  # Get max probability and predicted class
        
    predicted_class = predicted.item()
    confidence_score = confidence.item()  # Extract confidence score as a Python float
    
    print(f'Predicted class: {predicted_class}, Confidence: {confidence_score * 100:.2f}%')
    
    return predicted_class,confidence_score


# notebook , src_>backend, frontend, readme, 