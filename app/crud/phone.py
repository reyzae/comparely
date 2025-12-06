from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas

# ==================== READ OPERATIONS ====================

def get_phone(db: Session, phone_id: int) -> Optional[models.Phone]:
    """
    Mengambil 1 phone berdasarkan ID.
    
    Args:
        db: Database session
        phone_id: ID phone yang dicari
    
    Returns:
        Phone object jika ditemukan, None jika tidak ada
    """
    return db.query(models.Phone).filter(models.Phone.id == phone_id).first()


def get_phones(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None
) -> List[models.Phone]:
    """
    Mengambil list phones dengan pagination dan search.
    
    Args:
        db: Database session
        skip: Berapa data yang di-skip (untuk pagination)
        limit: Maksimal berapa data yang diambil
        search: Keyword untuk search berdasarkan nama phone ATAU brand
    
    Returns:
        List of Phone objects
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

def create_phone(db: Session, phone: schemas.PhoneCreate) -> models.Phone:
    """
    Membuat phone baru di database.
    
    Args:
        db: Database session
        phone: Data phone dari request (PhoneCreate schema)
    
    Returns:
        Phone object yang baru dibuat (dengan ID)
    """
    # Convert Pydantic schema ke SQLAlchemy model
    db_phone = models.Phone(**phone.dict())
    
    # Tambahkan ke session
    db.add(db_phone)
    
    # Commit ke database (save permanently)
    db.commit()
    
    # Refresh untuk mendapatkan data terbaru (termasuk ID auto-increment)
    db.refresh(db_phone)
    
    return db_phone


# ==================== UPDATE OPERATIONS ====================

def update_phone(
    db: Session, 
    phone_id: int, 
    phone: schemas.PhoneCreate
) -> Optional[models.Phone]:
    """
    Update data phone yang sudah ada.
    
    Args:
        db: Database session
        phone_id: ID phone yang mau di-update
        phone: Data baru untuk phone
    
    Returns:
        Phone object yang sudah di-update, atau None jika tidak ditemukan
    """
    # Cari phone yang mau di-update
    db_phone = get_phone(db, phone_id)
    
    if db_phone is None:
        return None
    
    # Update semua field dengan data baru
    for key, value in phone.dict().items():
        setattr(db_phone, key, value)
    
    # Commit perubahan
    db.commit()
    db.refresh(db_phone)
    
    return db_phone


# ==================== DELETE OPERATIONS ====================

def delete_phone(db: Session, phone_id: int) -> bool:
    """
    Hapus phone dari database.
    
    Args:
        db: Database session
        phone_id: ID phone yang mau dihapus
    
    Returns:
        True jika berhasil dihapus, False jika tidak ditemukan
    """
    db_phone = get_phone(db, phone_id)
    
    if db_phone is None:
        return False
    
    # Hapus dari database
    db.delete(db_phone)
    db.commit()
    
    return True
