import os
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file


# API Keys and IDs
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")

# Paths
BUFFER_FOLDER = "buffer"

# YouTube API Limits (Optional, can be used later if you implement quota management)
YOUTUBE_TITLE_MAX_LENGTH = 100
YOUTUBE_TAGS_MAX_COUNT = 5

# Video Processing Config (Optional, for future flexibility)
FRAME_EXTRACTION_TIME = 4  # Extract frame at 4 seconds
