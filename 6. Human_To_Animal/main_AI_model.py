import os
import subprocess

# Paths to the AI model scripts
AI_MODEL_DIR = "AI_model_scripts"
FEATURE_EXTRACTION_SCRIPT = os.path.join(AI_MODEL_DIR, "feature_extraction.py")
HUMAN_MATCH_SCRIPT = os.path.join(AI_MODEL_DIR, "human_to_animal_match.py")
IMAGE_UPLOAD_DIR = "image_to_upload"

def run_feature_extraction():
    """Runs the feature extraction script to generate animal embeddings."""
    print("\n🔄 Running feature extraction...\n")
    subprocess.run(["python", FEATURE_EXTRACTION_SCRIPT], check=True)
    print("\n✅ Feature extraction completed.\n")

def run_human_match():
    """Runs the human-to-animal matching script for all images in 'image_to_upload/'."""
    valid_extensions = (".jpg", ".jpeg", ".png")
    human_images = [f for f in os.listdir(IMAGE_UPLOAD_DIR) if f.lower().endswith(valid_extensions)]

    if not human_images:
        print("\n🚫 No human images found in 'image_to_upload/'. Please add images and retry.")
        return

    print("\n🔍 Running human-to-animal matching for uploaded images...\n")
    for filename in human_images:
        image_path = os.path.join(IMAGE_UPLOAD_DIR, filename)
        print(f"📸 Processing: {filename}")
        subprocess.run(["python", HUMAN_MATCH_SCRIPT, image_path], check=True)

def main():
    print("\n🚀 Starting AI Model Processing Pipeline\n")

    # Ask user if they want to run feature extraction
    run_extraction = input("Do you want to run feature extraction? (yes/no): ").strip().lower()
    if run_extraction == 'yes':
        # Step 1: Extract Features
        run_feature_extraction()
    else:
        print("\n⏭️ Skipping feature extraction.\n")

    # Step 2: Match Human Image to Animals
    run_human_match()

if __name__ == "__main__":
    main()
