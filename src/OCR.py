#pip install PyMuPDF
import fitz  # PyMuPDF, needs to be installed first: pip install PyMuPDF
from PIL import Image
import io
import os

# Set the PDF path and output image directory
pdf_path = "/Users/yangzhendong/Downloads/Amazon.com.pdf"
output_folder = "/Users/yangzhendong/Downloads/pdf_images"
os.makedirs(output_folder, exist_ok=True)

# Open the PDF file
doc = fitz.open(pdf_path)

# Iterate through each page and convert it to an image
for i in range(len(doc)):
    page = doc.load_page(i)  # Load page i
    # Set the DPI value, for example, 300 DPI
    zoom = 300 / 72  # 72 is the default DPI
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # Save as a PNG image
    image_path = os.path.join(output_folder, f"page_{i+1}.png")
    pix.save(image_path)
    print(f"Saved {image_path}")

    image_data = pix.tobytes("png")
    pil_image = Image.open(io.BytesIO(image_data))

#pip install easyocr
#pip install pillow

import easyocr
from PIL import Image
import os

# Initialize the OCR reader, use ['en'] for English only, or ['ch_sim', 'en'] for mixed Chinese and English
reader = easyocr.Reader(['en'])

# Paths to your images
image_paths = [
    "/Users/yangzhendong/Downloads/pdf_images/page_1.png",
    "/Users/yangzhendong/Downloads/pdf_images/page_2.png"
]

all_text = ""

for i, image_path in enumerate(image_paths):
    # Perform OCR recognition
    results = reader.readtext(image_path)
    # Concatenate the results
    page_text = "\n".join([res[1] for res in results])
    
    all_text += f"\n--- Page {i+1} ---\n{page_text}\n"
    print(f"Page {i+1} text recognition completed")

print(all_text)

output_txt_path = "/Users/yangzhendong/Downloads/extracted_text_easyocr.txt"
with open(output_txt_path, "w", encoding="utf-8") as f:
    f.write(all_text)

print(f"Recognition results have been saved to {output_txt_path}")

