import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "db_kitsune.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            date TEXT,
            author TEXT,
            url TEXT,
            summary TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_articles(articles):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for art in articles:
        cursor.execute("""
            INSERT OR REPLACE INTO articles (id, title, date, author, url, summary)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (art["id"], art["title"], art["date"], art["author"], art["url"], art["summary"]))
    conn.commit()
    conn.close()
