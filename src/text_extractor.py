import os
from PIL import Image # type: ignore
import pytesseract # type: ignore
from src.config import BUFFER_FOLDER


def extract_text_from_image(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        text = text.strip()
        if not text:
            raise ValueError("No text detected in image.")
        return text
    except Exception as e:
        raise RuntimeError(f"❌ Failed to extract text from image {image_path}: {e}")


if __name__ == "__main__":
    image_file = os.path.join(BUFFER_FOLDER, "test1_frame.jpg")
    try:
        extracted_text = extract_text_from_image(image_file)
        print(f"✅ Extracted Text: {extracted_text}")
    except Exception as e:
        print(str(e))
