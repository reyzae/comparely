"""
Router untuk admin/management functions
Termasuk reset database, dll

Author: Kelompok COMPARELY
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Device, Benchmark
from sqlalchemy import text

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.post("/reset-database")
def reset_database(db: Session = Depends(get_db)):
    """
    Reset database - hapus semua devices dan benchmarks
    
    ⚠️ HATI-HATI: Ini akan menghapus SEMUA data!
    """
    try:
        # Hitung data sebelum dihapus
        device_count = db.query(Device).count()
        benchmark_count = db.query(Benchmark).count()
        
        # Hapus benchmarks dulu (foreign key)
        db.query(Benchmark).delete()
        
        # Hapus devices
        db.query(Device).delete()
        
        # Commit perubahan
        db.commit()
        
        # Reset auto increment (opsional)
        try:
            db.execute(text("ALTER TABLE devices AUTO_INCREMENT = 1"))
            db.execute(text("ALTER TABLE benchmarks AUTO_INCREMENT = 1"))
            db.commit()
        except:
            pass  # Tidak masalah jika gagal
        
        return {
            "success": True,
            "message": "Database berhasil direset",
            "deleted": {
                "devices": device_count,
                "benchmarks": benchmark_count
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
def get_database_stats(db: Session = Depends(get_db)):
    """
    Dapatkan statistik database
    """
    try:
        device_count = db.query(Device).count()
        benchmark_count = db.query(Benchmark).count()
        
        # Hitung per brand
        brands = db.query(Device.brand).distinct().all()
        brand_stats = {}
        for (brand,) in brands:
            count = db.query(Device).filter(Device.brand == brand).count()
            brand_stats[brand] = count
        
        return {
            "total_devices": device_count,
            "total_benchmarks": benchmark_count,
            "brands": brand_stats
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
