import os
from src.drive_handler import delete_video_from_drive  # Import the function from drive_handler


def delete_local_buffer():
    """Deletes all files from the buffer folder."""
    buffer_path = "buffer"
    if os.path.exists(buffer_path):
        for file_name in os.listdir(buffer_path):
            file_path = os.path.join(buffer_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted local file: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

def clean_up(video_id):
    """Performs complete cleanup after upload process."""
    delete_video_from_drive(video_id)  # Use the function from drive_handler
    delete_local_buffer()  # Call this to delete local files from the buffer


if __name__ == "__main__":
    # Example usage for testing, replace 'VIDEO_ID' with actual Google Drive file ID
    clean_up('YOUR_VIDEO_FILE_ID')  # Call the cleanup function