import requests

API_URL = "https://api.spaceflightnewsapi.net/v4/articles/"

def fetch_articles(limit=100):
    """Spaceflight News API. Docs: https://spaceflightnewsapi.net/"""
    response = requests.get(API_URL, params={"limit": limit})
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])