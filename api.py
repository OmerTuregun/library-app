import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from app.library import Library
from app.entities import Book
from app.storage.json_store import JSONBookStore

# MySQL'e az sonra geçeceğiz; başta JSON ile başlatıyoruz (isterlerin gereği)
def build_library():
    backend = os.getenv("STORAGE_BACKEND", "json")
    if backend == "json":
        return Library(JSONBookStore(os.getenv("JSON_FILE", "library.json")))
    else:
        # MySQL varyantını birazdan ekleyeceğiz
        from app.storage.mysql_store import MySQLBookStore
        return Library(MySQLBookStore(os.getenv("DATABASE_URL")))
        
lib = build_library()
app = FastAPI(title="Library API", version="1.0.0")

class BookOut(BaseModel):
    title: str
    author: str
    isbn: str

class ISBNIn(BaseModel):
    isbn: str

class BookUpdateIn(BaseModel):
    title: str | None = None
    author: str | None = None

@app.get("/books", response_model=List[BookOut])
def get_books():
    return [BookOut(**b.__dict__) for b in lib.list_books()]

@app.post("/books", response_model=BookOut)
def post_books(payload: ISBNIn):
    try:
        b = lib.add_book_by_isbn(payload.isbn)
        return BookOut(**b.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/books/{isbn}")
def delete_book(isbn: str):
    lib.remove_book(isbn)
    return {"ok": True}

# Bonus: Güncelleme (PUT)
@app.put("/books/{isbn}", response_model=BookOut)
def update_book(isbn: str, payload: BookUpdateIn):
    book = lib.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Bulunamadı.")
    if payload.title:  book.title  = payload.title
    if payload.author: book.author = payload.author
    # kaydet:
    lib.remove_book(isbn)
    lib.add_book(book)
    return BookOut(**book.__dict__)
