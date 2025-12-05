"""
Models package - Database models (SQLAlchemy ORM)

File ini mengumpulkan semua model dari file terpisah agar mudah di-import.
Contoh: from app.models import Device, Category, Benchmark
"""

from ..database import Base
from .category import Category
from .device import Device
from .benchmark import Benchmark

# List semua model yang bisa di-import
__all__ = ["Base", "Category", "Device", "Benchmark"]
