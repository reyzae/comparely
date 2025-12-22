# 🎯 CARA CEPAT DEPLOY KE VPS

## Informasi VPS Anda:
- IP: 160.187.210.125
- User: root
- Pass: [PASSWORD_VPS]

---

## 🚀 LANGKAH TERCEPAT (5 MENIT)

### 1. Connect ke VPS
```bash
ssh root@160.187.210.125
```
Masukkan password: `[PASSWORD_VPS]`

### 2. Copy-Paste Command Ini

```bash
BACKUP_DATE=$(date +%Y%m%d_%H%M%S) && \
mkdir -p /root/backups && \
if [ -d "/root/comparely" ]; then \
    tar -czf /root/backups/comparely_backup_$BACKUP_DATE.tar.gz -C /root comparely && \
    mv /root/comparely /root/comparely_old_$BACKUP_DATE; \
fi && \
apt update -y && \
apt install -y python3 python3-pip python3-venv nginx git curl && \
cd /root && \
git clone https://github.com/reyzae/comparely.git && \
cd /root/comparely && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt && \
pip install gunicorn && \
cp .env.example .env && \
echo "✅ DEPLOYMENT SELESAI!" && \
echo "" && \
echo "NEXT STEPS:" && \
echo "1. Edit .env: nano .env" && \
echo "2. Init DB: python scripts/utils/init_db.py" && \
echo "3. Create admin: python scripts/utils/create_admin_simple.py" && \
echo "4. Test: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"
```

### 3. Setelah Selesai

**Edit .env:**
```bash
nano .env
```
Update `SECRET_KEY` dengan generate:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Initialize Database:**
```bash
source .venv/bin/activate
python scripts/utils/init_db.py
```

**Create Admin:**
```bash
python scripts/utils/create_admin_simple.py
```

**Test:**
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Buka: `http://160.187.210.125:8000`

---

## 📁 File-File yang Sudah Dibuat

1. **DEPLOYMENT_PACKAGE.md** ⭐ - Summary lengkap
2. **QUICK_DEPLOY.md** - Panduan detail 3 metode
3. **COPY_PASTE_COMMANDS.txt** - Command siap pakai
4. **quick_deploy.sh** - Script otomatis
5. **vps_commands.sh** - Setup script
6. **deploy_to_vps.ps1** - PowerShell helper
7. **auto_deploy_ssh.ps1** - Auto deploy
8. **connect_vps.ps1** - Quick connect

---

## 🔥 Setup Production (Opsional)

Lihat file **QUICK_DEPLOY.md** untuk:
- Setup Systemd Service
- Setup Nginx
- Setup SSL
- Setup Firewall

---

## 📦 Backup

Backup otomatis disimpan di: `/root/backups/`

List backup:
```bash
ls -lh /root/backups/
```

---

**SELAMAT DEPLOY! 🚀**
