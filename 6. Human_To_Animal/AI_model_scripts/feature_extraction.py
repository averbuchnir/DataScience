import os
import json
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

PROCESSED_IMAGE_FOLDER = "downloaded_images/processed_images/"
MODEL_STORAGE_DIR = "model_storage/"  # Directory for storing the model
MODEL_PATH = os.path.join(MODEL_STORAGE_DIR, "feature_extractor.pth")  # Saved model file
FEATURES_OUTPUT_FILE = os.path.join(MODEL_STORAGE_DIR, "animal_features.npy")
LABELS_OUTPUT_FILE = os.path.join(MODEL_STORAGE_DIR, "image_labels.json")

# Ensure model storage directory exists
os.makedirs(MODEL_STORAGE_DIR, exist_ok=True)

# Check for GPU availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load Pretrained Model (ResNet18 for now, but can switch to EfficientNet or others)
def load_model():
    if os.path.exists(MODEL_PATH):
        print("📥 Loading saved model...")
        model = models.resnet18()
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    else:
        print("🔄 Downloading and saving ResNet18 model...")
        model = models.resnet18(pretrained=True)
        torch.save(model.state_dict(), MODEL_PATH)  # Save the model for future use

    model = model.to(device)
    model.eval()
    return model

model = load_model()

# Define transformation pipeline for images
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # ResNet input size
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Standard ImageNet normalization
])

# Extract features function
def extract_features(image_path):
    """Loads an image, applies transformations, and extracts CNN features."""
    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0).to(device)  # Add batch dimension

        with torch.no_grad():
            features = model(image)

        return features.cpu().numpy().flatten()
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

# Process all images and extract features
def process_images():
    feature_vectors = []
    image_labels = {}

    for category in os.listdir(PROCESSED_IMAGE_FOLDER):
        category_path = os.path.join(PROCESSED_IMAGE_FOLDER, category)

        if os.path.isdir(category_path):  # Ensure it's a folder
            for image_name in os.listdir(category_path):
                image_path = os.path.join(category_path, image_name)
                folder_name = os.path.basename(category_path)
                print(f"🔍 Extracting features from {folder_name}")

                if image_name.lower().endswith((".jpg", ".jpeg", ".png")):
                    # print(f"🔍 Extracting features from: {image_name}")

                    features = extract_features(image_path)
                    if features is not None:
                        feature_vectors.append(features)
                        image_labels[len(feature_vectors) - 1] = {
                            "filename": image_name,
                            "category": category
                        }

    # Save extracted features and labels
    np.save(FEATURES_OUTPUT_FILE, np.array(feature_vectors))
    with open(LABELS_OUTPUT_FILE, "w") as f:
        json.dump(image_labels, f, indent=4)

    print(f"✅ Feature extraction complete. Saved {len(feature_vectors)} feature vectors.")

if __name__ == "__main__":
    process_images()
