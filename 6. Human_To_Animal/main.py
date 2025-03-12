import os
import json
from scripts.image_scraper_multi_lan import download_images, load_metadata, save_metadata
from scripts.filter_human import clean_human_faces
from scripts.update_metadata import update_metadata
from scripts.augmentation_standardization import run_augmentation


# Load config
with open("config.json", "r") as config_file:
    config = json.load(config_file)

ANIMALS = config["animals"]
METADATA_FILE = config["metadata_file"]

# Ensure metadata directory exists
os.makedirs("downloaded_images", exist_ok=True)

# Check if images exist before proceeding
def check_existing_images():
    existing_folders = [animal for animal in ANIMALS if os.path.exists(os.path.join("downloaded_images", animal.replace(" ", "_")))]
    if existing_folders:
        user_input = input(f"Images for {', '.join(existing_folders)} already exist. Continue downloading? (y/n): ")
        if user_input.lower() != 'y':
            print("🚫 Download process aborted.")
            return False
    return True

# Main function
def main():
    metadata = load_metadata()

    if check_existing_images():
        print("🔍 Downloading images...")
        for animal in ANIMALS:
            download_images(animal, metadata)
        save_metadata(metadata)
        print("✅ Image downloading complete.")
    else:
        print("⏩ Skipping image downloading.....there should be enough images to proceed.")

    # Ask user if they want to remove human images
    user_input = input("Press 'y' to delete all humans from images: ")
    if user_input.lower() == 'y':
        print("🗑 Deleting all human faces from images...")
        clean_human_faces(METADATA_FILE)
        print("✅ Updated metadata with human faces removed")
        update_metadata()
    else:
        print("⏩ Skipping human face deletion.")
        # Run augmentation and standardization

    print("🎨 Starting image augmentation and standardization...")
    run_augmentation()



if __name__ == "__main__":
    main()
