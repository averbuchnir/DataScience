import cv2
import os
import json
from concurrent.futures import ThreadPoolExecutor

# Load OpenCV's Deep Neural Network (DNN) face detector
FACE_NET = cv2.dnn.readNetFromCaffe(
    "human_model/deploy.prototxt",
    "human_model/res10_300x300_ssd_iter_140000.caffemodel"
)

# Confidence threshold for detecting human faces
FACE_CONFIDENCE_THRESHOLD = 0.6  

def detect_human_faces(image_path):
    """Detects human faces in an image. Returns True if a human is detected."""
    image = cv2.imread(image_path)
    if image is None:
        return False  # Skip unreadable images

    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))

    FACE_NET.setInput(blob)
    detections = FACE_NET.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > FACE_CONFIDENCE_THRESHOLD:
            return True  # Human face detected

    return False

def clean_human_faces(metadata_file="downloaded_images/metadata.json"):
    """Iterates over downloaded images, deletes those with human faces, and updates metadata."""
    
    # Load metadata if it exists
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
    else:
        print("No metadata found. Exiting filtering process.")
        return

    for animal, image_list in metadata.items():
        storage_dir = os.path.join("downloaded_images", animal)
        if not os.path.exists(storage_dir):
            continue

        images_to_keep = []

        for image_data in image_list:
            image_path = image_data["path"]

            if os.path.isfile(image_path) and detect_human_faces(image_path):
                os.remove(image_path)  # Delete human images
                print(f"Deleted human image: {image_path}")
            else:
                images_to_keep.append(image_data)  # Keep valid images

        # Update metadata after deletion
        metadata[animal] = images_to_keep

    # Save the updated metadata
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=4)

    print("Human face filtering complete.")

if __name__ == "__main__":
    clean_human_faces()
