"""
Handles DB logic for podcasts:
- connect to SQLite
- insert episodes
- avoid duplicates (use audio_url as unique key)
- update episodes with transcript after transcription
"""
import sqlite3
from datetime import datetime, timezone

DB_NAME = "vc_data.db"  # same database as articles, different table

def get_connection():
    # opens the vc_data.db file (creates it if it doesn't exist yet)
    return sqlite3.connect(DB_NAME)

def init_db():
    """Create the empty episodes table if it doesn't exist yet."""
    conn = get_connection()
    cursor = conn.cursor()  # cursor is the object used to run SQL commands

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- unique row ID, auto-increments with each insert
            podcast_id TEXT,
            podcast_name TEXT,
            title TEXT,
            published TEXT,
            audio_url TEXT UNIQUE,         -- no two rows can have the same url (avoid duplicates)
            audio_path TEXT,
            fetched_at TEXT,
            transcript TEXT,               -- filled in after transcription
            transcribed_at TEXT,           -- when transcription happened
            transcribed INTEGER DEFAULT 0  -- 0 = not transcribed yet, 1 = done
        )
    """)

    conn.commit()  # save the changes to the file
    conn.close()   # close the connection

def save_episodes(episodes: list) -> int:
    """Insert a list of episode metadata dicts, skip duplicates. Returns count of new rows."""
    conn = get_connection()
    cursor = conn.cursor()
    new_count = 0  # track how many episodes are actually new

    # put each episode into the DB
    for episode in episodes:
        # cursor.execute(SQL string, tuple of actual data to plug in)
        # INSERT OR IGNORE: try to insert the row, but if audio_url already exists skip
        cursor.execute("""
            INSERT OR IGNORE INTO episodes (
                podcast_id, podcast_name, title, published,
                audio_url, audio_path, fetched_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            # the ? placeholders map to the values in order
            episode["podcast_id"],
            episode["podcast_name"],
            episode["title"],
            episode["published"],
            episode["audio_url"],
            episode["audio_path"],
            episode["fetched_at"],
        ))
        # cursor.rowcount tells us what just happened:
        # 1 = a new row was inserted, 0 = it was a duplicate and was ignored
        if cursor.rowcount == 1:
            new_count += 1

    conn.commit()  # write all inserts to the file at once (more efficient than committing per row)
    conn.close()
    return new_count  # lets the caller print "saved X new episodes"

def get_untranscribed_episodes() -> list:
    """Return all episodes that have been fetched but not yet transcribed."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, audio_path, title
        FROM episodes
        WHERE transcribed = 0
    """)

    rows = cursor.fetchall()  # fetchall() returns a list of tuples, one per row
    conn.close()
    return rows

def update_episode_transcript(episode_id: int, transcript: str):
    """Save the transcript and mark the episode as transcribed."""
    conn = get_connection()
    cursor = conn.cursor()

    # use UPDATE to set the transcript, mark as transcribed, and save the timestamp
    cursor.execute("""
        UPDATE episodes
        SET transcript = ?,
            transcribed = 1,
            transcribed_at = ?
        WHERE id = ?
    """, (
        # fill in the placeholders with actual values
        transcript,
        datetime.now(timezone.utc).isoformat(),
        episode_id,
    ))

    conn.commit()
    conn.close()
