"""
Handles DB logic only 
- connect to SQLite 
- insert articles 
- avoid duplicates (use URL as a unique key)
"""
import sqlite3
from datetime import datetime, timezone


DB_NAME = "vc_data.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            link TEXT UNIQUE,
            published TEXT,
            summary TEXT
        )
    """)

    # add fetched_at column if the table already existed before 
    cursor.execute('PRAGMA table_info(articles)')
    columns = [row[1] for row in cursor.fetchall()]
    if 'fetched_at' not in columns: 
        cursor.execute('ALTER TABLE articles ADD COLUMN fetched_at TEXT')
        
    conn.commit()
    conn.close()


def save_articles(articles):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    new_count = 0
    fetched_at = datetime.now(timezone.utc).isoformat()

    for article in articles:
        cursor.execute("""
            INSERT OR IGNORE INTO articles
            (source, title, link, published, summary)
            VALUES (?, ?, ?, ?, ?)
        """, (
            article["source"],
            article["title"],
            article["link"],
            article["published"],
            article["summary"]
        ))
        if cursor.rowcount == 1: 
            new_count += 1 

    conn.commit()
    conn.close()

    return new_count 