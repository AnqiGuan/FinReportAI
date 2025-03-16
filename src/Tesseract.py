import fitz
from PIL import Image
import os
import pytesseract

# ----------------------------
# PDF to Image Conversion
# ----------------------------
# Set the PDF file path and the output image directory
pdf_path = "uploads/financial_report.pdf"
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

# Open the PDF file using PyMuPDF
doc = fitz.open(pdf_path)

# Iterate through each page in the PDF and convert it to an image
for i in range(len(doc)):
    page = doc.load_page(i)  # Load page number i
    # Set the DPI: default DPI is 72, so scale for 300 DPI
    zoom = 300 / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # Save the page as a PNG image
    image_path = os.path.join(output_folder, f"page_{i+1}.png")
    pix.save(image_path)
    print(f"Saved {image_path}")

# ----------------------------
# OCR with Tesseract
# ----------------------------
def ocr_image(image_path):
    """
    Open an image and perform OCR using Tesseract.
    """
    image = Image.open(image_path)
    # Perform OCR using Tesseract; change 'eng' to 'chi_sim' for Chinese recognition if needed
    text = pytesseract.image_to_string(image, lang='eng')
    return text

def process_folder(folder_path):
    """
    Process all supported image files in the specified folder,
    perform OCR on each, and combine the extracted text.
    """
    combined_text = ""
    # Process images in sorted order (by filename)
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing image: {filename}")
            text = ocr_image(image_path)
            combined_text += f"Results for {filename}:\n{text}\n\n"
    return combined_text

# Process the output folder images and write OCR results to a text file
extracted_text = process_folder(output_folder)
output_file = "extracted_text.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(extracted_text)

print(f"OCR extraction completed. Results saved to {output_file}")
