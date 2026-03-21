"""
Handles DB logic only 
- connect to SQLite 
- insert articles 
- avoid duplicates (use URL as a unique key)
"""
import sqlite3
from datetime import datetime, timezone


DB_NAME = "vc_data.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            title TEXT,
            link TEXT UNIQUE,
            published TEXT,
            summary TEXT,
            fetched_at TEXT,
            article_text TEXT,
            clean_text TEXT,
            processed INTEGER DEFAULT 0,
            fetch_status TEXT,
            processed_at TEXT
        )
    """)
  

    # # add fetched_at column if the table already existed before 
    # cursor.execute('PRAGMA table_info(articles)')
    # columns = [row[1] for row in cursor.fetchall()]
    # if 'fetched_at' not in columns: 
    #     cursor.execute('ALTER TABLE articles ADD COLUMN fetched_at TEXT')
        
    conn.commit()
    conn.close()


def insert_article(source, title, link, published, summary, fetched_at): 
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO articles (
            source, title, link, published, summary, fetched_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (source, title, link, published, summary, fetched_at))

    conn.commit()
    conn.close()

def delete_source(source_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE source = ?", (source_name,))
    conn.commit()
    conn.close()

def get_unprocessed_articles(limit=20):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, source, title, link, summary
    FROM articles
    WHERE processed = 0
        AND (article_text IS NULL OR article_text = '')
    LIMIT ? 
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()
    return rows 
    
def update_article_parsed(article_id, article_text, clean_text, fetch_status='success'):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE articles
        SET article_text = ?,
            clean_text = ?,
            processed = 1,
            fetch_status = ?,
            processed_at = ?
        WHERE id = ?
    """, (
        article_text,
        clean_text,
        fetch_status,
        datetime.utcnow().isoformat(),
        article_id
    ))

    conn.commit()
    conn.close()

def mark_article_failed(article_id, fetch_status='failed'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE articles
        SET processed = 1,
            fetch_status = ?,
            processed_at = ?
        WHERE id = ?
        """, (
        fetch_status,
        datetime.utcnow().isoformat(),
        article_id
        ))

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