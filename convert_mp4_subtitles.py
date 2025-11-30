#!/home/project-model/venv/bin/python3

#!/home/project-model/venv/bin/python3

import whisper
import subprocess
import os
import shutil
import sys

# ---------------------------
# Argument validation
# ---------------------------
if len(sys.argv) < 3:
    print("Usage: python3 script.py <video.mp4> <language-prefix>")
    print("Example: python3 script.py video.mp4 en")
    sys.exit(1)

video_path = sys.argv[1]
language_prefix = sys.argv[2]  # language prefix for filenames (es, en, fr, ru, etc.)

# Verify input file
if not os.path.isfile(video_path):
    print(f"ERROR: File '{video_path}' does not exist")
    sys.exit(1)

# Verify ffmpeg installation
if shutil.which("ffmpeg") is None:
    print("ERROR: ffmpeg is not installed. Install it with: sudo apt install ffmpeg")
    sys.exit(1)

# ---------------------------
# Generate output filenames
# ---------------------------
basename = os.path.splitext(os.path.basename(video_path))[0]

srt_path = f"{language_prefix}_{basename}.srt"
output_video = f"{language_prefix}_{basename}.mp4"

# ---------------------------
# Whisper
# ---------------------------
print("Loading Whisper model...")
model = whisper.load_model("base")  # tiny/base recommended for CPUs

print("Transcribing / translating...")
result = model.transcribe(video_path, task="translate")

# ---------------------------
# Create SRT file
# ---------------------------
print(f"Generating subtitles: {srt_path}")

def format_timestamp(t):
    hrs = int(t // 3600)
    mins = int((t % 3600) // 60)
    secs = int(t % 60)
    ms = int((t * 1000) % 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

with open(srt_path, "w", encoding="utf-8") as srt:
    for i, segment in enumerate(result["segments"], start=1):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"].strip()

        srt.write(f"{i}\n{start} --> {end}\n{text}\n\n")

# ---------------------------
# Create subtitled video (ASS method prevents duplication)
# ---------------------------
import pathlib

video_abs = str(pathlib.Path(video_path).resolve())
srt_abs = str(pathlib.Path(srt_path).resolve())
ass_path = f"{language_prefix}_{basename}.ass"
ass_abs = str(pathlib.Path(ass_path).resolve())
output_abs = str(pathlib.Path(output_video).resolve())

print("Converting SRT → ASS to avoid rendering issues...")
subprocess.run([
    "ffmpeg",
    "-y",
    "-i", srt_abs,
    ass_abs
], check=True)

print(f"Creating subtitled video (no duplication): {output_video}")

cmd_final = [
    "ffmpeg",
    "-y",
    "-i", video_abs,
    "-vf", f"ass='{ass_abs}'",
    "-map", "0:v:0",
    "-map", "0:a:0",
    "-c:v", "libx264",
    "-crf", "18",
    "-preset", "fast",
    "-c:a", "copy",
    output_abs
]

subprocess.run(cmd_final, check=True)

print("\n====================================")
print("✔ PROCESS COMPLETE")
print(f"✔ SRT generated:   {srt_path}")
print(f"✔ Final video:     {output_video}")
print("====================================")

