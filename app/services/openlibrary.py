import httpx
from typing import Optional
from app.entities import Book

BASE = "https://openlibrary.org"

async def fetch_book_by_isbn(isbn: str) -> Optional[Book]:
    url = f"{BASE}/isbn/{isbn}.json"
    try:
        async with httpx.AsyncClient(
            timeout=10,
            follow_redirects=True,      # ← önemli: 302’leri takip et
            headers={"User-Agent": "LibraryApp/1.0"}
        ) as client:
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
                    name = ar.json().get("name")
                    if name:
                        author_names.append(name)

            author = ", ".join(author_names) if author_names else "Unknown"
            return Book(title=title, author=author, isbn=isbn) if title else None

    except httpx.HTTPError:
        return None
