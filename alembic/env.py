# alembic/env.py
import asyncio
import urllib.parse
import configparser
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.db.models import customer_model, login_model, mutation_model, portofolio_model, transaction_model

from app.db.database import Base
from app.core.config import settings

# Ambil konfigurasi Alembic aktif
config = context.config

# Nonaktifkan interpolation untuk mencegah error karakter khusus seperti % atau @
config.file_config = configparser.ConfigParser(interpolation=None)

# Konfigurasi logging (opsional, dari alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata dari model utama
target_metadata = Base.metadata

# Encode password (agar aman untuk karakter spesial)
encoded_password = urllib.parse.quote_plus(settings.DB_PASSWORD)

# Buat URL sinkron (gunakan pymysql agar Alembic bisa jalan)
SYNC_DB_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{encoded_password}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Override sqlalchemy.url dari alembic.ini
config.set_main_option("sqlalchemy.url", SYNC_DB_URL)


def run_migrations_offline():
    """Mode offline (tanpa koneksi DB langsung)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Mode online (dengan koneksi DB langsung)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
