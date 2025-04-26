import whisper
import sys
import os



# Check if a file was passed in command-line arguments
if len(sys.argv) < 2:
    print("Usage: python audiototexts.py <audio_file_path>")
    sys.exit(1)

file_path = sys.argv[1]

model = whisper.load_model("base")

result = model.transcribe(file_path,fp16=False)



# Optional: Save to file with the same name + .txt

base_name = os.path.splitext(os.path.basename(file_path))[0]  # Get just the filename without path/extension
txt_filename = os.path.join("texts", base_name + ".txt")      # Save in the "texts" folder

with open(txt_filename, "w", encoding="utf-8") as f:
    f.write(result["text"])
print(f"Transcript saved to: {txt_filename}")

