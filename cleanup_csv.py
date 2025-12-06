"""
Script untuk membersihkan data CSV hasil scraping
Memisahkan RAM dan Storage yang ngegabung

Cara pakai: python cleanup_csv.py
"""

import csv
import re

INPUT_FILE = "data/scraped_phones.csv"
OUTPUT_FILE = "data/scraped_phones_cleaned.csv"

def parse_storage_ram(storage_value, ram_value):
    """
    Fungsi untuk memisahkan Storage dan RAM yang ngegabung
    
    Args:
        storage_value: Value dari kolom storage (misal: "256GB 12GB RAM")
        ram_value: Value dari kolom ram (misal: "N/A")
    
    Returns:
        Tuple (storage_cleaned, ram_cleaned)
    """
    # Kalau RAM sudah ada dan bukan N/A, skip
    if ram_value and ram_value != 'N/A':
        return storage_value, ram_value
    
    # Kalau storage kosong atau N/A, skip
    if not storage_value or storage_value == 'N/A':
        return storage_value, ram_value
    
    # Cari pattern: "256GB 12GB RAM" atau "128GB 6GB RAM"
    # Pattern: angka + GB + spasi + angka + GB + RAM
    pattern = r'(\d+(?:\.\d+)?GB)\s+(\d+(?:\.\d+)?GB)\s*RAM'
    match = re.search(pattern, storage_value)
    
    if match:
        # Ditemukan pattern storage + RAM
        storage_clean = match.group(1)  # Misal: "256GB"
        ram_clean = match.group(2)      # Misal: "12GB"
        return storage_clean, ram_clean
    
    # Kalau tidak match, coba pattern lain: "256GB 12GB" (tanpa kata RAM)
    pattern2 = r'(\d+(?:\.\d+)?GB)\s+(\d+(?:\.\d+)?GB)'
    match2 = re.search(pattern2, storage_value)
    
    if match2:
        # Asumsi: yang pertama storage, yang kedua RAM
        storage_clean = match2.group(1)
        ram_clean = match2.group(2)
        return storage_clean, ram_clean
    
    # Kalau tidak ada pattern yang match, return as is
    return storage_value, ram_value

def cleanup_csv():
    """
    Fungsi utama untuk membersihkan CSV
    """
    print("=" * 70)
    print("🧹 COMPARELY - CSV Cleanup Script")
    print("=" * 70)
    print(f"Input: {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print("=" * 70)
    
    cleaned_count = 0
    total_count = 0
    
    try:
        # Baca CSV input
        with open(INPUT_FILE, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            rows = list(reader)
            fieldnames = reader.fieldnames
        
        # Proses setiap row
        cleaned_rows = []
        for row in rows:
            total_count += 1
            
            # Ambil storage dan RAM
            storage_original = row.get('storage', 'N/A')
            ram_original = row.get('ram', 'N/A')
            
            # Parse dan pisahkan
            storage_clean, ram_clean = parse_storage_ram(storage_original, ram_original)
            
            # Update row
            row['storage'] = storage_clean
            row['ram'] = ram_clean
            
            # Track jika ada perubahan
            if storage_clean != storage_original or ram_clean != ram_original:
                cleaned_count += 1
                print(f"✅ {row['name'][:30]:30} | Storage: {storage_original[:20]:20} → {storage_clean:10} | RAM: {ram_original:10} → {ram_clean}")
            
            cleaned_rows.append(row)
        
        # Tulis ke CSV output
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(cleaned_rows)
        
        print("\n" + "=" * 70)
        print(f"✨ SELESAI!")
        print(f"   📊 Total data: {total_count}")
        print(f"   🧹 Data yang dibersihkan: {cleaned_count}")
        print(f"   📁 File output: {OUTPUT_FILE}")
        print("=" * 70)
        print("\n💡 Langkah selanjutnya:")
        print("   1. Cek file cleaned CSV")
        print("   2. Hapus data lama dari database (opsional)")
        print("   3. Import ulang: python import_csv.py data/scraped_phones_cleaned.csv")
        
    except FileNotFoundError:
        print(f"❌ ERROR: File '{INPUT_FILE}' tidak ditemukan!")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    cleanup_csv()
