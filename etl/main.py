from extract import fetch_articles
from transform import normalize_articles
from load import init_db, load_articles

def run_etl():
    print("Extract...")
    raw = fetch_articles(limit=100)

    print("Transform...")
    normalized = normalize_articles(raw)

    print("Create DB (SQLite is here!)...")
    init_db()

    print("Load...")
    load_articles(normalized)

    print("ETL pipeline finished, Kitsune part 1 completed!", len(normalized), "registers inserted.")

if __name__ == "__main__":
    run_etl()