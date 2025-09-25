from fastapi import FastAPI, HTTPException, Query, Header, Request
from . import crud
import subprocess
import os
import sys

app = FastAPI(title="API Artículos ETL")

API_TOKEN = "kitsunepruebalamejorrcontrasena"  # Token

@app.get("/articles")
def list_articles(limit: int = 20, offset: int = 0):
    return crud.list_articles(limit, offset)

@app.get("/articles/{article_id}")
def get_article(article_id: int):
    article = crud.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@app.get("/search")
def search_articles(q: str = Query(..., min_length=3)):
    return crud.search_articles(q)

@app.api_route("/update", methods=["GET", "POST"])
async def update_articles(
    request: Request,
    token: str | None = None,
    authorization: str | None = Header(None, convert_underscores=False),
):
    """
    Update the database by running the ETL.
    - Try to obtain the token from:
      1) Authorization header: “Bearer <token>” or just “<token>”
      2) Query string ?token=...
      3) JSON body {“token”:“...”}
    - Allow GET and POST to facilitate testing (although POST is preferable).
    """
    # 1) Auth (using header)
    token_value = None
    if authorization:
        auth = authorization.strip()
        if auth.lower().startswith("bearer "):
            token_value = auth.split(" ", 1)[1]
        else:
            token_value = auth

    # 2) Auth (not using header) query parameter
    if not token_value and token:
        token_value = token

    # 3) Auth (read json)
    if not token_value:
        try:
            body = await request.json()
            token_value = body.get("token")
        except Exception:
            token_value = None

    if token_value != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")

    etl_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../etl/main.py"))

    # Etl subprocess - match with api
    result = subprocess.run([sys.executable, etl_path], capture_output=True, text=True)
    if result.returncode != 0:
        # stderr for debugging
        raise HTTPException(status_code=500, detail=f"Error in ETL run: {result.stderr}")

    return {"status": "ok", "message": "Data updated!"}
