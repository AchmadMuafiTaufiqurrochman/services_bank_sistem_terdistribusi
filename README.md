# Services Backend - Sistem Bank Terdistribusi

Dokumentasi untuk layanan backend proyek "Services Backend".

## Deskripsi

Proyek ini adalah backend untuk sistem bank terdistribusi yang dibangun menggunakan FastAPI. Aplikasi menggunakan SQLAlchemy (asynchronous) dan aiomysql untuk koneksi database MySQL. 

Fokus saat ini mencakup:
- **Autentikasi**: Registrasi & Login.
- **Manajemen Akun**: Cek saldo, detail nasabah, mutasi, dan daftar transaksi.
- **Transaksi**: Transfer sesama bank (Overbook), Transfer antar bank (Online), setor/tarik saldo.
- **Middleware**: Validasi Token & PIN.

## Fitur utama

- **Autentikasi Pengguna**: Registrasi nasabah dan login dengan enkripsi bcrypt.
- **Manajemen Portofolio**: 
    - Cek Saldo & Detail Akun.
    - Riwayat Transaksi (Transaction List) & Mutasi.
- **Transaksi Finansial**:
    - **Overbook (Sesama Bank)**: Transfer internal antar rekening.
    - **Online (Antar Bank)**: Transfer eksternal (placeholder logic).
    - **Deposit & Withdraw**: Setor dan tarik dana via API.
- **Validasi Keamanan**:
    - Middleware verifikasi Auth (Login).
    - Middleware verifikasi PIN (untuk transaksi finansial).
- **Integrasi Middleware Eksternal**: Mengirim notifikasi transaksi ke service middleware lain.
- **Deployment Docker**: Dukungan penuh untuk deployment menggunakan Docker & Docker Compose.

## Teknologi & Dependensi

- Python 3.11+
- FastAPI & Uvicorn (Server)
- SQLAlchemy (Async ORM)
- aiomysql (MySQL Driver)
- Docker & Docker Compose
- Alembic (Database Migrations)

## Persyaratan (Prasyarat)

- Docker Desktop (jika menggunakan Docker)
- MySQL / MariaDB (jika berjalan manual)
- Python 3.11+

## Cara Menjalankan (Docker - Direkomendasikan)

Pastikan file `.env` sudah dikonfigurasi (lihat contoh di bawah).

1. **Jalankan container**:
   ```bash
   docker network create minibank-network
   docker-compose up --build -d
   ```
2. **Cek status**:
   ```bash
   docker-compose ps
   ```
3. **Akses API**:
   - URL: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs

## Cara Menjalankan (Manual)

1. Buat dan aktifkan virtual environment:
   ```powershell
   python -m venv env ; .\env\Scripts\Activate.ps1
   # Atau di Linux/Mac: source env/bin/activate
   ```

2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup Database:
   - Pastikan MySQL berjalan.
   - Buat database sesuai config `.env`.
   - Jalankan migrasi: `alembic upgrade head`

4. Jalankan Server:
   ```bash
   python run_server.py
   # Atau: uvicorn app.main:app --reload
   ```

## Konfigurasi Environment (.env)

Copy .env.example dan buat file `.env` di root folder:



## Struktur Proyek Utama

```
app/
├── core/
│   ├── config.py             # Konfigurasi Environment & DB URI
│   ├── exception_handler.py  # Global Exception Handling
│   └── logging.py            # Konfigurasi Logger
├── db/
│   ├── models/               # Definisi Tabel Database (ORM)
│   │   ├── customer_model.py
│   │   ├── login_model.py 
│   │   ├── portofolio_model.py
│   │   └── transaction_model.py
│   └── database.py           # Config Async Engine & Session
├── middleware/
│   ├── auth_middleware.py    # Middleware Validasi Token Login
│   └── pin_middleware.py     # Middleware Validasi PIN
├── repositories/             # Data Access Layer (CRUD Operation)
│   ├── accounts_repository.py
│   ├── auth_repository.py
│   └── transaction_repository.py
├── routes/
│   └── v1/                   # Endpoints API Version 1
│       ├── accounts_router.py
│       ├── auth_router.py
│       └── transaction_router.py
├── schemas/                  # Pydantic Schemas (Validasi Request/Response)
│   ├── accounts_schema.py
│   ├── add_balance_schema.py
│   ├── auth_schema.py
│   ├── online_schema.py
│   └── overbook_schema.py
├── services/                 # Business Logic Layer
│   ├── accounts_service.py
│   ├── auth_service.py
│   ├── online_service.py
│   └── overbook_service.py
├── utils/                    # Utilities & Helper
│   ├── request_middleware.py # Helper HTTP Request ke Ext Service
│   └── wrapper_response.py   # Standardisasi Response API
└── main.py                   # Entry Point Aplikasi FastAPI
```

## Troubleshooting

- **Error 404 pada Transaction List**: Pastikan user memiliki akun di tabel `portofolio_accounts` dan `start_date`/`end_date` valid.
- **Error Middleware 422**: Payload transaksi mungkin kurang lengkap. Service otomatis melengkapi `transaction_type`, `transaction_bank`, dll sebelum kirim ke middleware.
- **Database Connection Error di Docker**: Pastikan `DB_HOST=db` (nama service di docker-compose), bukan `localhost`.

---
Made with ❤️ by Choco_Mette
