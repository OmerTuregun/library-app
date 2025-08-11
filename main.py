from app.library import Library
from app.storage.json_store import JSONBookStore

def menu():
    store = JSONBookStore("library.json")
    lib = Library(store)

    while True:
        print("\n1) Kitap Ekle (ISBN)  2) Kitap Sil  3) Listele  4) Ara  5) Çıkış")
        sec = input("Seçim: ").strip()

        if sec == "1":
            isbn = input("ISBN: ").strip()
            try:
                added = lib.add_book_by_isbn(isbn)
                print("Eklendi:", added)
            except ValueError as e:
                print("Hata:", e)

        elif sec == "2":
            isbn = input("ISBN: ").strip()
            lib.remove_book(isbn)
            print("Silindi (varsa).")

        elif sec == "3":
            for b in lib.list_books():
                print("-", b)

        elif sec == "4":
            isbn = input("ISBN: ").strip()
            b = lib.find_book(isbn)
            print(b if b else "Bulunamadı.")

        elif sec == "5":
            break
        else:
            print("Geçersiz seçim.")
