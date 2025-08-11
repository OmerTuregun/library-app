import json, os
from typing import List, Optional
from app.entities import Book
from app.storage.base import BookStore

class JSONBookStore(BookStore):
    def __init__(self, file_path: str = "library.json") -> None:
        self.file_path = file_path
        self._books: List[Book] = []
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.file_path):
            self._save()
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._books = [Book(**b) for b in data]

    def _save(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([b.__dict__ for b in self._books], f, ensure_ascii=False, indent=2)

    def add(self, book: Book) -> None:
        if self.find(book.isbn):
            raise ValueError("Bu ISBN zaten var.")
        self._books.append(book)
        self._save()

    def remove(self, isbn: str) -> None:
        self._books = [b for b in self._books if b.isbn != isbn]
        self._save()

    def list(self) -> List[Book]:
        return list(self._books)

    def find(self, isbn: str) -> Optional[Book]:
        for b in self._books:
            if b.isbn == isbn:
                return b
        return None
