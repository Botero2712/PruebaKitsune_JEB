from datetime import datetime

def normalize_articles(raw_articles):
    """Normaliza y organiza los artículos en un formato consistente."""
    normalized = []
    for art in raw_articles:
        # Obtener lista de autores si existe
        authors = art.get("authors", [])
        if authors:
            author_names = ", ".join([a.get("name", "Unknown") for a in authors])
        else:
            author_names = "Unknown"

        normalized.append({
            "id": art["id"],
            "title": art["title"],
            "date": art["published_at"],
            "author": author_names,
            "url": art["url"],
            "summary": art["summary"][:255] if art["summary"] else None
        })
    return normalized
