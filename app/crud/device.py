from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas

# ==================== READ OPERATIONS ====================

def get_device(db: Session, device_id: int) -> Optional[models.Phone]:
    """
    Mengambil 1 device berdasarkan ID.
    
    Args:
        db: Database session
        device_id: ID device yang dicari
    
    Returns:
        Device object jika ditemukan, None jika tidak ada
    """
    return db.query(models.Phone).filter(models.Phone.id == device_id).first()


def get_devices(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None
) -> List[models.Phone]:
    """
    Mengambil list devices dengan pagination dan search.
    
    Args:
        db: Database session
        skip: Berapa data yang di-skip (untuk pagination)
        limit: Maksimal berapa data yang diambil
        search: Keyword untuk search berdasarkan nama device ATAU brand
    
    Returns:
        List of Device objects
    """
    query = db.query(models.Phone)
    
    # Jika ada keyword search, filter berdasarkan nama ATAU brand
    # Menggunakan ilike() untuk case-insensitive search
    # Contoh: "samsung", "Samsung", "SAMSUNG" semua akan match
    if search:
        search_pattern = f"%{search}%"
        search_filter = (
            models.Phone.name.ilike(search_pattern) | 
            models.Phone.brand.ilike(search_pattern)
        )
        query = query.filter(search_filter)
    
    return query.offset(skip).limit(limit).all()


# ==================== CREATE OPERATIONS ====================

def create_device(db: Session, device: schemas.PhoneCreate) -> models.Phone:
    """
    Membuat device baru di database.
    
    Args:
        db: Database session
        device: Data device dari request (DeviceCreate schema)
    
    Returns:
        Device object yang baru dibuat (dengan ID)
    """
    # Convert Pydantic schema ke SQLAlchemy model
    db_device = models.Phone(**device.dict())
    
    # Tambahkan ke session
    db.add(db_device)
    
    # Commit ke database (save permanently)
    db.commit()
    
    # Refresh untuk mendapatkan data terbaru (termasuk ID auto-increment)
    db.refresh(db_device)
    
    return db_device


# ==================== UPDATE OPERATIONS ====================

def update_device(
    db: Session, 
    device_id: int, 
    device: schemas.PhoneCreate
) -> Optional[models.Phone]:
    """
    Update data device yang sudah ada.
    
    Args:
        db: Database session
        device_id: ID device yang mau di-update
        device: Data baru untuk device
    
    Returns:
        Device object yang sudah di-update, atau None jika tidak ditemukan
    """
    # Cari device yang mau di-update
    db_device = get_device(db, device_id)
    
    if db_device is None:
        return None
    
    # Update semua field dengan data baru
    for key, value in device.dict().items():
        setattr(db_device, key, value)
    
    # Commit perubahan
    db.commit()
    db.refresh(db_device)
    
    return db_device


# ==================== DELETE OPERATIONS ====================

def delete_device(db: Session, device_id: int) -> bool:
    """
    Hapus device dari database.
    
    Args:
        db: Database session
        device_id: ID device yang mau dihapus
    
    Returns:
        True jika berhasil dihapus, False jika tidak ditemukan
    """
    db_device = get_device(db, device_id)
    
    if db_device is None:
        return False
    
    # Hapus dari database
    db.delete(db_device)
    db.commit()
    
    return True
