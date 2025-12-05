# 📱 COMPARELY - Aplikasi Perbandingan Perangkat Teknologi

![CI Status](https://github.com/reyzae/comparely/workflows/CI%20-%20COMPARELY/badge.svg)

Aplikasi web untuk membandingkan dan memberikan rekomendasi perangkat teknologi (smartphone & laptop) berbasis **Python FastAPI** dan **MySQL**.

---

## 🎯 Fitur Utama

1. **🌐 Web Interface**: Antarmuka web modern dan responsif
2. **🔍 Pencarian Perangkat**: Cari perangkat berdasarkan nama atau brand
3. **⚖️ Perbandingan**: Bandingkan 2 perangkat secara detail
4. **🤖 AI Comparison**: Analisis perbandingan menggunakan AI
5. **🎯 Rekomendasi**: Dapatkan rekomendasi perangkat sesuai budget dan kebutuhan
6. **🧠 AI Recommendation**: Rekomendasi personal dari AI berdasarkan use case
7. **📊 Benchmark**: Data performa perangkat
8. **🏷️ Kategori**: Manajemen kategori perangkat
9. **📥 CSV Import**: Import data perangkat dari file CSV

---

## 🛠️ Teknologi

### Backend
- **Python 3.11+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM untuk database
- **Pydantic** - Validasi data
- **Uvicorn** - ASGI server
- **MySQL** - Database relational
- **AI** - AI analysis & recommendations

### Frontend
- **Jinja2** - Template engine untuk HTML
- **Vanilla CSS** - Styling dengan design system
- **Responsive Design** - Mobile-friendly layout

---

## 📁 Struktur Project

```
comparely/
├── app/
│   ├── core/              # Core utilities (config, dependencies)
│   ├── crud/              # CRUD operations (devices, categories)
│   ├── models/            # SQLAlchemy models (Device, Category, Benchmark)
│   ├── routers/           # API endpoints (devices, compare, recommendation)
│   ├── schemas/           # Pydantic schemas (request/response)
│   ├── services/          # Business logic (comparison, AI services)
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # Jinja2 templates (HTML)
│   ├── database.py        # Database connection
│   └── main.py            # FastAPI application entry point
├── data/
│   └── devices.csv        # Sample CSV data for import
├── docs/
│   ├── flowcharts.md      # Mermaid flowcharts & diagrams
│   ├── api_ai_endpoints.md  # AI endpoints documentation
│   ├── import_guide.md    # CSV import guide
│   └── troubleshooting.md # Common issues & solutions
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI workflow
├── import_csv.py          # Script untuk import data dari CSV
├── init_db.py             # Script inisialisasi database
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── TROUBLESHOOTING.md     # Panduan troubleshooting
└── README.md              # Dokumentasi ini
```

### Mapping Proposal → Codebase

| Proposal Section | Implementation | Location |
|-----------------|----------------|----------|
| FastAPI Backend | ✅ Implemented | `app/main.py`, `app/routers/` |
| MySQL Database | ✅ Implemented | `app/database.py`, `app/models/` |
| Device CRUD | ✅ Implemented | `app/crud/device.py` |
| Comparison Service | ✅ Implemented | `app/services/comparison_service.py` |
| AI Integration (AI) | ✅ Implemented | `app/services/ai_service.py`, `app/services/AI_service.py` |
| Recommendation Engine | ✅ Implemented | `app/services/recommendation_service.py` |
| CSV Import | ✅ Implemented | `import_csv.py` |
| Flowcharts & Documentation | ✅ Implemented | `docs/flowcharts.md` |
| **Web Frontend** | ✅ **Implemented** | `app/templates/`, `app/static/`, `app/routers/frontend.py` |

---

## 🚀 Cara Menjalankan

### 1. Clone Repository
```bash
git clone https://github.com/reyzae/comparely.git
cd comparely
```

### 2. Setup Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
# Buat database MySQL bernama 'comparely'
mysql -u root -p -e "CREATE DATABASE comparely;"

# Copy .env.example ke .env dan sesuaikan konfigurasi
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=mysql+mysqlconnector://root:password@localhost/comparely
AI_API_KEY=your_AI_API_KEY_here
```

### 5. Inisialisasi Database
```bash
python init_db.py
```

### 6. Import Data (Opsional)
```bash
# Import dari CSV
python import_csv.py data/devices.csv
```

### 7. Jalankan Server
```bash
uvicorn app.main:app --reload
```

Server akan berjalan di: `http://localhost:8000`

### 8. Akses Web Interface

Setelah server berjalan, buka browser dan akses:

- **Homepage**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **API Documentation (ReDoc)**: http://localhost:8000/redoc

---

## 📥 CSV Import Guide

### Format CSV
File CSV harus memiliki header berikut:
```csv
name,brand,category_id,cpu,gpu,ram,storage,camera,battery,screen,release_year,price,image_url,source_data
```

### Contoh Data
```csv
iPhone 15 Pro,Apple,1,A17 Pro,Apple GPU,8GB,256GB,48MP + 12MP,3274 mAh,6.1" OLED,2023,12000000,https://...,GSMArena
Samsung Galaxy S24,Samsung,1,Snapdragon 8 Gen 3,Adreno 750,8GB,256GB,50MP + 12MP,4000 mAh,6.2" AMOLED,2024,11000000,https://...,GSMArena
```

### Cara Import
```bash
# Default: membaca dari data/devices.csv
python import_csv.py

# Custom path
python import_csv.py path/to/your/file.csv
```

### Validasi
Script akan otomatis:
- ✅ Validasi field wajib (name, brand, category_id, price)
- ✅ Konversi tipe data (integer, decimal)
- ✅ Handle missing values dengan default 'N/A'
- ✅ Menampilkan summary hasil import

---

## 🧪 Testing & CI

### Run Tests Locally
```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing
```

### Continuous Integration
Project ini menggunakan **GitHub Actions** untuk CI/CD:

- ✅ Automated testing pada setiap push/PR
- ✅ Python 3.11 & 3.12 compatibility check
- ✅ Code linting dengan flake8
- ✅ Model validation
- ✅ Syntax validation untuk import_csv.py

Lihat workflow di: `.github/workflows/ci.yml`

---

## 📖 API Documentation

Setelah server berjalan, akses dokumentasi interaktif:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoint Utama

#### Devices
- `GET /devices/` - List semua devices
- `GET /devices/{id}` - Detail device
- `GET /devices/search?query=...` - Cari device

#### Comparison
- `POST /compare/` - Bandingkan 2 devices (rule-based)
- `POST /compare/ai` - Bandingkan dengan AI analysis

#### Recommendation
- `GET /recommendation/` - Rekomendasi devices
- `POST /recommendation/ai` - Rekomendasi dengan AI

#### Categories
- `GET /categories/` - List semua kategori

---

## 📚 Dokumentasi Lengkap

- [Flowcharts & Diagrams](docs/flowcharts.md) - Visual sistem architecture
- [AI Endpoints Guide](docs/api_ai_endpoints.md) - Panduan AI features
- [CSV Import Guide](docs/import_guide.md) - Detail import process
- [Troubleshooting](TROUBLESHOOTING.md) - Panduan mengatasi masalah umum

---

## 👥 Tim COMPARELY

**Ketua**: Reyza Wirakusuma [17250107]

**Anggota**:
- Rachmat Muhaimin Rustam [17250381]
- Tegar Apdiansyah [17250651]
- Abdul Khair [17250610]
- Rofik Rokhmattullah [17250705]

---

## 📄 Lisensi

Project ini dibuat untuk keperluan tugas kuliah **Dasar Pemrograman**.

---

## 📚 Resources untuk Belajar

### Backend Development

#### FastAPI
- **Official Documentation**: https://fastapi.tiangolo.com/
- **Tutorial Lengkap**: https://fastapi.tiangolo.com/tutorial/
- **Advanced User Guide**: https://fastapi.tiangolo.com/advanced/

#### SQLAlchemy & Database
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/
- **SQLAlchemy ORM Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **MySQL Documentation**: https://dev.mysql.com/doc/

#### Python Best Practices
- **PEP 8 Style Guide**: https://pep8.org/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html
- **Pydantic Documentation**: https://docs.pydantic.dev/

### Frontend Development

#### Jinja2 Templates
- **Jinja2 Documentation**: https://jinja.palletsprojects.com/
- **Template Designer Documentation**: https://jinja.palletsprojects.com/en/3.1.x/templates/
- **FastAPI with Templates**: https://fastapi.tiangolo.com/advanced/templates/

#### CSS & Design
- **CSS Tricks - Complete Guide to Grid**: https://css-tricks.com/snippets/css/complete-guide-grid/
- **CSS Tricks - Complete Guide to Flexbox**: https://css-tricks.com/snippets/css/a-guide-to-flexbox/
- **MDN CSS Documentation**: https://developer.mozilla.org/en-US/docs/Web/CSS
- **Web.dev - Responsive Design**: https://web.dev/responsive-web-design-basics/

#### Design Systems
- **CSS Variables Guide**: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties
- **Material Design**: https://material.io/design
- **Design Principles**: https://principles.design/

### AI Integration

#### AI
- **AI API Documentation**: https://docs.x.ai/
- **API Console**: https://console.x.ai/

### Tools & Workflow

#### Git & GitHub
- **Git Documentation**: https://git-scm.com/doc
- **GitHub Actions**: https://docs.github.com/en/actions

#### Development Tools
- **VS Code**: https://code.visualstudio.com/docs
- **Postman (API Testing)**: https://learning.postman.com/

### Tutorial Bahasa Indonesia

#### Python & FastAPI
- **Python ID**: https://www.python.or.id/
- **Dicoding - Belajar Python**: https://www.dicoding.com/academies/86

#### Web Development
- **Petani Kode - HTML & CSS**: https://www.petanikode.com/html-dasar/
- **Web Programming UNPAS (YouTube)**: https://www.youtube.com/c/WebProgrammingUNPAS

---

**Dibuat oleh Tim COMPARELY** | 2025

