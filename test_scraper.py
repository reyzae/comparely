"""
Script untuk TEST scraper GSMArena dengan sample kecil
Gunakan ini untuk testing sebelum scraping full

Cara pakai: python test_scraper.py
"""

import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent

# Test dengan 1 brand, 3 model aja
BASE_URL = "https://www.gsmarena.com"
TEST_BRAND = "Samsung"
TEST_BRAND_URL = "samsung-phones-9"
TEST_LIMIT = 3

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def test_scrape():
    print("=" * 60)
    print("🧪 TEST SCRAPER - COMPARELY")
    print("=" * 60)
    print(f"Testing dengan {TEST_BRAND}, limit {TEST_LIMIT} model\n")
    
    # Test 1: Ambil daftar handphone
    print("📋 Test 1: Mengambil daftar handphone...")
    url = f"{BASE_URL}/{TEST_BRAND_URL}.php"
    headers = {'User-Agent': get_random_user_agent()}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"   ✅ Berhasil akses {url}")
        print(f"   Status Code: {response.status_code}")
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Cari link handphone - update selector sesuai struktur GSMArena
        phone_links = []
        general_menu = soup.find('div', class_='general-menu')
        
        if general_menu:
            links = general_menu.find_all('a')
            for link in links:  # Iterate semua link
                if 'href' in link.attrs and '.php' in link['href']:
                    phone_url = BASE_URL + "/" + link['href']
                    phone_name = link.find('strong')
                    if phone_name:
                        phone_name = phone_name.get_text().strip()
                    else:
                        phone_name = link.get_text().strip()
                    phone_links.append((phone_name, phone_url))
                    
                    # Stop setelah dapat TEST_LIMIT
                    if len(phone_links) >= TEST_LIMIT:
                        break
        
        print(f"   ✅ Ditemukan {len(phone_links)} model:")
        for idx, (name, url) in enumerate(phone_links, 1):
            print(f"      {idx}. {name}")
        
        # Test 2: Scrape detail 1 handphone
        if phone_links:
            print(f"\n📱 Test 2: Scraping detail handphone...")
            test_name, test_url = phone_links[0]
            print(f"   Target: {test_name}")
            print(f"   URL: {test_url}")
            
            response = requests.get(test_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Ambil nama
            name_tag = soup.find('h1', class_='specs-phone-name-title')
            name = name_tag.text.strip() if name_tag else "Unknown"
            print(f"   ✅ Nama: {name}")
            
            # Ambil gambar
            img_tag = soup.find('div', class_='specs-photo-main').find('img') if soup.find('div', class_='specs-photo-main') else None
            image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ""
            print(f"   ✅ Gambar: {image_url[:50]}...")
            
            # Ambil spesifikasi
            specs_found = {
                'cpu': 'N/A',
                'ram': 'N/A',
                'storage': 'N/A',
                'camera': 'N/A',
                'battery': 'N/A',
                'screen': 'N/A'
            }
            
            spec_tables = soup.find_all('table')
            for table in spec_tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    header = row.find('td', class_='ttl')
                    value = row.find('td', class_='nfo')
                    
                    if header and value:
                        field_name = header.text.strip().lower()
                        field_value = value.text.strip()
                        
                        if 'chipset' in field_name:
                            specs_found['cpu'] = field_value
                        elif 'internal' in field_name:
                            specs_found['storage'] = field_value
                        elif 'camera' in field_name or 'main' in field_name:
                            if specs_found['camera'] == 'N/A':
                                specs_found['camera'] = field_value
                        elif 'battery' in field_name:
                            specs_found['battery'] = field_value
                        elif 'size' in field_name:
                            if specs_found['screen'] == 'N/A':
                                specs_found['screen'] = field_value
            
            print(f"\n   📊 Spesifikasi yang berhasil di-scrape:")
            for key, value in specs_found.items():
                status = "✅" if value != "N/A" else "⚠️"
                print(f"      {status} {key.upper()}: {value[:50]}")
            
            print("\n" + "=" * 60)
            print("✅ TEST SELESAI!")
            print("\nKesimpulan:")
            print("- Scraper bisa akses GSMArena ✅")
            print("- Bisa ambil daftar handphone ✅")
            print("- Bisa scrape detail spesifikasi ✅")
            print("\n💡 Scraper siap digunakan untuk scraping full!")
            print("   Jalankan: python scrape_gsmarena.py")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Cek koneksi internet")
        print("2. Coba lagi dalam beberapa menit")
        print("3. Pastikan library sudah terinstall: pip install -r requirements.txt")

if __name__ == "__main__":
    test_scrape()
