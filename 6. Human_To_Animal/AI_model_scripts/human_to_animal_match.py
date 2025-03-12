import os
import json
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from scipy.spatial.distance import cosine
import matplotlib.pyplot as plt

# Paths
MODEL_STORAGE_DIR = "model_storage/"
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
def extract_human_features(image_path, model):
    """Extracts features from a human face image."""
    try:
        img = Image.open(image_path).convert("RGB")
        img = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            features = model(img)

        return features.cpu().numpy().flatten()
    except Exception as e:
        print(f"❌ Error processing human image: {e}")
        return None

# Compute similarity scores
def compute_similarity(human_features, animal_features, labels):
    """Calculates similarity between human and animal features with normalization."""
    scores = {}

    for idx, animal_feature in enumerate(animal_features):
        similarity = 1 - cosine(human_features, animal_feature)  # Cosine similarity
        category = labels[str(idx)]["category"]

        if category not in scores:
            scores[category] = []
        
        scores[category].append(similarity)

    # Compute average similarity per animal category
    category_scores = {animal: np.mean(similarities) for animal, similarities in scores.items()}

    # 1️⃣ **Normalize Scores: Ensure No Negative Values**
    min_score = min(category_scores.values())
    max_score = max(category_scores.values())

    # Adjust all scores to be between 0 and 100%
    normalized_scores = {
        animal: ((score - min_score) / (max_score - min_score)) * 100
        for animal, score in category_scores.items()
    }

    # 2️⃣ **Remove Low Confidence Matches (<1%)**
    filtered_scores = {animal: score for animal, score in normalized_scores.items() if score > 1}

    return dict(sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True))  # Sort by highest match

# Generate Pie Chart with Original Image
def plot_results(results, image_path):
    """Displays similarity percentages as a pie chart and includes the original human image."""
    labels = list(results.keys())
    values = list(results.values())

    best_match = labels[0]  # Best match animal

    fig, axes = plt.subplots(1, 2, figsize=(10, 6))  # Create a subplot layout

    # Load and display the original image
    img = Image.open(image_path)
    axes[0].imshow(img)
    axes[0].axis("off")
    axes[0].set_title("Uploaded Image", fontsize=12, fontweight="bold")

    # Create the pie chart
    axes[1].pie(values, labels=labels, autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
    axes[1].set_title(f"Best Match: {best_match}", fontsize=14, fontweight="bold")

    plt.tight_layout()
    plt.show()

# Main function to process the uploaded image
def match_human_to_animal(image_path):
    model = load_model()
    animal_features, labels = load_animal_data()

    human_features = extract_human_features(image_path, model)
    if human_features is None:
        return

    results = compute_similarity(human_features, animal_features, labels)

    print("\n🎭 Human-to-Animal Match Results:")
    for animal, percentage in results.items():
        print(f"🐾 {animal}: {percentage:.2f}%")

    # Plot Pie Chart with Image
    plot_results(results, image_path)

    return results

if __name__ == "__main__":
    image_dir = "image_to_upload"
    valid_extensions = (".jpg", ".jpeg", ".png")

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(valid_extensions):
            human_image = os.path.join(image_dir, filename)
            if os.path.exists(human_image):
                print(f"\n📸 Processing: {filename}...\n")
                match_human_to_animal(human_image)
            else:
                print(f"🚫 File not found: {filename}")
