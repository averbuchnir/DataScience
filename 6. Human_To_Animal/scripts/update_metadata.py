import os
import json

# Path to metadata file
metadata_file = "downloaded_images/metadata.json"

def update_metadata():
    """
    Removes references to deleted images in metadata.json.
    This function checks the metadata.json file for references to images that no longer exist
    in the specified directories. It updates the metadata by removing entries for missing images
    and saves the cleaned metadata back to the metadata.json file.
    Steps:
    1. Check if the metadata.json file exists. If not, print a message and exit.
    2. Load the metadata from the metadata.json file.
    3. Iterate through each animal category in the metadata.
    4. For each image in the category, check if the image file exists.
    5. If the image file exists, keep the reference in the updated metadata.
       Otherwise, print a message indicating the missing image and remove its reference.
    6. Save the updated metadata back to the metadata.json file.
    Raises:
        FileNotFoundError: If the metadata.json file does not exist.
    Prints:
        Messages indicating the removal of missing images and the successful update of metadata.
    """
    """Removes references to deleted images in metadata.json."""
    
    if not os.path.exists(metadata_file):
        print("No metadata.json found. Exiting.")
        return
    
    # Load metadata
    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    updated_metadata = {}

    # Iterate through each animal category
    for animal, image_list in metadata.items():
        storage_dir = os.path.join("downloaded_images", animal)
        updated_metadata[animal] = []

        for image_data in image_list:
            image_path = image_data["path"]
            
            # Keep only existing images
            if os.path.exists(image_path):
                updated_metadata[animal].append(image_data)
            else:
                print(f"Removing missing image from metadata: {image_path}")

    # Save cleaned metadata
    with open(metadata_file, "w") as f:
        json.dump(updated_metadata, f, indent=4)

    print("Metadata updated successfully.")

if __name__ == "__main__":
    update_metadata()
