import os
import requests
import subprocess
import shutil
import zipfile
from pathlib import Path

# Configuration
FONT_SIZES = [5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 48, 56, 64]
OUTPUT_DIR = Path("fonts")
TTF_DIR = OUTPUT_DIR / "ttf"
BDF_DIR = OUTPUT_DIR / "bdf"
C_DIR = OUTPUT_DIR / "c"
UNICODE_RANGE = "32-255,160-383,7680-7935"  # Covers Vietnamese Unicode characters


def setup_directories():
    """Create output directories."""
    for dir_path in [TTF_DIR, BDF_DIR, C_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)

def is_valid_ttf(file_path):
    """Check if a file is a valid TTF by verifying its magic number."""
    try:
        with open(file_path, "rb") as f:
            header = f.read(4)
            # TTF files start with 0x00 0x01 0x00 0x00
            return header == b"\x00\x01\x00\x00" or header == b"\x4F\x54\x54\x4F"
    except Exception as e:
        print(f"Error checking TTF validity for {file_path}: {e}")
        return False

def convert_ttf_to_bdf(ttf_path, font_name, size):
    """Convert TTF to BDF using otf2bdf."""
    font_name = font_name.replace(" ", "_").replace("-", "_").lower()  # Normalize font name
    font_name, font_style = font_name.split("_")  # Normalize font name
    bdf_path = BDF_DIR / f"{font_name}/{font_name}_{font_style}_{size}pt.bdf"
    bdf_dir = BDF_DIR / f"{font_name}"
    if not os.path.exists(bdf_dir):
        os.makedirs(bdf_dir, exist_ok=True)
    
    # Verify TTF exists and is readable
    if not ttf_path.exists():
        print(f"TTF file {ttf_path} does not exist for {font_name} at {size}pt")
        return None
    if not os.access(ttf_path, os.R_OK):
        print(f"TTF file {ttf_path} is not readable for {font_name} at {size}pt")
        return None
    if not is_valid_ttf(ttf_path):
        print(f"TTF file {ttf_path} is not a valid TTF for {font_name} at {size}pt")
        return None
    
    cmd = [
        "otf2bdf",
        "-p", str(size),
        "-n", str(ttf_path),
        "-o", str(bdf_path)
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Converted {font_name} at {size}pt to BDF")
        print(bdf_path)
        return bdf_path
    except Exception as e:
        print(f"Error converting {font_name} at {size}pt: {e.stderr}")
        return None

def convert_bdf_to_c(bdf_path, font_name, size):
    """Convert BDF to u8g2 C array using bdfconv."""
    font_name = font_name.replace(" ", "").lower()  # Normalize font name
    font_name, font_style = font_name.split("_")  # Normalize font name
    c_path = C_DIR / f"{font_name}/u8g2_font_{font_name}_{font_style}_{size}pt.c"
    c_dir = C_DIR / f"{font_name}"
    if not os.path.exists(c_dir):
        os.makedirs(c_dir, exist_ok=True)
    font_identifier = f"u8g2_font_{font_name}_{size}pt"
    cmd = [
        "bdfconv",
        "-v",
        "-f", "1",
        "-m", UNICODE_RANGE,
        "-n", font_identifier,
        "-o", str(c_path),
        str(bdf_path)
    ]
    # print("Command:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Generated C array for {font_name} at {size}pt")
        return c_path
    except subprocess.CalledProcessError as e:
        print(f"Error converting {font_name} at {size}pt to C: {e.stderr}")
        return None

def main():
    setup_directories()
    
    for path in os.listdir(TTF_DIR):
        print(f"Processing {path}...")
        font_name = path.split(".")[0].lower().replace(" ", "_").replace("-", "_")
        if path.endswith(".ttf") or path.endswith(".otf"):
            ttf_path = TTF_DIR / path
            if not is_valid_ttf(ttf_path):
                print(f"Invalid TTF file: {ttf_path}")
                continue
            
            # Convert for each size
            for size in FONT_SIZES:
                bdf_path = convert_ttf_to_bdf(ttf_path, font_name, size)
                if not bdf_path:
                    continue
                
                c_path = convert_bdf_to_c(bdf_path, font_name, size)
                if c_path:
                    print(f"Completed processing for {font_name} at {size}pt")
    
if __name__ == "__main__":
    main()