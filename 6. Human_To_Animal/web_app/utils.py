import os
import json
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from scipy.spatial.distance import cosine

# Paths
MODEL_STORAGE_DIR = "../model_storage/"
PROCESSED_IMAGE_FOLDER = "../downloaded_images/processed_images/"
MODEL_PATH = os.path.join(MODEL_STORAGE_DIR, "feature_extractor.pth")
FEATURES_FILE = os.path.join(MODEL_STORAGE_DIR, "animal_features.npy")
LABELS_FILE = os.path.join(MODEL_STORAGE_DIR, "image_labels.json")

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("🚫 Model not found! Run `feature_extraction.py` first.")
    
    model = models.resnet18()
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model = model.to(device)
    model.eval()
    return model

# Load extracted animal features & labels
def load_animal_data():
    if not os.path.exists(FEATURES_FILE) or not os.path.exists(LABELS_FILE):
        raise FileNotFoundError("🚫 Animal features not found! Run `feature_extraction.py` first.")
    
    features = np.load(FEATURES_FILE)
    with open(LABELS_FILE, "r") as f:
        labels = json.load(f)

    return features, labels

# Define image transformations (same as in feature extraction)
transform = transforms.Compose([
    transforms.Resize((224, 224)),  
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  
])

# Extract features from the uploaded human image
def extract_human_features(image):
    """Extracts features from a human face image."""
    try:
        img = Image.open(image).convert("RGB")
        img = transform(img).unsqueeze(0).to(device)

        model = load_model()

        with torch.no_grad():
            features = model(img)

        return features.cpu().numpy().flatten()
    except Exception as e:
        print(f"❌ Error processing human image: {e}")
        return None

# Compute similarity scores and find most similar image
def compute_similarity(human_features, animal_features, labels):
    """Calculates similarity between human and animal features with normalization."""
    scores = {}
    best_match_index = None
    best_match_score = -1

    for idx, animal_feature in enumerate(animal_features):
        similarity = 1 - cosine(human_features, animal_feature)  # Cosine similarity
        category = labels[str(idx)]["category"]

        if category not in scores:
            scores[category] = []

        scores[category].append(similarity)

        # Track the best matching image
        if similarity > best_match_score:
            best_match_score = similarity
            best_match_index = idx

    # Compute average similarity per animal category
    category_scores = {animal: np.mean(similarities) for animal, similarities in scores.items()}

    # Normalize Scores
    min_score = min(category_scores.values())
    max_score = max(category_scores.values())

    normalized_scores = {
        animal: ((score - min_score) / (max_score - min_score)) * 100
        for animal, score in category_scores.items()
    }

    return dict(sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)), best_match_index

# Get the most similar animal image
def get_most_similar_image(best_match_index, labels):
    """Finds the image path of the most similar animal from processed_images/."""
    if best_match_index is None:
        return None

    best_match_filename = labels[str(best_match_index)]["filename"]
    best_match_category = labels[str(best_match_index)]["category"]

    best_match_path = os.path.join(PROCESSED_IMAGE_FOLDER, best_match_category, best_match_filename)

    return best_match_path if os.path.exists(best_match_path) else None
