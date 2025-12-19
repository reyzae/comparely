"""
Script untuk recreate tabel users dan roles
HATI-HATI: Ini akan menghapus semua data users dan roles yang ada!
"""

from app.database import engine
from app.models import User, Role, Base
from sqlalchemy import text

def recreate_user_tables():
    """Drop dan recreate tabel users dan roles"""
    
    print("="*60)
    print("RECREATE USER & ROLE TABLES")
    print("="*60)
    
    with engine.connect() as conn:
        try:
            # Drop tabel users dulu (karena ada foreign key ke roles)
            print("\n1. Dropping table 'users'...")
            conn.execute(text("DROP TABLE IF EXISTS users"))
            conn.commit()
            print("   ✅ Table 'users' dropped")
            
            # Drop tabel roles
            print("\n2. Dropping table 'roles'...")
            conn.execute(text("DROP TABLE IF EXISTS roles"))
            conn.commit()
            print("   ✅ Table 'roles' dropped")
            
        except Exception as e:
            print(f"   ⚠️  Error dropping tables: {e}")
    
    # Recreate tables menggunakan SQLAlchemy
    print("\n3. Creating tables from models...")
    
    # Hanya create tabel User dan Role
    User.__table__.create(engine, checkfirst=True)
    Role.__table__.create(engine, checkfirst=True)
    
    print("   ✅ Tables created successfully")
    
    print("\n" + "="*60)
    print("DONE! Tabel users dan roles sudah di-recreate")
    print("="*60)
    print("\nSekarang jalankan: python create_sample_users.py")
    print("untuk membuat sample data")
    print("="*60)

if __name__ == "__main__":
    import sys
    
    # Konfirmasi dulu
    print("\n⚠️  WARNING: Script ini akan menghapus SEMUA data users dan roles!")
    confirm = input("Apakah Anda yakin? (ketik 'yes' untuk lanjut): ")
    
    if confirm.lower() == 'yes':
        recreate_user_tables()
    else:
        print("Dibatalkan.")
        sys.exit(0)
