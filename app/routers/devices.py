from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.deps import get_db  # Import get_db dari core.deps (centralized)
from ..crud import device as device_crud
from .. import schemas

# Membuat router (kelompok URL) untuk devices
router = APIRouter(
    prefix="/devices",
    tags=["devices"]
)



# API: Tambah Device Baru
@router.post("/", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    return device_crud.create_device(db=db, device=device)

# API: Ambil Semua Device (bisa cari nama)
@router.get("/", response_model=List[schemas.Device])
def read_devices(skip: int = 0, limit: int = 100, search: str = None, db: Session = Depends(get_db)):
    devices = device_crud.get_devices(db, skip=skip, limit=limit, search=search)
    return devices

# API: Autocomplete Search (untuk suggestions)
@router.get("/autocomplete")
def autocomplete_devices(query: str, db: Session = Depends(get_db)):
    """
    Endpoint untuk autocomplete search.
    
    Cara kerja:
    - User ketik di search bar (minimal 2 karakter)
    - Frontend kirim request ke endpoint ini
    - Return list device yang namanya match dengan query
    - Frontend tampilkan sebagai dropdown suggestions
    
    Contoh:
    - Query: "galaxy" → Return: Galaxy S24, Galaxy S23, dll
    - Query: "iphone" → Return: iPhone 14, iPhone 13, dll
    """
    
    # Cari device yang namanya mengandung query (case insensitive)
    # Limit 5 hasil agar tidak terlalu banyak
    devices = device_crud.get_devices(db, search=query, limit=5)
    
    # Return hanya data yang diperlukan (id dan name)
    # Biar response lebih ringan
    return [
        {"id": device.id, "name": device.name, "brand": device.brand}
        for device in devices
    ]


# API: Ambil Detail Device per ID
@router.get("/{device_id}", response_model=schemas.Device)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = device_crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device
