"""
Handles DB logic only 
- connect to SQLite 
- insert articles 
- avoid duplicates (use URL as a unique key)
"""
import sqlite3


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

    conn.commit()
    conn.close()


def save_articles(articles):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

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

    conn.commit()
    conn.close()