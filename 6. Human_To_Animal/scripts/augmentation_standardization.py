import os
import json
from PIL import Image, ImageOps

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

INPUT_FOLDER = config["metadata_file"].replace("metadata.json", "")  # Points to downloaded_images
MODEL_STORAGE_DIR = "model_storage/"  # Save metadata in model_storage
LOG_FILE = os.path.join(MODEL_STORAGE_DIR, "augmentation_metadata.json")  # New path

# Ensure directories exist
os.makedirs(MODEL_STORAGE_DIR, exist_ok=True)

# Load previous metadata if exists
def load_augmentation_metadata():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return {}

# Save metadata
def save_augmentation_metadata(metadata):
    with open(LOG_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

# Augment and standardize images
def augment_and_standardize(image_path, output_folder, base_filename, augmentation_metadata):
    """Applies rotation, flipping, and resizing to an image while ensuring proper conversion."""
    try:
        img = Image.open(image_path)

        # Handle transparent PNGs and palette-based images
        if img.mode in ["P", "LA", "RGBA"]:
            img = img.convert("RGBA")
            # Create a white background and merge it with the transparent image
            background = Image.new("RGBA", img.size, (255, 255, 255, 255))
            img = Image.alpha_composite(background, img).convert("RGB")
        else:
            img = img.convert("RGB")

        # Get category (Dog, Cat, etc.)
        category = os.path.basename(os.path.dirname(image_path))
        category_folder = os.path.join(output_folder, category)
        os.makedirs(category_folder, exist_ok=True)

        # Standardization - Resize to 256x256
        img_resized = img.resize((256, 256))
        original_filename = f"{base_filename}.jpg"
        img_resized.save(os.path.join(category_folder, original_filename))

        # Augmentation: Rotation (-20° to +20°)
        rotated_files = []
        for angle in [-20, -10, 10, 20]:
            img_rotated = img.rotate(angle)
            rotated_filename = f"{base_filename}_rotated_{angle}.jpg"
            img_rotated_resized = img_rotated.resize((256, 256))
            img_rotated_resized.save(os.path.join(category_folder, rotated_filename))
            rotated_files.append(rotated_filename)

        # Augmentation: Horizontal Flip
        img_flipped = ImageOps.mirror(img)
        flipped_filename = f"{base_filename}_flipped.jpg"
        img_flipped_resized = img_flipped.resize((256, 256))
        img_flipped_resized.save(os.path.join(category_folder, flipped_filename))

        # Log metadata
        augmentation_metadata[original_filename] = {
            "original": original_filename,
            "category": category,
            "augmentations": [
                {"type": "rotation", "angle": angle, "filename": rotated_filename} for angle, rotated_filename in zip([-20, -10, 10, 20], rotated_files)
            ] + [{"type": "flip", "filename": flipped_filename}]
        }

    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")

# Main function for augmentation
def run_augmentation():
    augmentation_metadata = load_augmentation_metadata()

    for root, _, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(root, file)
                base_filename, _ = os.path.splitext(file)
                augment_and_standardize(image_path, MODEL_STORAGE_DIR, base_filename, augmentation_metadata)

    save_augmentation_metadata(augmentation_metadata)
    print(f"✅ Augmentation and Standardization Complete! Metadata saved at {LOG_FILE}")

