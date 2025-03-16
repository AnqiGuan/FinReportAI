# FinReportAI - Infinity AI

## App Description

**FinReportAI** is an on-device AI-powered financial report analysis tool designed for non-financial professionals. It extracts key data from lengthy financial reports using OCR, processes and visualizes the data, and generates an easy-to-understand financial analysis report using NLP and a local language model. This enables users to receive personalized financial insights and investment advice without needing extensive financial expertise.

## Developers

- **Anqi Guan**  
  - LinkedIn: https://www.linkedin.com/in/anqi-g-a2108b24b/
  - Email: anqi.guan@outlook.com

- **Zhendong Yang**  
  - LinkedIn: https://www.linkedin.com/in/zhendong-aaron-yang-98667b290/
  - Email: yang.zhend@northeastern.edu

- **Jing Du**  
  - LinkedIn: https://www.linkedin.com/in/du-jing2-northeastern-edu/
  - Email: du.jing2@northeastern.edu

- **Sicheng Zhou**  
  - LinkedIn: https://www.linkedin.com/in/sicheng-zhou-81419758/ 
  - Email: zhou.sich@northeastern.edu

- **Rui Min**  
  - LinkedIn: https://www.linkedin.com/in/ryanmin55
  - Email: min.rui1@northeastern.edu
  

## Features

- **PDF to Image Conversion:**  
  Uses `pdf2image` and `PyMuPDF` (fitz) to convert PDF pages to high-resolution PNG images.

- **OCR Processing:**  
  Uses Tesseract OCR (via `pytesseract` and `Pillow`) to extract text from images.

- **Data Extraction & Parsing:**  
  Processes the OCR output to detect date columns, extract financial field values, and capture company information.

- **Data Analysis & Visualization:**  
  Uses `pandas`, `matplotlib`, and `seaborn` to analyze financial data and generate visualizations.

- **Report Generation:**  
  Utilizes a language model (via `llama-cpp-python` or Hugging Face's `transformers` pipeline) to generate a comprehensive financial report.

- **Web UI:**  
  A simple Flask-based file upload interface for users to upload PDFs and trigger processing.

## Installation

### Prerequisites

- Python 3.8 or later
- Tesseract OCR installed and added to your system's PATH  
  - **Windows:** [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)  
  - **macOS:** `brew install tesseract`  
  - **Linux:** `sudo apt-get install tesseract-ocr`

### Setup Instructions

To set up the project from scratch, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/YourGitHubUsername/FinReportAI.git
   cd FinReportAI
   ```

2. **Create a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On macOS/Linux
   venv\Scripts\activate       # On Windows
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirementss
   ```

   *Note: The `requirements.txt` file includes dependencies such as `pdf2image`, `numpy`, `pillow`, `matplotlib`, `seaborn`, `pytesseract`, `pandas`, `flask`, `transformers`, `torch`, and the appropriate LLM package (e.g., `llama-cpp-python`).*

  Or Install the required Python packages by running:

    ```bash
    pip install pdf2image numpy pillow matplotlib llama-cpp-python pytesseract pandas flask seaborn transformers torch subprocess markdown2
    ```

> **Note:** If you encounter issues installing `llama_cpp` or if you need a version that doesn't require AVX, consider using `llama-cpp-python` instead (see its [GitHub repository](https://github.com/abetlen/llama-cpp-python) for more details).

4. **Set Up Tesseract:**

   - **Windows:** Download and install Tesseract OCR from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and add it to your PATH.
   - **macOS:** Install via Homebrew:
     ```bash
     brew install tesseract
     ```
   - **Linux:** Install via package manager:
     ```bash
     sudo apt-get install tesseract-ocr
     ```

5. **Configure the Application:**

   - Place your financial report PDF in the `src/uploads` folder.
   - Ensure that the `outputs` folder exists (the application will create it automatically if it doesn't).

## Project Structure

```
your_project/
├── src/                     
│   ├── app.py                   # Flask file upload UI and main application
│   ├── advice_pipeline.py                   # Generate a financial advice report
│   ├── ocr_pipeline.py             # PDF-to-image conversion, OCR extraction, and parsing OCR text into financial_data.csv
│   ├── visualization_pipeline.py # Visualization and analysis of financial data (e.g., plotting trends)
│   ├── report_pipeline.py       # Generate a comprehensive financial analysis report using an LLM
│   ├── outputs/                 # Automatically generated output files:
│   │   ├── extracted_text.txt   # OCR results
│   │   ├── financial_data.csv   # Parsed financial data CSV
│   │   ├── analysis_report.txt  # Generated financial analysis report
|   |   └── advice_report.txt    # Generated financial advice report
│   └── uploads/                 # Directory for uploaded PDF files
├── examples/                    # Example scripts or notebooks for testing/experiments
└── README.md                    # This file

```

## Usage

### 1. Run the Web UI for File Upload
1. Open a terminal and navigate to the source folder:
   ```bash
   cd src
   ```
2. Run the Flask application:
   ```bash
   python app.py
   ```
3. In your browser, go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) and upload your `financial_report.pdf` file from the **examples** folder.  

### 2. Convert PDF to Images & Parse OCR Data into CSV
To run the OCR pipeline:
1. Place your `financial_report.pdf` in the `uploads` folder.
2. From the `src` folder, run:
   ```bash
   python ocr_pipeline.py
   ```
   This script will:
   - Convert the PDF from the `uploads/financial_report.pdf` into PNG images stored in the `outputs/` folder.
   - Apply Tesseract OCR on each image and save the combined text to `outputs/extracted_text.txt`.
   - Read `outputs/extracted_text.txt`, detect date columns and extract financial fields (and company name), then write the parsed data into `outputs/financial_data.csv`.

### 3. Generate the Financial Analysis and Advice Report
To generate a report based on the parsed CSV:
1. From the `src` folder, run:
   ```bash
   python report_pipeline.py
   python advice_pipeline.py
   python visualization_pipeline.py
   ```
2. The script will load `outputs/financial_data.csv`, construct a prompt, and use the offline language model to generate a detailed financial analysis report.
3. The final report is saved as `outputs/analysis_report.txt` and `outputs/advice_report.txt`.

## Customization

- **OCR Preprocessing:**  
  You can adjust the image preprocessing in the OCR script to improve recognition accuracy.

- **Parsing Logic:**  
  Modify the regex patterns in the parsing scripts if your OCR output format changes.

- **Model & Prompt:**  
  Adjust the prompt for the language model to fit your desired report style. If using a different LLM, update the model loading code accordingly.

## Troubleshooting

- **Tesseract Not Found:**  
  Make sure Tesseract is installed and its executable is in your PATH. You may specify the path in your script:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
  ```

- **Dependency Issues:**  
  Ensure all dependencies are installed in your virtual environment. Use `pip freeze` to verify package versions.

- **Model Compatibility:**  
  If you face issues with the language model (e.g., AVX requirements on Snapdragon devices), consider using an ARM-compatible version like `llama-cpp-python`.

## Open-Source License

This project is licensed under the [MIT License](LICENSE).

For help choosing an open-source license, visit [choosealicense.com](https://choosealicense.com).

## Acknowledgments

- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [Transformers](https://github.com/huggingface/transformers)
- [Flask](https://flask.palletsprojects.com/)