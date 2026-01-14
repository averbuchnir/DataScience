from pathlib import Path
from urllib.parse import quote
import requests
from PIL import Image
from ..utils import get_current_time_display


def save_board_png(fen: str, filename: str):
    """
    Save a PNG image of the board for the given FEN and filename.
    Uses chessvision.ai fen2image API: https://fen2image.chessvision.ai/
    """
    # URL-encode the FEN string for the API
    fen_encoded = quote(fen, safe="")
    
    # Construct the API URL - format: https://fen2image.chessvision.ai/{encoded_fen}
    base_url = "https://fen2image.chessvision.ai/"
    url = f"{base_url}{fen_encoded}"

    # Fetch the image
    r = requests.get(url, timeout=10, headers={"Accept": "image/png"})
    r.raise_for_status()

    # Verify we got an image
    ct = r.headers.get("Content-Type", "")
    if "image" not in ct.lower():
        raise ValueError(f"Not an image (got {ct}). URL was: {url}\nResponse: {r.text[:200]}")

    # Ensure the directory exists
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    
    # Save the image
    with open(filename, "wb") as f:
        f.write(r.content)


def frame_to_gif(frame_dir, output_gif, fps=10):
    """"
    Convert a directory of PNG frames into a GIF animation.
    frame_dir: directory containing the PNG frames
    output_gif: filename of the output GIF
    fps: frames per second
    """
    frames = sorted(Path(frame_dir).glob("*.png"))
    if not frames:
        raise ValueError(f"No frames found in {frame_dir}")
    
    images = [Image.open(frame) for frame in frames]
    # 2 seconds per frame
    duration = 5000 / fps # milliseconds per frame -> 2 seconds per frame

    Path(output_gif).parent.mkdir(parents=True, exist_ok=True)
    images[0].save(
        output_gif,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
        disposal=2, # background disposal
        optimize=True,
        quality=100,
    )
    print(f"{get_current_time_display()} - GIF animation saved to {output_gif}")