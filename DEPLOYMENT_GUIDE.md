# 📦 Panduan Deployment COMPARELY

## 🎯 Arsitektur Deployment

COMPARELY adalah aplikasi **Full-Stack Python** yang menggunakan FastAPI dengan server-side rendering. Karena menggunakan Python backend, **TIDAK BISA** di-upload ke shared hosting biasa (yang hanya support PHP/HTML statis).

### ⚠️ PENTING: Kenapa Tidak Bisa Pakai Shared Hosting?

1. **Shared hosting** biasanya hanya mendukung:
   - HTML/CSS/JavaScript statis
   - PHP
   - Tidak ada akses terminal/command line
   - Tidak bisa install Python packages

2. **COMPARELY membutuhkan**:
   - Python 3.8+
   - FastAPI (web framework Python)
   - SQLite/PostgreSQL database
   - Akses terminal untuk menjalankan `uvicorn`
   - Install dependencies dari `requirements.txt`

---

## 🚀 Opsi Deployment yang Tersedia

### Opsi 1: VPS (Recommended) ✅
Deploy **SELURUH APLIKASI** ke VPS karena ini adalah aplikasi monolithic.

### Opsi 2: Platform Cloud (Alternative) ✅
- **Railway.app** (Free tier tersedia)
- **Render.com** (Free tier tersedia)
- **Heroku** (Paid)
- **PythonAnywhere** (Free tier terbatas)

### ❌ Opsi yang TIDAK BISA:
- Shared hosting (Hostinger, Niagahoster, dll) - Tidak support Python
- Upload file statis ke cPanel - Aplikasi ini butuh Python runtime

---

## 📂 Struktur File untuk VPS Deployment

Jika deploy ke VPS, upload **SEMUA FILE** kecuali yang ada di `.gitignore`:

### ✅ File yang HARUS di-upload ke VPS:

```
comparely/
├── app/                          # ✅ Folder aplikasi utama
│   ├── core/                     # Config & dependencies
│   ├── crud/                     # Database operations
│   ├── models/                   # Database models
│   ├── routers/                  # API & page routes
│   ├── schemas/                  # Data validation
│   ├── services/                 # Business logic (AI, scraping)
│   ├── static/                   # ✅ CSS, JS, Images (Frontend assets)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/                # ✅ HTML templates
│   ├── database.py               # Database connection
│   └── main.py                   # ✅ Entry point aplikasi
│
├── data/                         # ✅ Data CSV (opsional, bisa di-generate ulang)
│   └── scraped_phones.csv
│
├── docs/                         # 📄 Dokumentasi (opsional)
│
├── .env                          # ⚠️ BUAT BARU di VPS (jangan upload yang ada API key!)
├── .env.example                  # ✅ Template untuk .env
├── requirements.txt              # ✅ WAJIB - List dependencies Python
├── init_db.py                    # ✅ Script inisialisasi database
├── import_csv.py                 # ✅ Script import data
├── scrape_gsmarena.py            # ✅ Script scraping (opsional)
└── README.md                     # 📄 Dokumentasi
```

### ❌ File yang TIDAK perlu di-upload:

```
.git/                   # Git repository (tidak perlu)
.venv/                  # Virtual environment (buat baru di VPS)
__pycache__/            # Python cache (auto-generated)
*.pyc                   # Compiled Python files
.env                    # ⚠️ JANGAN upload! Buat baru dengan API key VPS
test_scraper.py         # File testing (tidak perlu di production)
cleanup_csv.py          # Utility script (tidak perlu di production)
rescrape_complete.py    # Utility script (tidak perlu di production)
reset_database.py       # Utility script (tidak perlu di production)
```

---

## 🔧 Langkah Setup di VPS

### 1️⃣ Upload File ke VPS
```bash
# Opsi A: Clone dari GitHub (Recommended)
git clone https://github.com/reyzae/comparely.git
cd comparely

# Opsi B: Upload manual via SFTP/SCP
# Upload semua file kecuali yang ada di .gitignore
```

### 2️⃣ Install Python & Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Buat virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# atau
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Setup Environment Variables
```bash
# Copy template .env
cp .env.example .env

# Edit .env dengan nano/vim
nano .env
```

Isi `.env`:
```env
DATABASE_URL=sqlite:///./comparely.db
AI_API_KEY=your_actual_api_key_here
```

### 4️⃣ Inisialisasi Database
```bash
# Buat database
python init_db.py

# Import data (opsional)
python import_csv.py
```

### 5️⃣ Jalankan Aplikasi

**Development Mode:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Production Mode (dengan Gunicorn):**
```bash
# Install gunicorn
pip install gunicorn

# Jalankan dengan gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 6️⃣ Setup Reverse Proxy (Nginx)
```nginx
# /etc/nginx/sites-available/comparely
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/comparely/app/static;
    }
}
```

### 7️⃣ Setup Systemd Service (Auto-start)
```ini
# /etc/systemd/system/comparely.service
[Unit]
Description=COMPARELY FastAPI Application
After=network.target

[Service]
User=your-username
WorkingDirectory=/path/to/comparely
Environment="PATH=/path/to/comparely/.venv/bin"
ExecStart=/path/to/comparely/.venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

```bash
# Enable & start service
sudo systemctl enable comparely
sudo systemctl start comparely
sudo systemctl status comparely
```

---

## 🌐 Alternatif: Deploy ke Platform Cloud (Tanpa VPS)

### Railway.app (Recommended untuk Pemula)

1. **Push ke GitHub** (sudah dilakukan)
2. **Buat akun di Railway.app**
3. **New Project → Deploy from GitHub**
4. **Pilih repository `comparely`**
5. **Set Environment Variables:**
   - `AI_API_KEY` = your_api_key
   - `DATABASE_URL` = (Railway auto-provide PostgreSQL)
6. **Deploy otomatis!**

### Render.com

1. **Buat akun di Render.com**
2. **New → Web Service**
3. **Connect GitHub repository**
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. **Set Environment Variables**
7. **Deploy!**

---

## 📊 Ringkasan

| Komponen | Lokasi | Keterangan |
|----------|--------|------------|
| **Backend (Python/FastAPI)** | VPS/Cloud Platform | Semua file di folder `app/` |
| **Frontend (HTML/CSS/JS)** | VPS/Cloud Platform | `app/static/` & `app/templates/` |
| **Database** | VPS/Cloud Platform | SQLite file atau PostgreSQL |
| **Static Files** | Served by FastAPI | Tidak perlu CDN terpisah |

### ⚠️ Kesimpulan Penting:

1. **TIDAK BISA** split frontend ke shared hosting karena HTML templates butuh FastAPI untuk render
2. **HARUS** deploy full-stack ke VPS atau cloud platform yang support Python
3. **Semua file** (backend + frontend) jalan di server yang sama
4. **Static files** (CSS/JS/images) di-serve oleh FastAPI melalui `/static` route

---

## 🆘 Troubleshooting

Lihat [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) untuk masalah umum deployment.

## 📞 Bantuan Lebih Lanjut

- **GitHub Issues:** https://github.com/reyzae/comparely/issues
- **Dokumentasi FastAPI:** https://fastapi.tiangolo.com/deployment/
- **Dokumentasi Uvicorn:** https://www.uvicorn.org/deployment/
