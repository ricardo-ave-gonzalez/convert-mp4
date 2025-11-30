# convert_mp4_subtitles.py

This script allows you to transcribe, translate, and generate subtitles for an MP4 video using OpenAI Whisper, and then embed those subtitles into a new MP4 file using FFmpeg.

The script outputs:
- An `.srt` subtitle file
- An `.ass` subtitle file used internally
- A final `.mp4` video with hardcoded subtitles

## Requirements

### Dependencies:
- Python 3.8+
- Whisper
- FFmpeg
- (Optional) A Python virtual environment

### Install dependencies:

```
pip install openai-whisper
sudo apt install ffmpeg
```

## Usage

```
python3 convert_mp4_subtitles.py <video.mp4> <language-prefix>
```

Example:

```
python3 convert_mp4_subtitles.py interview.mp4 en
```

This generates:
- `en_interview.srt`
- `en_interview.ass`
- `en_interview.mp4`

## Parameters

| Parameter | Description |
|----------|-------------|
| `<video.mp4>` | Path to the input video file. Must exist. |
| `<language-prefix>` | Prefix used for naming output files (es, en, fr, ru, etc.). Does not affect Whisper translation.|

## What the script does

1. Validates arguments.
2. Checks the video file and FFmpeg installation.
3. Loads Whisper `base` model.
4. Transcribes and translates audio.
5. Generates an `.srt` file.
6. Converts `.srt` to `.ass` to avoid rendering issues.
7. Creates a new MP4 with hardcoded subtitles.
8. Prints final summary.

## Output Files

| File | Description |
|------|-------------|
| `xx_name.srt` | SubRip subtitles. |
| `xx_name.ass` | ASS subtitle file. |
| `xx_name.mp4` | Final video with subtitles. |

## Example Output

```
====================================
✔ PROCESS COMPLETE
✔ SRT generated:   en_video.srt
✔ Final video:     en_video.mp4
====================================
```
