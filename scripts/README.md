# Management Scripts

Các script quản lý hệ thống Smart City IoT.

## 🚀 Quick Start

### Start/Stop Services
```bash
# Start tất cả services
./start.sh

# Stop tất cả services
./scripts/stop.sh

# Restart tất cả services
./scripts/restart.sh

# Fresh start (xóa database + rebuild)
./scripts/fresh-start.sh
```

## 🔨 Build Scripts

### Build tất cả
```bash
./scripts/build.sh
```
Build lại tất cả services (frontend + backend) từ đầu.

### Rebuild Frontend
```bash
./scripts/rebuild-frontend.sh
```
Chỉ rebuild frontend khi thay đổi React code.

### Rebuild Backend
```bash
./scripts/rebuild-backend.sh
```
Chỉ rebuild backend khi thay đổi Python code hoặc thêm packages.

## 📊 Monitoring

### Check Status
```bash
./scripts/status.sh
```
Hiển thị:
- Trạng thái các containers
- Số lượng users trong database
- Health check backend API

### View Logs
```bash
# Logs tất cả services
./scripts/logs.sh

# Logs service cụ thể
./scripts/logs.sh django
./scripts/logs.sh frontend
./scripts/logs.sh postgres
./scripts/logs.sh celery_worker
```

## 🐍 Django Management

### Run Django Commands
```bash
# Migrations
./scripts/django.sh makemigrations
./scripts/django.sh migrate

# Create superuser
./scripts/django.sh createsuperuser

# Django shell
./scripts/django.sh shell

# Collect static files
./scripts/django.sh collectstatic

# Custom commands
./scripts/django.sh <any_django_command>
```

## 💾 Database Management

### Backup Database
```bash
./scripts/backup-db.sh
```
Tạo backup file trong `backups/smartcity_db_YYYYMMDD_HHMMSS.sql`

### Restore Database
```bash
# List backups
./scripts/restore-db.sh

# Restore từ backup cụ thể
./scripts/restore-db.sh backups/smartcity_db_20251128_120000.sql
```

## 📁 Script Files

| Script | Mô tả |
|--------|-------|
| `build.sh` | Build tất cả services |
| `restart.sh` | Restart tất cả services |
| `stop.sh` | Stop tất cả services |
| `fresh-start.sh` | Reset + rebuild + start |
| `rebuild-frontend.sh` | Rebuild chỉ frontend |
| `rebuild-backend.sh` | Rebuild chỉ backend |
| `status.sh` | Check trạng thái hệ thống |
| `logs.sh` | Xem logs |
| `django.sh` | Run Django commands |
| `backup-db.sh` | Backup database |
| `restore-db.sh` | Restore database |

## 🎯 Common Workflows

### Khi thay đổi React code
```bash
./scripts/rebuild-frontend.sh
```

### Khi thay đổi Django code
```bash
./scripts/rebuild-backend.sh
```

### Khi thêm models mới
```bash
./scripts/django.sh makemigrations
./scripts/django.sh migrate
./scripts/restart.sh
```

### Khi thêm packages mới
```bash
# Update requirements.txt
./scripts/rebuild-backend.sh
```

### Khi muốn reset toàn bộ
```bash
./scripts/fresh-start.sh
```

### Trước khi deploy
```bash
# Backup database
./scripts/backup-db.sh

# Check status
./scripts/status.sh
```

## ⚡ Tips

- Tất cả scripts đều có thể chạy từ root directory
- Logs có thể dùng `Ctrl+C` để thoát
- Fresh start sẽ XÓA toàn bộ database!
- Backup định kỳ database trước khi thay đổi lớn
