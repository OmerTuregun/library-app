from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List, Optional

from app.library import Library
import os

# storage seçimi
def build_library():
    backend = os.getenv("STORAGE_BACKEND", "json")
    if backend == "mysql":
        from app.storage.mysql_store import MySQLBookStore
        return Library(MySQLBookStore(os.getenv("DATABASE_URL")))
    else:
        from app.storage.json_store import JSONBookStore
        return Library(JSONBookStore(os.getenv("JSON_FILE", "library.json")))

app = FastAPI(title="Library API", version="1.1.0")
lib = build_library()

class BookOut(BaseModel):
    title: str
    author: str
    isbn: str

class ISBNIn(BaseModel):
    isbn: str

class BookUpdateIn(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None

# root redirect
from fastapi.responses import RedirectResponse
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/books", response_model=List[BookOut])
def get_books():
    return [BookOut(**b.__dict__) for b in lib.list_books()]

@app.post("/books", response_model=BookOut)
def post_books(payload: ISBNIn):
    try:
        b = lib.add_book_by_isbn(payload.isbn)  # CLI için sync wrapper
        return BookOut(**b.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    lib.remove_book(isbn)
    return {"ok": True}

# ---- BONUS: PUT (güncelleme)
@app.put("/books/{isbn}", response_model=BookOut)
def update_book(isbn: str, payload: BookUpdateIn):
    book = lib.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Bulunamadı.")
    if payload.title is not None:
        book.title = payload.title
    if payload.author is not None:
        book.author = payload.author
    # kalıcı kaydet: önce eskisini sil, sonra ekle
    lib.remove_book(isbn)
    lib.add_book(book)
    return BookOut(**book.__dict__)
