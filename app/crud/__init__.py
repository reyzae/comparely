"""
CRUD package - Database operations (Create, Read, Update, Delete)

File ini mengumpulkan semua CRUD operations dari file terpisah.

Perbedaan CRUD vs Service:
- CRUD: Operasi database langsung (query, insert, update, delete)
- Service: Business logic yang mungkin pakai beberapa CRUD operations

Contoh import:
    from app.crud import device, category
    
    # Lalu pakai:
    device.get_device(db, device_id=1)
    category.get_categories(db)
"""

from . import device
from . import category
from . import benchmark

__all__ = ["device", "category", "benchmark"]
