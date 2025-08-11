from typing import List, Optional
from app.entities import Book
from app.storage.base import BookStore
from app.services.openlibrary import fetch_book_by_isbn
import asyncio

class Library:
    def __init__(self, store: BookStore) -> None:
        self.store = store

    def add_book(self, book: Book) -> None:
        self.store.add(book)

    def remove_book(self, isbn: str) -> None:
        self.store.remove(isbn)

    def list_books(self) -> List[Book]:
        return self.store.list()

    def find_book(self, isbn: str) -> Optional[Book]:
        return self.store.find(isbn)

    # --- ASENKRON: FastAPI'de kullan (endpoint içinde await et) ---
    async def add_book_by_isbn_async(self, isbn: str) -> Book:
        book = await fetch_book_by_isbn(isbn)
        if not book:
            raise ValueError("Kitap bulunamadı veya API hatası.")
        self.add_book(book)
        return book

    # --- SENKRON: Terminal/CLI için kullan ---
    def add_book_by_isbn(self, isbn: str) -> Book:
        # Burayı CLI'da çağır; FastAPI tarafında _async olanı await et
        return asyncio.run(self.add_book_by_isbn_async(isbn))
