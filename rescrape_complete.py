"""
Script untuk scraping ULANG dengan filter data lengkap
Hanya ambil handphone yang datanya complete (no N/A)

Cara pakai: python rescrape_complete.py
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from fake_useragent import UserAgent

# Import fungsi dari scraper utama
import sys
sys.path.append('.')
from scrape_gsmarena import (
    BASE_URL, BRANDS, get_random_user_agent, 
    scrape_phone_list, scrape_phone_details, is_data_complete
)

OUTPUT_FILE = "data/complete_phones.csv"

# Naikkan limit per brand karena banyak yang akan di-skip
MODELS_TO_SCRAPE = 40  # Scrape 40, harapan dapat 20 yang lengkap

def main():
    print("=" * 70)
    print("🚀 COMPARELY - Complete Data Only Scraper")
    print("=" * 70)
    print(f"Target: Hanya data LENGKAP (no N/A)")
    print(f"Scraping: {MODELS_TO_SCRAPE} model per brand")
    print(f"Brands: {', '.join(BRANDS.keys())}")
    print("=" * 70)
    
    all_phones = []
    stats = {
        'total_scraped': 0,
        'complete': 0,
        'skipped': 0
    }
    
    for brand_name, brand_url in BRANDS.items():
        print(f"\n📱 Memproses brand: {brand_name}")
        
        # Ambil daftar handphone (lebih banyak dari target)
        phone_urls = scrape_phone_list(brand_name, brand_url)
        
        # Extend list jika perlu (scrape lebih banyak halaman)
        phone_urls = phone_urls[:MODELS_TO_SCRAPE]
        
        brand_complete = 0
        
        for idx, phone_url in enumerate(phone_urls, 1):
            print(f"   [{idx}/{len(phone_urls)}] Scraping: {phone_url.split('/')[-1]}")
            
            phone_data = scrape_phone_details(phone_url, brand_name)
            stats['total_scraped'] += 1
            
            if phone_data and is_data_complete(phone_data):
                all_phones.append(phone_data)
                brand_complete += 1
                stats['complete'] += 1
                print(f"      ✅ {phone_data['name']} - COMPLETE")
            else:
                stats['skipped'] += 1
                if phone_data:
                    missing = []
                    for f in ['camera', 'battery', 'ram', 'storage']:
                        if phone_data.get(f) == 'N/A':
                            missing.append(f)
                    print(f"      ⏭️  SKIP - Missing: {', '.join(missing)}")
            
            # Delay
            time.sleep(random.uniform(1, 3))
        
        print(f"\n   📊 {brand_name}: {brand_complete} complete dari {len(phone_urls)} scraped")
    
    # Save
    if all_phones:
        fieldnames = [
            'name', 'brand', 'category_id', 'cpu', 'gpu', 'ram', 
            'storage', 'camera', 'battery', 'screen', 'release_year', 
            'price', 'image_url', 'source_data'
        ]
        
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_phones)
        
        print("\n" + "=" * 70)
        print(f"✨ SELESAI!")
        print(f"   📊 Total scraped: {stats['total_scraped']}")
        print(f"   ✅ Complete: {stats['complete']}")
        print(f"   ⏭️  Skipped: {stats['skipped']}")
        print(f"   📁 File: {OUTPUT_FILE}")
        print("=" * 70)
        print("\n💡 Langkah selanjutnya:")
        print("   python import_csv.py data/complete_phones.csv")
    else:
        print("\n❌ Tidak ada data complete yang ditemukan!")

if __name__ == "__main__":
    main()
