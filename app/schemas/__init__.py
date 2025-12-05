"""
Schemas package - Pydantic schemas untuk validasi dan serialisasi data

File ini mengumpulkan semua schema dari file terpisah.
Contoh: from app.schemas import Device, Category, DeviceCreate
"""

from .category import Category, CategoryCreate, CategoryBase
from .device import Device, DeviceCreate, DeviceBase
from .benchmark import Benchmark, BenchmarkCreate, BenchmarkBase

# List semua schema yang bisa di-import
__all__ = [
    # Category schemas
    "Category",
    "CategoryCreate",
    "CategoryBase",
    
    # Device schemas
    "Device",
    "DeviceCreate",
    "DeviceBase",
    
    # Benchmark schemas
    "Benchmark",
    "BenchmarkCreate",
    "BenchmarkBase",
]
