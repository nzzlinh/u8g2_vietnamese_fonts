import os
from pathlib import Path
from bdfparser import Font
from PIL import Image, ImageDraw

# Define the Vietnamese accented characters string
VIETNAMESE_CHARS = (
    "aàáảãạăằắẳẵặâầấẩẫậ\n"
    "AÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬ\n"
    "eèéẻẽẹêềếểễệ\n"
    "EÈÉẺẼẸÊỀẾỂỄỆ\n"
    "iìíỉĩị\n"
    "IÌÍỈĨỊ\n"
    "oòóỏõọôồốổỗộơờớởỡợ\n"
    "OÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ\n"
    "uùúủũụưừứửữự\n"
    "UÙÚỨŨỤƯỪỨỬỮỰ\n"
    "yỳýỷỹỵ\n"
    "YỲÝỶỸỴ\n"
)

# Test string combining Vietnamese characters with a sample text
TEST_STRING = f"{VIETNAMESE_CHARS}\nCon cò bé bé nó đậu cành tre, đi không hỏi mẹ biết đi đường nào?"

def load_bdf_font(font_path):
    """Load a BDF font file using bdfparser and return the font object."""
    try:
        font = Font(str(font_path))
        return font
    except Exception as e:
        raise Exception(f"Failed to load font {font_path}: {str(e)}")

def render_font_to_image(font, text, output_path):
    """Render the given text using the BDF font to an image."""
    font_preview = font.draw(text)
    image = Image.frombytes('1',
                            (font_preview.width(), font_preview.height()),
                            font_preview.tobytes('1'))
    
    # Save the image
    image.save(output_path, "PNG")

def main():
    # Directories
    font_dir = Path("fonts/bdf")
    output_dir = Path("images")
    output_dir.mkdir(exist_ok=True)
    
    font_files = [f for f in font_dir.glob("**/*.bdf") if "_24pt" in f.name]
    
    # List to store font info for README
    font_info = []
    
    # Generate table of contents
    toc = []
    
    # Process each font
    for font_path in font_files:
        font_name = font_path.stem
        print(f"Processing {font_name}...")
        
        try:
            # Load the font
            font = load_bdf_font(font_path)
            
            # Generate output image path
            output_image = output_dir / f"{font_name}.png"
            
            # Render the font to an image
            render_font_to_image(font, TEST_STRING, output_image)
            
            # Store font info
            font_info.append((font_name, output_image.name))
        
        except Exception as e:
            print(f"Error processing {font_name}: {e}")
            continue
    
    # Generate README.md
    readme_content = "# U8G2 Vietnamese Fonts\n\n"
    readme_content += "This repository contains pre-made Vietnamese fonts to be used with U8G2 library.\n\n"
    readme_content += "Welcome friends' contribution for free fonts and improvement =)\n\n"
    readme_content += "Each font supports these sizes: 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 48, 56, 64.\n\n"
    readme_content += """Used tools:\n
 - otf2bdf: 
    ```
    sudo apt-get install otf2bdf
    ```
 - bdfconv: https://github.com/olikraus/u8g2/tree/master/tools/font/bdfconv\n\n"""
 
    readme_content += "## Font Preview (24pt version only)\n\n"
    
    body_content = ""
    for font_name, image_name in font_info:
        body_content += f"### {font_name}\n\n"
        toc.append(f" - [{font_name}](#{font_name})")
        body_content += f"![{font_name}](output/{image_name})\n\n"
    
    readme_content += "\n".join(toc) + "\n\n"
    readme_content += body_content
    
    # Write README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("README.md generated successfully.")

if __name__ == "__main__":
    main()