import os
from pathlib import Path
from bdfparser import Font
from PIL import Image, ImageDraw

README_HEADER = """
# U8G2 Vietnamese Fonts

Bộ font miễn phí hỗ trợ các ký tự Tiếng Việt tương thích với thư viện U8G2.

This repository contains pre-made Vietnamese fonts to be used with U8G2 library.

## Cách dùng

Anh em có thể copy font cần dùng trong folder `fonts/c/` vào project của anh em. Sau đó, trong source code chính (eg. main.c) cần khai báo extern cho font.

Ví dụ, tôi cần dùng font u8g2_font_arial_5pt. Tôi sẽ copy file `fonts/c/arial/u8g2_font_arial_regular_5pt.c` vào project của tôi. Sau đó, trong main.c, khai báo extern:

```c
extern const uint8_t u8g2_font_arial_5pt[3652] U8G2_FONT_SECTION("u8g2_font_arial_5pt");
```

Và cuối cùng, thì pass `u8g2_font_arial_5pt` vào các hàm của thư viện u8g2 để dùng thôi.

**Thông tin thêm**:
 - Để dùng bộ font này với Adafruit_GFX thì anh em cần sử dụng thêm bộ thư viện sau:
https://github.com/olikraus/U8g2_for_Adafruit_GFX
 - Hỗ trợ kích thước font: 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 48, 56, 64.
 - **Repository này bao gồm các phông chữ miễn phí (tôi nghĩ vậy). Nếu có bất kỳ vi phạm bản quyền nào, vui lòng thông báo cho tôi, và tôi sẽ xóa nó càng sớm càng tốt.**

#### Cách đóng góp

Chào đón mọi sự đóng góp của anh em! Anh em có thể đóng góp thêm các bộ font Tiếng Việt **miễn phí** mà anh em biết. Hạy tạo 1 branch và PR mới, đặt font (định dạng .ttf) vào folder `fonts/ttf`. Sau đó, chạy script `python3 ./scripts/make.py`. 

**Lưu ý**
 - Anh em nên rename tên font thành định dạng sau "{font_name}_{font_style}.ttf". `font_style` bao gồm: bold, italic, regular, etc (nếu không rõ font style thì anh em để none)

## Usage

You can copy the required font from the `fonts/c/` folder into your project. Then, in the main source code (e.g., `main.c`), you need to declare the font as `extern`.

For example, if I need to use the font `u8g2_font_arial_5pt`, I will copy the file `fonts/c/arial/u8g2_font_arial_regular_5pt.c` into my project. Then, in `main.c`, declare it as `extern`:

```c
extern const uint8_t u8g2_font_arial_5pt[3652] U8G2_FONT_SECTION("u8g2_font_arial_5pt");
```

Finally, pass u8g2_font_arial_5pt into the functions of the U8g2 library to use it.

**Additional Information**:
- To use this font collection with Adafruit_GFX, you need to include the following library: https://github.com/olikraus/U8g2_for_Adafruit_GFX
- Supported font sizes: 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 48, 56, 64.
- **This repository includes free fonts (or so I believe). If there is any copyright infringement, please notify me, and I will remove it as soon as possible.**

#### How to contribute

Contributions are welcome! You can add more free Vietnamese fonts that you know. Create a new branch and submit a pull request (PR), placing the font file (in .ttf format) into the fonts/ttf folder. Then, run the script:

```bash
python3 ./scripts/make.py
```

**Note**:
- Please rename the font using the following format: {font_name}_{font_style}.ttf 
- Font styles include: bold, italic, regular, etc. (if you dont know the font style exactly, let it to be none)

## Used tools:

 - otf2bdf: 
    ```
    sudo apt-get install otf2bdf
    ```
 - bdfconv: https://github.com/olikraus/u8g2/tree/master/tools/font/bdfconv
"""

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
    readme_content = README_HEADER + "\n\n"
    readme_content += "## Font Preview (24pt version only)\n\n"
    
    body_content = ""
    processed_fonts = []
    for font_name, image_name in font_info:
        full_font_name = font_name
        if len(font_name.split("_")) > 1:
            font_name, font_style = font_name.split("_")[0], font_name.split("_")[1]
        else:
            font_style = "regular"
        if not (font_name in processed_fonts):
            body_content += f"------------------\n### {font_name}\n\n"
            toc.append(f"\n - [{font_name}](#{font_name}) - ")
            processed_fonts.append(font_name)
            toc.append(f" | [{font_style}](#{font_name})  ")
        else:
            body_content += f"#### {full_font_name}\n\n"
            toc.append(f" | [{font_style}](#{full_font_name})  ")
        body_content += f"![{font_name}]({output_dir}/{image_name})\n\n"
    
    readme_content += "".join(toc) + "\n\n"
    readme_content += body_content
    
    # Write README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("README.md generated successfully.")

if __name__ == "__main__":
    main()