import requests
import zipfile
import os

url = "https://cricsheet.org/downloads/all_json.zip"
raw_dir = "data/raw"
zip_path = os.path.join(raw_dir, "all_json.zip")

os.makedirs(raw_dir, exist_ok=True)

print("Downloading dataset...")
r = requests.get(url)

with open(zip_path, "wb") as f:
    f.write(r.content)

print("Download complete.")

print("Extracting files...")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(raw_dir)

print("Extraction complete.")
