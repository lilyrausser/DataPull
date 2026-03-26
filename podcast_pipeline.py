import argparse
# import each module's main() function, but rename it so the names don't clash
from podcasts.fetch_audio import main as fetch_audio
from podcasts.transcribe import main as transcribe
from podcasts.storage import init_db, save_episodes

def run(days_back):
    """Run the full podcast pipeline: fetch audio, then transcribe."""
    print("Initializing database...")
    init_db()  # creates the episodes table if it doesn't exist yet

    print("=== Step 1: Fetching podcast episodes ===")
    episodes = fetch_audio(days_back=days_back)  # returns list of metadata dicts
    new_count = save_episodes(episodes) # inserts metadata into DB, not transcribed yet
    print(f"Saved {new_count} new episodes to database")

    print("\n=== Step 2: Transcribing episodes ===")
    transcribe()  # reads untranscribed episodes from DB, writes transcripts back

    print("\nPodcast pipeline complete.")

# parses command-line arguments and starts pipeline
if __name__ == "__main__":
    # argparse handles command-line arguments like --days-back 3
    parser = argparse.ArgumentParser(description="Run the podcast pipeline: fetch + transcribe")
    # regsiter a --days-back argument
    parser.add_argument("--days-back", type=int, default=7,
                        help="How many days back to fetch episodes (default: 7)")
    # args.days_back will be 7 unless the --days-back passed in
    args = parser.parse_args()

    run(days_back=args.days_back)