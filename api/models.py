from pydantic import BaseModel

class Article(BaseModel):
    id: int
    title: str
    date: str
    author: str
    url: str
    summary: str | None = None