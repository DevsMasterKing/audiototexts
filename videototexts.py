import whisper
import sys
import os
import subprocess

# Check if a file was passed in command-line arguments
if len(sys.argv) < 2:
    print("Usage: python audiototexts.py <audio_file_path>")
    sys.exit(1)

file_path = sys.argv[1]

# Check if the file is a video (e.g., .mp4, .mov, .avi, .webm)
video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.webm']
file_extension = os.path.splitext(file_path)[1].lower()

audio_file_path = file_path

# If it's a video file, extract the audio using ffmpeg
if file_extension in video_extensions:
    audio_file_path = os.path.splitext(file_path)[0] + ".wav"  # Save as .wav
    print(f"Extracting audio from video: {file_path} -> {audio_file_path}")
    
    # Run ffmpeg to extract audio (from .webm or other video formats)
    subprocess.run(["ffmpeg", "-i", file_path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "2", audio_file_path], check=True)

# Load the Whisper model
model = whisper.load_model("base")

# Transcribe the audio (or extracted audio)
result = model.transcribe(audio_file_path, fp16=False)

# Optional: Save to file with the same name + .txt
base_name = os.path.splitext(os.path.basename(file_path))[0]  # Get just the filename without path/extension
txt_filename = os.path.join("texts", base_name + ".txt")      # Save in the "texts" folder

# Save the transcript to a text file
with open(txt_filename, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"Transcript saved to: {txt_filename}")

# Clean up extracted audio file if it was created
if audio_file_path != file_path:
    os.remove(audio_file_path)
    print(f"Removed temporary audio file: {audio_file_path}")
