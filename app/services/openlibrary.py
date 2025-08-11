import httpx
from typing import Optional
from app.entities import Book

BASE = "https://openlibrary.org"

async def fetch_book_by_isbn(isbn: str) -> Optional[Book]:
    url = f"{BASE}/isbn/{isbn}.json"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            data = r.json()
            title = data.get("title")
            author_names = []

            for a in data.get("authors", []):
                key = a.get("key")
                if not key:
                    continue
                ar = await client.get(f"{BASE}{key}.json")
                if ar.status_code == 200:
                    author_names.append(ar.json().get("name"))

            author = ", ".join([n for n in author_names if n]) or "Unknown"
            if title:
                return Book(title=title, author=author, isbn=isbn)
            return None
    except httpx.HTTPError:
        return None
