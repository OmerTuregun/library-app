📚 Library App — Python 202 Bootcamp Projesi
Basit ama üretime yakın bir kütüphane uygulaması:

Aşama 1: OOP + JSON kalıcılık (CLI)

Aşama 2: Open Library + httpx ile ISBN’den otomatik veri

Aşama 3: FastAPI REST API (GET/POST/PUT/DELETE) + Swagger

Aşama 4 (Bonus): MySQL (Docker) + basit Web UI (/ui) + Testler

Uygulama ISBN girildiğinde Open Library’den başlık/yazar bilgilerini çeker, veriyi MySQL’e kaydeder; /ui üzerinden ekleme, listeleme, güncelleme ve silme yapılabilir.


✨ Özellikler
ISBN ile otomatik kitap ekleme (başlık/yazar Open Library’den çekilir)

Listele / Güncelle / Sil

REST API: GET /books, POST /books, PUT /books/{isbn}, DELETE /books/{isbn}

Swagger UI: /docs (root / otomatik yönlendirir)

Basit Web Arayüzü: /ui (aynı origin → CORS gerekmez)

MySQL 8 + Adminer (görsel DB yönetimi)


🗂️ Proje Yapısı

app/
  entities.py                # Book veri modeli (domain)
  library.py                 # Library iş mantığı (store bağımsız)
  services/openlibrary.py    # Open Library entegrasyonu (httpx)
  storage/
    base.py                  # BookStore arayüzü
    json_store.py            # JSON dosya tabanlı kalıcılık
    mysql_store.py           # MySQL/SQLAlchemy tabanlı kalıcılık
api.py                       # FastAPI uçları
main.py                      # (opsiyonel) CLI / terminal girişi
static/index.html            # Basit web arayüzü (/ui)
Dockerfile
docker-compose.yml
requirements.txt
tests/
  test_library_json.py       # JSON store birim testi
  test_api_endpoints.py      # API testi (Open Library stub’lı)
README.md


🚀 Hızlı Başlangıç
Seçenek 1 — Docker Compose (Önerilen)

docker compose up -d --build
# API:     http://<SUNUCU-IP>:8000/docs
# UI:      http://<SUNUCU-IP>:8000/ui
# Adminer: http://<SUNUCU-IP>:8080   (System: MySQL, Server: db, User: app, Pass: apppass, DB: library)

Seçenek 2 — Lokal (virtualenv, JSON backend)

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export STORAGE_BACKEND=json
export JSON_FILE="library.json"
uvicorn api:app --reload --host 0.0.0.0 --port 8000
# http://localhost:8000/docs  ve  http://localhost:8000/ui

Not: Docker imajında ca-certificates kurulu olduğu için HTTPS çağrıları (Open Library) güvenli şekilde çalışır.


⚙️ Ortam Değişkenleri
STORAGE_BACKEND: mysql | json

Docker Compose varsayılanı: mysql

DATABASE_URL: mysql+pymysql://app:apppass@db:3306/library?charset=utf8mb4

JSON_FILE: JSON backend için dosya adı (varsayılan library.json)


🧪 Test Çalıştırma
Testler ağsızdır (Open Library çağrısı stub’lanır), deterministiktir.

Docker içinde:
# PYTHONPATH ayarı gerekebilir:
docker compose run --rm -e PYTHONPATH=/app app pytest -q

Virtualenv içinde:
pip install -r requirements.txt
pytest -q


🖥️ Kullanım
1) Swagger ile test (kolay)
/docs sayfasından tüm uçları deneyebilirsiniz.

POST /books → Body:
{ "isbn": "9780140328721" }

Diğer ISBN örnekleri: 9780131103627, 9780596007973.

2) Web Arayüzü (/ui)
Üstte ISBN yaz → Ekle

Liste tablosunda başlık/yazar alanlarını değiştir → Kaydet

Sil ile kaydı kaldır

Yenile ile durumu güncelle

3) Komut satırı
# ekle
curl -X POST http://localhost:8000/books -H "Content-Type: application/json" \
  -d '{"isbn":"9780140328721"}'

# listele
curl http://localhost:8000/books

# güncelle
curl -X PUT http://localhost:8000/books/9780140328721 -H "Content-Type: application/json" \
  -d '{"title":"Yeni Başlık"}'

# sil
curl -X DELETE http://localhost:8000/books/9780140328721


📡 API Uçları
GET /books
Tüm kitapları döndürür.

[
  { "title": "Fantastic Mr. Fox", "author": "Roald Dahl", "isbn": "9780140328721" }
]

POST /books
Body:

{ "isbn": "9780140328721" }

Başarılı yanıt:

{ "title": "Fantastic Mr. Fox", "author": "Roald Dahl", "isbn": "9780140328721" }

Hata örnekleri:

404 { "detail": "Kitap bulunamadı veya API hatası." }

400/409 { "detail": "Bu ISBN zaten var." } (implementasyonuna bağlı)


PUT /books/{isbn}
Body (opsiyonel alanlar):

{ "title": "Yeni Başlık", "author": "Yeni Yazar" }

Başarılı Yanıt:

{ "title": "Yeni Başlık", "author": "Roald Dahl", "isbn": "9780140328721" }


DELETE /books/{isbn}
Başarılı yanıt:

{ "ok": true }


🗄️ Veritabanı (MySQL)
Tablo: books

id (PK, auto inc)

isbn (unique, index)

title

author

Adminer ile görsel kontrol:
http://<SUNUCU-IP>:8080 → System: MySQL, Server: db, User: app, Pass: apppass, DB: library.


🔒 Üretim Notları
.env/secrets ile DB şifresi vb. gizli bilgileri dışarı alın.

Uvicorn için CPU çekirdek sayısına göre --workers artırılabilir.

Farklı bir domain’den erişecekseniz CORS’u açın.

Nginx reverse proxy + Let’s Encrypt ile TLS/HTTPS terminasyonu.

Yedekleme: mysqldump ile periyodik dump.


🧭 Yol Haritası / Geliştirme Fikirleri
Arama & sayfalama: GET /books?q=&limit=&offset=

PUT ile kısmi güncelleme geliştirme (title/author NULL kontrolleri)

Alembic ile migration’lar

CI (GitHub Actions): push’ta pytest + Docker build/push

Basit frontend (React/Vue) ve Nginx ile servis

Docker Healthcheck’ler + hazır dashboard


Kapanış
Bu repository, Bootcamp’in üç ana konusunu birleştirip uçtan uca çalışan bir ürün ortaya koyar: OOP → HTTP entegrasyon → API ve Docker altyapısı.
Takıldığınız bir yer olursa issue açın ya da sorularınızı iletin. İyi çalışmalar! 👋