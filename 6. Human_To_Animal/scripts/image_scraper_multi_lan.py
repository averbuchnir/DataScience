import os
import json
import time
import logging
import random
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler

# Load configuration
with open("config.json", "r") as config_file:
    config = json.load(config_file)

ANIMALS = config["animals"]
SEARCH_QUERIES = config["search_queries"]
MAX_IMAGES = config["max_images"]
METADATA_FILE = config["metadata_file"]

# Configure logging
os.makedirs("log", exist_ok=True)
logging.basicConfig(
    filename="log/image_download_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ensure metadata directory exists
os.makedirs("downloaded_images", exist_ok=True)

# Load existing metadata
def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    return {}

# Save metadata
def save_metadata(metadata):
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)

# Image downloading function
def download_images(animal, metadata):
    """Downloads images for a given animal category."""
    try:
        print(f"📥 Downloading images for: {animal}")
        storage_dir = os.path.join('downloaded_images', animal.replace(" ", "_"))
        os.makedirs(storage_dir, exist_ok=True)

        crawlers = {
            "Google": GoogleImageCrawler(storage={'root_dir': storage_dir}),
            "Bing": BingImageCrawler(storage={'root_dir': storage_dir}),
        }

        existing_files = set(os.listdir(storage_dir))  # Track existing images

        for source, crawler in crawlers.items():
            try:
                print(f"🌍 Fetching from {source}...")

                downloaded_count = 0

                for query in SEARCH_QUERIES[source]:
                    if downloaded_count >= MAX_IMAGES // len(crawlers):
                        break

                    retry_count = 3
                    while retry_count > 0:
                        try:
                            before_download = set(os.listdir(storage_dir))

                            crawler.crawl(
                                keyword=f"{animal} {query}",
                                max_num=150,
                                overwrite=False
                            )

                            after_download = set(os.listdir(storage_dir))
                            new_files = after_download - before_download
                            downloaded_count += len(new_files)

                            print(f"📸 Downloaded {len(new_files)} images for {animal} from {source}. Total: {downloaded_count}")

                            if len(new_files) == 0:
                                delay_time = random.uniform(15, 30)
                                print(f"⏳ No new images detected. Waiting {delay_time:.2f} seconds...")
                                time.sleep(delay_time)

                            break
                        except Exception as e:
                            print(f"⚠ {source} failed, retrying... ({3 - retry_count}/3)")
                            retry_count -= 1
                            sleep_time = random.uniform(10, 20)
                            print(f"🕒 Waiting {sleep_time:.2f} seconds before retrying...")
                            time.sleep(sleep_time)

                final_image_count = len(os.listdir(storage_dir)) - len(existing_files)
                if final_image_count < MAX_IMAGES // len(crawlers):
                    print(f"⚠ Warning: {source} stopped early after {final_image_count} new images.")

                print(f"✅ Finished downloading {animal} from {source} (New images: {final_image_count})")
                time.sleep(random.uniform(10, 25))

                if animal not in metadata:
                    metadata[animal] = []

                for filename in os.listdir(storage_dir):
                    file_path = os.path.join(storage_dir, filename)
                    if os.path.isfile(file_path) and filename not in existing_files:
                        metadata[animal].append({
                            "filename": filename,
                            "source": source,
                            "path": file_path
                        })

            except Exception as e:
                logging.error(f"❌ Error downloading {animal} from {source}: {e}")

    except Exception as e:
        logging.error(f"❌ Error processing {animal}: {e}")
