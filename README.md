# Services Backend - Sistem Bank Terdistribusi

Dokumentasi singkat untuk layanan backend proyek "Services Backend".

## Deskripsi

Proyek ini adalah backend untuk sistem bank terdistribusi yang dibangun menggunakan FastAPI. Aplikasi menggunakan SQLAlchemy (asynchronous) dan aiomysql untuk koneksi database MySQL. Fokus saat ini mencakup fitur autentikasi (registrasi & login) dan model-model dasar nasabah, login, portofolio, dan transaksi.

## Fitur utama

- Registrasi pengguna (nasabah)
- Login (melalui middleware verifikasi)
- Struktur database memakai SQLAlchemy Async
- Menggunakan environment variables untuk konfigurasi koneksi database

## Teknologi & Dependensi

Beberapa paket penting (lihat `requirements.txt` untuk daftar lengkap):

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy (async)
- aiomysql / PyMySQL
- passlib (bcrypt)
- python-dotenv

## Persyaratan (Prasyarat)

- MySQL / MariaDB yang dapat diakses dari aplikasi
- Python 3.11+
- Virtual environment (direkomendasikan)

## Instalasi (Windows PowerShell)

1. Buat dan aktifkan virtual environment (opsional tapi direkomendasikan):

```powershell
python -m venv env ; .\env\Scripts\Activate.ps1
```

2. Install dependensi:

```powershell
pip install -r requirements.txt
```

3. Buat file `.env` di root proyek dan isi variabel berikut:

- DB_HOST
- DB_USER
- DB_PASSWORD
- DB_NAME
- DB_PORT

Contoh `.env` (jangan commit file ini ke VCS):

```
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=rahasia
DB_NAME=services_db
DB_PORT=3306
```

## Menjalankan aplikasi

Jalankan server pengembangan dengan Uvicorn:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API akan tersedia di `http://localhost:8000` dan dokumentasi interaktif OpenAPI di `http://localhost:8000/docs`.

## Endpoints (ringkasan)

Semua endpoint dikelompokkan di bawah prefix `/api/v1`.

- POST /api/v1/auth/register
  - Registrasi nasabah baru
  - Payload (contoh, JSON):

```json
{
  "full_name": "Budi Santoso",
  "birth_date": "1990-01-01",
  "address": "Jl. Contoh No.1",
  "nik": "3201012304950007",
  "phone_number": "08123456789",
  "email": "budi@example.com",
  "username": "budi",
  "password": "rahasia123",
  "PIN": "1234"
}
```

- POST /api/v1/auth/login
  - Login menggunakan middleware `verify_auth` (implementasi verifikasi berada di `app/middleware/auth_middleware.py`)

Catatan: Lihat skema Pydantic `app/schemas/auth_schema.py` untuk detail field.

## Konfigurasi Database

- Koneksi database dibuat di `app/db/database.py` sebagai asynchronous engine menggunakan `aiomysql`.
- URL koneksi terbentuk dari variabel environment yang diambil melalui `python-dotenv` (`app/core/config.py`).

## Struktur proyek (ringkas)

Berikut struktur utama proyek:

```
README.md
requirements.txt
app/
  main.py              # entrypoint FastAPI
  core/
    config.py          # pembacaan .env
    logging.py
  db/
    database.py        # engine async + dependency get_db
    models/            # model-model SQLAlchemy (Customer, Login, Portofolio, Transaction, ...)
  middleware/
    auth_middleware.py
  repositories/
    auth_repository.py
  routes/
    v1/
      auth_router.py
  schemas/
    auth_schema.py
  services/
    auth_service.py
test/
  test_connection.py   # skrip kecil untuk verifikasi koneksi DB
```

## Testing (cek koneksi DB cepat)

Ada skrip sederhana untuk menguji koneksi database: `test/test_connection.py`.

Jalankan dari PowerShell (pastikan environment aktif dan `.env` sudah terisi):

```powershell
python.exe -m test.test_connection
```

Output akan menampilkan apakah koneksi berhasil atau gagal.

## Catatan pengembangan

- Password di-hash menggunakan `passlib` dengan algoritma bcrypt (di `app/services/auth_service.py`).
- Pastikan password yang dikirimkan tidak lebih dari 72 byte (pemeriksaan ada di service).
- File `app/core/logging.py` ada tetapi kosong — Anda bisa menambahkan konfigurasi logging sesuai kebutuhan.

## Kontribusi

Jika ingin berkontribusi, silakan fork repo, buat branch fitur, dan kirim PR. Sertakan deskripsi perubahan dan jika mengubah skema DB, tambahkan migrasi atau instruksi terkait.

## Lisensi

Tambahkan file `LICENSE` jika ingin menentukan lisensi. Saat ini tidak ada lisensi eksplisit di repo.

## Kontak

Jika butuh bantuan lebih lanjut atau ingin diskusi desain, tambahkan issue di repository.

---

Dokumentasi ini dibuat otomatis berdasarkan sumber di folder `app/`. Perlu penambahan detail (contoh: contoh response, autentikasi token, migrasi DB) bila fitur baru ditambahkan.
