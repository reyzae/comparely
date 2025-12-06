"""
CRUD package - Database operations (Create, Read, Update, Delete)

File ini mengumpulkan semua CRUD operations dari file terpisah.

Perbedaan CRUD vs Service:
- CRUD: Operasi database langsung (query, insert, update, delete)
- Service: Business logic yang mungkin pakai beberapa CRUD operations

Contoh import:
    from app.crud import phone, category
    
    # Lalu pakai:
    phone.get_phone(db, phone_id=1)
    category.get_categories(db)
"""

from . import phone
from . import category

__all__ = ["phone", "category"]
