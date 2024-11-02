import torch

# Paths
model_save_path = 'pathogen/best_pathogen_classifier_model_150824.pth'

# Training configurations
BATCH_SIZE = 32
NUM_CLASSES = 5
LEARNING_RATE = 1e-3
NUM_EPOCHS = 10
IMAGE_SIZE = (512, 512)

# Dataset transformations
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

# Model parameters
DROPOUT_RATE = 0.2
WEIGHTS = None  # Set to None for CPU-only inference

# Device
DEVICE = 'cpu'  # Force CPU usage

# Versioning
TORCH_VERSION = torch.__version__
print(f"PyTorch version: {TORCH_VERSION}")