import requests
import urllib.parse
import json
import os
from config import GENERATOR_BASE


def download_qr_image(short_url, code_design_config, business_name, output_dir, image_type="png", width=300):
    # Flatten and URL-encode the design config
    config_str = json.dumps(code_design_config, separators=(",", ":"))
    encoded_opts = urllib.parse.quote(config_str)
    encoded_data = urllib.parse.quote(short_url)

    url = f"{GENERATOR_BASE}?data={encoded_data}&imageType={image_type}&width={width}&opts={encoded_opts}"

    response = requests.get(url)
    response.raise_for_status()

    # Sanitize filename
    safe_name = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in business_name).strip()
    filename = os.path.join(output_dir, f"{safe_name}.{image_type}")

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename


def demo_save_placeholder(business_name, output_dir, image_type="png"):
    """In demo mode, saves a text placeholder instead of a real image."""
    safe_name = "".join(c if c.isalnum() or c in (" ", "-", "_") else "_" for c in business_name).strip()
    filename = os.path.join(output_dir, f"{safe_name}.txt")
    with open(filename, "w") as f:
        f.write(f"[DEMO] QR code placeholder for: {business_name}\n")
        f.write("Replace with real image when using live API credentials.\n")
    return filename
