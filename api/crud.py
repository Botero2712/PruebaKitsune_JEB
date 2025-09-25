from .database import get_connection

def list_articles(limit=20, offset=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_article(article_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def search_articles(keyword: str):
    conn = get_connection()
    cursor = conn.cursor()
    like_pattern = f"%{keyword}%"
    cursor.execute(
        "SELECT * FROM articles WHERE title LIKE ? OR summary LIKE ?",
        (like_pattern, like_pattern),
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
