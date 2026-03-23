import feedparser # for parsing RSS feeds
import requests
import os
import re
from datetime import datetime, timedelta, timezone
from podcasts.rss_podcasts import rss_podcasts

# Config -----------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(_HERE, "audio")
DAYS_BACK = 7
# ------------------------------------------------------------

def sanitize_filename(title: str) -> str:
    """Remove special characters from episode title for use as filename"""
    return re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")

def fetch_feed(rss_url: str) -> feedparser.FeedParserDict:
    """Fetch and parse the RSS feed"""
    print(f"  Fetching feed: {rss_url}")
    # make HTTP GET request to RSS URL, get XML, parse into Python object
    feed = feedparser.parse(rss_url)
    return feed

def is_recent(entry: feedparser.FeedParserDict, cutoff: datetime) -> bool:
    """Check if an episode was published after the cutoff date."""
    pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
    return pub_date >= cutoff

def download_episode(entry: feedparser.FeedParserDict, podcast: dict, output_dir: str) -> dict:
    """Download a single episode mp3, returns metadata dict (or None if skipped)"""
    if not entry.get("enclosures"):
        print(f"    Skipping (no audio): {entry.title}")
        return None

    audio_url = entry.enclosures[0].href
    filename = f"{podcast['id']}__{sanitize_filename(entry.title)}.mp3"
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        print(f"    Already exists, skipping: {filename}")
    else:
        print(f"    Downloading: {filename}")
        response = requests.get(audio_url, stream=True) # stream=True to download in chunks

        # save to file in chunks to avoid loading entire file into memory
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"    Saved: {filepath}")

    # convert published_parsed (a time.struct_time tuple) to an ISO string
    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()

    return {
        "podcast_id": podcast["id"],
        "podcast_name": podcast["name"],
        "title": entry.title,
        "published": published,
        "audio_url": audio_url,
        "audio_path": filepath,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }

def fetch_recent_episodes(podcast: dict, cutoff: datetime, output_dir: str, days_back: int) -> list:
    """Fetch and download all recent episodes, returns list of metadata dicts"""
    feed = fetch_feed(podcast["rss_feed"])
    episodes = []

    for entry in feed.entries:
        if not is_recent(entry, cutoff):
            break  # RSS is newest-first, so we can stop here

        metadata = download_episode(entry, podcast, output_dir)
        if metadata:
            episodes.append(metadata)

    if not episodes:
        print(f"    No new episodes in the last {days_back} days")
    else:
        print(f"  Found {len(episodes)} episode(s) in the last {days_back} days")

    return episodes

def main(days_back=DAYS_BACK) -> list:
    """Fetch and download recent episodes for all podcasts, returns list of metadata dicts"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    print(f"Fetching episodes since {cutoff.strftime('%Y-%m-%d')}\n")

    all_episodes = []
    for podcast in rss_podcasts:
        print(f"Podcast: {podcast['name']}")
        episodes = fetch_recent_episodes(podcast, cutoff, OUTPUT_DIR, days_back)
        all_episodes.extend(episodes)  # extend adds all items from a list, unlike append which adds the list itself
        print()

    print(f"Done! Episodes saved to '{OUTPUT_DIR}/'")
    return all_episodes

if __name__ == "__main__":
    main()
