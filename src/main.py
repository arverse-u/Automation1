import os
from src.drive_handler import fetch_oldest_video
from src.frame_extractor import extract_frame
from src.text_extractor import extract_text_from_image
from src.gemini_handler import preprocess_raw_text, clean_quiz_text_with_gemini, extract_title_description_tags_from_quiz_text
from src.youtube_handler import upload_video
from src.cleanup import clean_up
from src.config import BUFFER_FOLDER,DRIVE_FOLDER_ID,GEMINI_API_KEY


def main():
    # Step 1: Fetch the oldest video from Google Drive
    video_path, file_id = fetch_oldest_video()
    if not video_path:
        print("No video found to process.")
        return
    
    # Step 2: Extract frame at 4 seconds
    frame_output_path = os.path.join(BUFFER_FOLDER, "extracted_frame.jpg")
    try:
        extract_frame(video_path, frame_output_path)
    except Exception as e:
        print(f"❌ Error in frame extraction: {e}")
        return

    # Step 3: Extract text from the extracted frame using Tesseract OCR
    try:
        extracted_text = extract_text_from_image(frame_output_path)
        print(f"Extracted Text: {extracted_text}")
    except Exception as e:
        print(f"❌ Error in text extraction: {e}")
        return

    # Step 4: Clean the OCR text using Gemini API
    preprocessed_text = preprocess_raw_text(extracted_text)
    cleaned_text = clean_quiz_text_with_gemini(preprocessed_text)
    print(f"Cleaned Text: {cleaned_text}")

    # Step 5: Generate YouTube metadata (title, description, tags)
    title, description, tags = extract_title_description_tags_from_quiz_text(cleaned_text)

    # Step 6: Upload the video to YouTube
    try:
        video_id = upload_video(video_path, title, description, tags)
    except Exception as e:
        print(f"❌ Error during video upload: {e}")
        return

    # Step 7: Cleanup - Delete the video from Google Drive and local buffer
    clean_up(file_id)
    print(f"✅ Video uploaded and cleanup completed successfully.")


if __name__ == "__main__":
    main()
