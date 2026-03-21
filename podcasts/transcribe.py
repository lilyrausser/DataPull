from faster_whisper import WhisperModel
import os

# Config -----------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
EPISODES_DIR = os.path.join(_HERE, "audio")
TRANSCRITS_DIR = os.path.join(_HERE, "transcripts")
MODEL_SIZE = "base"  # tiny, base, small, medium, large
# ------------------------------------------------------------

def load_model(model_size: str) -> WhisperModel:
    print(f"Loading Whisper model: {model_size}")
    model = WhisperModel(model_size)
    print("Model loaded!")
    return model

def transcribe_episode(model: WhisperModel, mp3_path: str) -> str:
    """Transcribe a single mp3 file, returns transcript text"""
    print(f"  Transcribing: {mp3_path}")
    segments, info = model.transcribe(mp3_path)
    return " ".join([segment.text for segment in segments])

def main():
    """Load model, transcribe all mp3 files in episodes directory, save transcripts, and delete mp3s"""
    model = load_model(MODEL_SIZE)

    mp3_files = [f for f in os.listdir(EPISODES_DIR) if f == "tbpn__Bezos_100B_AI_Plan_Nvida_Chip_Smuggling_The_Mansion_Section__Diet_TBPN.mp3"]
    # mp3_files = [f for f in os.listdir(EPISODES_DIR) if f.endswith(".mp3")]
    print(f"\nFound {len(mp3_files)} mp3 files in '{EPISODES_DIR}/'")

    for filename in mp3_files:
        mp3_path = os.path.join(EPISODES_DIR, filename)
        os.makedirs(TRANSCRITS_DIR, exist_ok=True)
        transcript_path = os.path.join(TRANSCRITS_DIR, filename.replace(".mp3", ".txt"))

        if os.path.exists(transcript_path):
            print(f"\nAlready transcribed, skipping: {filename}")
            continue

        print(f"\nEpisode: {filename}")
        transcript = transcribe_episode(model, mp3_path)

        with open(transcript_path, "w") as f:
            f.write(transcript)
        print(f"Saved transcript: {transcript_path}")

        os.remove(mp3_path)
        print(f"Deleted mp3: {mp3_path}")

    print("\nDone!")

if __name__ == "__main__":
    main()