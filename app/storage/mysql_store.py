from typing import List, Optional
from sqlalchemy import create_engine, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from app.entities import Book
from app.storage.base import BookStore
import os

class Base(DeclarativeBase):
    pass

class BookORM(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(256))
    author: Mapped[str] = mapped_column(String(256))

class MySQLBookStore(BookStore):
    def __init__(self, url: Optional[str] = None) -> None:
        self.url = url or os.getenv(
            "DATABASE_URL",
            "mysql+pymysql://app:apppass@db:3306/library?charset=utf8mb4"
        )
        self.engine = create_engine(self.url, pool_pre_ping=True)
        Base.metadata.create_all(self.engine)

    def add(self, book: Book) -> None:
        with Session(self.engine) as s:
            if s.scalar(select(BookORM).where(BookORM.isbn == book.isbn)):
                raise ValueError("Bu ISBN zaten var.")
            s.add(BookORM(isbn=book.isbn, title=book.title, author=book.author))
            s.commit()

    def remove(self, isbn: str) -> None:
        with Session(self.engine) as s:
            row = s.scalar(select(BookORM).where(BookORM.isbn == isbn))
            if row:
                s.delete(row)
                s.commit()

    def list(self) -> List[Book]:
        with Session(self.engine) as s:
            rows = s.scalars(select(BookORM)).all()
            return [Book(title=r.title, author=r.author, isbn=r.isbn) for r in rows]

    def find(self, isbn: str) -> Optional[Book]:
        with Session(self.engine) as s:
            r = s.scalar(select(BookORM).where(BookORM.isbn == isbn))
            return Book(title=r.title, author=r.author, isbn=r.isbn) if r else None