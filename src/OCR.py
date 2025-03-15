import os
from PIL import Image
from qai_hub_models.models.trocr import Model


def ocr_with_trocr(image_path, model):
    image = Image.open(image_path).convert("RGB")
    ocr_text = model(image)
    return ocr_text

def process_images_folder(image_folder, model):
    results = {}
    for filename in os.listdir(image_folder):
        if filename.lower().endswith('.jpg'):
            image_path = os.path.join(image_folder, filename)
            text = ocr_with_trocr(image_path, model)
            results[image_path] = text
            print(f"OCR result for {image_path}:\n{text}\n")
    return results

if __name__ == "__main__":
    image_folder = "output_images"
    model = Model.from_pretrained()
    model.to("cpu")
    
    results = process_images_folder(image_folder, model)
    
    with open("ocr_results.txt", "w", encoding="utf-8") as f:
        for image_path, text in results.items():
            f.write(f"Results for {image_path}:\n{text}\n\n")
    print("OCR processing complete. Results saved in ocr_results.txt.")
