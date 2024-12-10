import subprocess
import os
import sys

# Add whisper to Python path if not installed system-wide
# If whisper is a submodule in ./whisper, do this:
sys.path.append(os.path.join(os.path.dirname(__file__), "whisper"))

import whisper

def extract_audio(mkv_path, wav_path="audio.wav"):
    import subprocess
    
    # Step 1: Extract audio from MKV
    cmd = [
        "ffmpeg",
        "-i", mkv_path,
        "-vn",  # Ignore video
        "-ar", "16000",  # Resample to 16kHz
        "-ac", "1",  # Convert to mono
        "-c:a", "pcm_s16le",  # Use WAV format
        "out/audio_processed.wav",
        "-y"  # Overwrite if exists
    ]
    subprocess.run(cmd, check=True)

    # Step 2: Trim silence, normalize, denoise, and add fade-in
    cmd = [
        "ffmpeg",
        "-i", "out/audio_processed.wav",
        "-af", "silenceremove=1:0:-30dB,loudnorm,afftdn=nf=-25,afade=t=in:ss=0:d=1.0",
        wav_path,
        "-y"  # Overwrite if exists
    ]
    subprocess.run(cmd, check=True)
    

def transcribe_audio(wav_path, model_name="small"):
    model = whisper.load_model(model_name)
    result = model.transcribe(wav_path, initial_prompt="The following is the audo from a movie or tv show:")
    return result["text"]

if __name__ == "__main__":
    # Example usage:
    mkv_file = "in/the_swan.mkv"  # Change this to your MKV filename
    wav_file = "out/audio.wav"

    # 1. Extract audio from MKV
    extract_audio(mkv_file, wav_file)

    # 2. Transcribe using Whisper
    transcription = transcribe_audio(wav_file, model_name="small")
    # Save transcription to a file
    with open("out/transcription.txt", "w") as f:
        f.write(transcription)
