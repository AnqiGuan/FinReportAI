import os
import re
import fitz
import pytesseract
from PIL import Image
import pandas as pd

# PDF -> Images
def pdf_to_images(pdf_path, output_folder):
    """
    Convert each page of the PDF to a PNG image at ~300 DPI,
    saving images into 'output_folder'.
    """
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        page = doc.load_page(i)
        zoom = 300 / 72
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        pix.save(image_path)
        print(f"Saved {image_path}")

# OCR each image
def ocr_folder_images(folder_path, lang='eng'):
    """
    For all image files in 'folder_path', run Tesseract OCR (lang=eng).
    Return the combined text from all images.
    """
    combined_text = ""
    image_exts = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp')
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith(image_exts):
            image_path = os.path.join(folder_path, filename)
            print(f"OCR on: {filename}")
            text = pytesseract.image_to_string(Image.open(image_path), lang=lang)
            combined_text += f"Results for {filename}:\n{text}\n\n"
    return combined_text

# Auto-detect date columns
def detect_date_columns(lines):
    """
    Go through all lines, find the line that has the MOST date substrings (regex-based).
    Extract and return those date substrings as a list (maintaining order, removing duplicates).
    
    Regex: find patterns like 'MM/DD/YYYY' or 'M/D/YYYY'. 
    Adjust if your data might have different formats (e.g., 2024/12/31).
    """
    date_pattern = r"\d{1,2}/\d{1,2}/\d{4}"
    
    best_line = ""
    best_count = 0
    best_dates = []

    for line in lines:
        found = re.findall(date_pattern, line)
        if len(found) > best_count:
            best_count = len(found)
            best_line = line
            best_dates = found

    seen = set()
    unique_dates = []
    for d in best_dates:
        if d not in seen:
            seen.add(d)
            unique_dates.append(d)

    return unique_dates

# Extract field values
def extract_field_values(lines, date_columns, fields):
    """
    For each field in 'fields' dict, search the lines for that field name.
    Extract all numeric patterns from that line. Then align them with the date_columns.

    fields = {
       "Total Assets": [],
       "Total Liabilities": [],
       ...
    }

    Return an updated dictionary where each field has a list of len(date_columns) numeric values (or None).
    """
    for field in fields.keys():
        fields[field] = [None] * len(date_columns) 

        for i, line in enumerate(lines):
            if field.lower() in line.lower():
                numbers = re.findall(r"-?\d{1,3}(?:,\d{3})*", line)
                num_list = []
                for n in numbers:
                    clean_n = n.replace(",", "")
                    try:
                        num_list.append(int(clean_n))
                    except ValueError:
                        pass

                for idx in range(min(len(num_list), len(date_columns))):
                    fields[field][idx] = num_list[idx]
                break

    return fields

# Main Flow
def main():
    pdf_path = "uploads/financial_report.pdf"
    output_folder = "outputs"
    txt_path = os.path.join(output_folder, "extracted_text.txt")
    csv_path = os.path.join(output_folder, "financial_data.csv")

    pdf_to_images(pdf_path, output_folder=output_folder)
    extracted_text = ocr_folder_images(output_folder, lang='eng')

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    print(f"OCR extraction completed. Results saved to {txt_path}")

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    date_columns = detect_date_columns(lines)

    fields = {
        "Total Assets": [],
        "Total Liabilities": [],
        "Total Equity": [],
        "Total Capitalization": [],
        "Common Stock Equity": [],
        "Capital Lease Obligations": [],
        "Net Tangible Assets": [],
        "Working Capital": [],
        "Invested Capital": [],
        "Tangible Book Value": [],
        "Total Debt": [],
        "Net Debt": [],
        "Share Issued": [],
        "Ordinary Shares Number": [],
        "Treasury Shares Number": []
    }

    fields = extract_field_values(lines, date_columns, fields)

    data = {"Date": date_columns}
    data.update(fields)
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Final CSV saved to: {csv_path}")


if __name__ == "__main__":
    main()
