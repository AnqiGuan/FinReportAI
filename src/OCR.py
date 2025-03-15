import os
import numpy as np
from PIL import Image
import onnxruntime as ort

encoder_session = ort.InferenceSession("trocr-trocrencoder.onnx")
decoder_session = ort.InferenceSession("trocr-trocrdecoder.onnx")

def preprocess_image(image_path, target_size=(384, 384)):
    image = Image.open(image_path).convert("RGB")
    image = image.resize(target_size)
    image_np = np.array(image).astype(np.float32) / 255.0
    image_np = np.transpose(image_np, (2, 0, 1)) 
    image_np = np.expand_dims(image_np, axis=0)  
    return image_np

dummy_vocab = {i: chr(65 + (i % 26)) for i in range(1000)}

def decode_tokens(token_ids, vocab):
    return ''.join([vocab.get(token, '') for token in token_ids])

def ocr_with_trocr(image_path, encoder_session, decoder_session,
                   start_token_id=1, end_token_id=2, max_length=100):
    image_data = preprocess_image(image_path)
    
    encoder_outputs = encoder_session.run(None, {"pixel_values": image_data})
    encoder_hidden_states = encoder_outputs[0]
    decoder_input = np.array([[start_token_id]], dtype=np.int64)
    generated_tokens = []
    
    for _ in range(max_length):
        decoder_inputs = {
            "input_ids": decoder_input,
            "encoder_hidden_states": encoder_hidden_states
        }
        decoder_outputs = decoder_session.run(None, decoder_inputs)
        logits = decoder_outputs[0]
        next_token = int(np.argmax(logits[0, -1, :]))
        
        if next_token == end_token_id:
            break
        
        generated_tokens.append(next_token)
        decoder_input = np.concatenate([decoder_input, np.array([[next_token]], dtype=np.int64)], axis=1)
    
    ocr_text = decode_tokens(generated_tokens, dummy_vocab)
    return ocr_text

def process_images_folder(image_folder, encoder_session, decoder_session):
    results = {}
    for filename in os.listdir(image_folder):
        if filename.lower().endswith('.jpg'):
            image_path = os.path.join(image_folder, filename)
            text = ocr_with_trocr(image_path, encoder_session, decoder_session)
            results[image_path] = text
            print(f"OCR result for {image_path}:\n{text}\n")
    return results

if __name__ == "__main__":
    image_folder = "output_images"
    results = process_images_folder(image_folder, encoder_session, decoder_session)
    
    with open("ocr_results.txt", "w", encoding="utf-8") as f:
        for image_path, text in results.items():
            f.write(f"Results for {image_path}:\n{text}\n\n")
    print("OCR processing complete. Results saved in ocr_results.txt.")
