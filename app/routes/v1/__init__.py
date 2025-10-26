import importlib
import pkgutil
from fastapi import APIRouter

router_v1 = APIRouter()

# Scan semua modul di direktori ini (app/routes/v1)
package = __name__
package_path = __path__

for _, module_name, is_pkg in pkgutil.iter_modules(package_path):
    # Hanya ambil file yang berakhiran _router.py
    if not is_pkg and module_name.endswith("_router"):
        module = importlib.import_module(f"{package}.{module_name}")
        # pastikan modul punya variabel `router`
        if hasattr(module, "router"):
            router_v1.include_router(module.router)
