from app.entities import Book
from app.library import Library
from app.storage.json_store import JSONBookStore

def test_add_list_find_remove(tmp_path):
    store = JSONBookStore(tmp_path / "lib.json")
    lib = Library(store)

    b = Book(title="Test", author="Tester", isbn="111")
    lib.add_book(b)

    allb = lib.list_books()
    assert len(allb) == 1 and allb[0].isbn == "111"

    found = lib.find_book("111")
    assert found and found.title == "Test"

    lib.remove_book("111")
    assert lib.find_book("111") is None
