from pdf2image import convert_from_path
import os

# import pdf file
pdf_path = 'financial_report.pdf'
output_folder = 'output_images'
os.makedirs(output_folder, exist_ok=True)

# convert pdf to images
pages = convert_from_path(pdf_path, dpi=300)
for i, page in enumerate(pages):
    image_path = os.path.join(output_folder, f'page_{i+1}.jpg')
    page.save(image_path, 'JPEG')
    print(f'Saved {image_path}')
