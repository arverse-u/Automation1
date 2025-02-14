import os
import subprocess
from src.config import BUFFER_FOLDER, FRAME_EXTRACTION_TIME


def extract_frame(video_path, output_path):
    try:
        # Extract frame at specific timestamp (4 seconds in this case)
        result = subprocess.run(
            [
                "ffmpeg", "-y", "-i", video_path,
                "-ss", f"00:00:{FRAME_EXTRACTION_TIME:02}",  # Example: 00:00:04
                "-vframes", "1",
                "-q:v", "2",  # Good quality frame extraction
                output_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr.decode()}")

        print(f"✅ Frame extracted successfully to {output_path}")

    except Exception as e:
        raise RuntimeError(f"❌ Failed to extract frame from {video_path}: {e}")


if __name__ == "__main__":
    video_file = os.path.join(BUFFER_FOLDER, "test1.mp4")
    output_frame = os.path.join(BUFFER_FOLDER, "test1_frame.jpg")
    extract_frame(video_file, output_frame)
