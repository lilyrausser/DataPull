import whisper
import os
from podcasts.storage import get_untranscribed_episodes, update_episode_transcript

# Config -----------------------------------------------------
MODEL_SIZE = "base"  # tiny, base, small, medium, large
# ------------------------------------------------------------

def load_model(model_size: str) -> whisper.Whisper:
    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)
    print("Model loaded!")
    return model

def transcribe_episode(model: whisper.Whisper, mp3_path: str) -> str:
    """Transcribe a single mp3 file, returns transcript text"""
    print(f"  Transcribing: {mp3_path}")
    result = model.transcribe(mp3_path)
    return result["text"]

def main():
    """Transcribe all untranscribed episodes from the database."""
    # get_untranscribed_episodes() returns a list of tuples: (id, audio_path, title)
    episodes = get_untranscribed_episodes()
    print(f"\nFound {len(episodes)} untranscribed episode(s)")

    if not episodes:
        print("Nothing to transcribe.")
        return  # exit early, no need to load the model

    # only load the model if there's actually something to transcribe
    # (loading is slow, so we avoid it when unnecessary)
    model = load_model(MODEL_SIZE)

    for episode_id, audio_path, title in episodes:  # unpack each tuple into named variables
        print(f"\nEpisode: {title}")

        if not os.path.exists(audio_path):
            print(f"  Audio file not found, skipping: {audio_path}")
            continue

        transcript = transcribe_episode(model, audio_path)

        # save transcript text to DB and mark as transcribed
        update_episode_transcript(episode_id, transcript)
        print(f"  Transcript saved to database")

        os.remove(audio_path)
        print(f"  Deleted mp3: {audio_path}")

    print("\nDone!")

if __name__ == "__main__":
    main()
