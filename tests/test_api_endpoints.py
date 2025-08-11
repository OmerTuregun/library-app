import importlib, os
from fastapi.testclient import TestClient
from app.entities import Book
import app.library as library_mod  # <-- DEĞİŞİKLİK: tüketen modülü import et

def make_client(tmp_path):
    os.environ["STORAGE_BACKEND"] = "json"
    os.environ["JSON_FILE"] = str(tmp_path / "lib.json")
    import api
    importlib.reload(api)  # env'e göre app'i yeniden yükle
    return TestClient(api.app)

def test_post_get_put_delete_with_stub(tmp_path, monkeypatch):
    async def fake_fetch_async(isbn: str):
        return Book(title="Stub Title", author="Stub Author", isbn=isbn)

    # ÖNEMLİ: tüketen yerdeki ismi patch'le
    monkeypatch.setattr(library_mod, "fetch_book_by_isbn", fake_fetch_async)

    c = make_client(tmp_path)

    r = c.post("/books", json={"isbn": "999"})
    assert r.status_code == 200
    assert r.json()["title"] == "Stub Title"

    r = c.get("/books")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1 and data[0]["isbn"] == "999"

    r = c.put("/books/999", json={"title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"

    r = c.delete("/books/999")
    assert r.status_code == 200
    assert r.json()["ok"] is True
