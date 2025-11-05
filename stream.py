import subprocess
from urls import *
import time

def record_audio_stream(url: str, output_dir: str, timeout: int = 120) -> int:

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-i", url,
        "-c:a", "copy",
        output_dir
    ]

    print(f"Starting recording: {url}")

    try:
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        start_time = time.time()
        while True:
            # Check if process has exited
            if process.poll() is not None:
                print("FFmpeg process exited.")
                break

            # Read stderr output (useful for detecting errors)
            output = process.stderr.readline().strip()
            if output:
                print(output)  # Log FFmpeg messages

                # Detect if FFmpeg reports an issue with the stream
                if "Server returned 404" in output or "Invalid data found" in output:
                    print("Stream unavailable. Stopping recording.")
                    process.terminate()
                    process.wait()
                    return 1  # Return error code

            time.sleep(1)  # Prevent excessive CPU usage
        return 0  # Success

    except Exception as e:
        print(f"Error: {e}")
        return -1
if __name__ == "__main__":
    while True:
        record_audio_stream(STREAM_URL, output_dir="recordings/last.mp3")
        time.sleep(5)