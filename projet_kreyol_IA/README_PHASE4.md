# 🇭🇹 Pwojè Kreyòl IA - Phase 4: Scale & Deploy

## Version 5.0 - Enterprise Ready

---

## 🚀 Quick Start

### Option 1: Docker (Recommandé)

```bash
# Déploiement automatique
./deploy.sh production

# Ou manuellement
docker-compose up -d

# Accéder aux services
# API:  http://localhost:8000
# Docs: http://localhost:8000/docs
# GUI:  http://localhost:8501
```

### Option 2: Local

```bash
# Installer dépendances
pip install -r requirements.txt

# Démarrer API
python start_api.py

# Dans un autre terminal, démarrer GUI
streamlit run app.py
```

---

## 📡 API REST

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/translate` | POST | Traduire du texte |
| `/api/v1/audio` | POST | Générer audio |
| `/api/v1/process` | POST | Traiter document PDF/TXT/DOCX |
| `/api/v1/tasks/{id}` | GET | Statut d'une tâche |
| `/api/v1/tasks` | GET | Liste des tâches |
| `/api/v1/download/{id}/{type}` | GET | Télécharger résultat |

### Exemples

**Translation:**
```bash
curl -X POST http://localhost:8000/api/v1/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "target_lang": "ht",
    "enable_cache": true
  }'
```

**Document Processing:**
```bash
curl -X POST http://localhost:8000/api/v1/process \
  -F "file=@document.pdf" \
  -F "target_lang=ht" \
  -F "generate_audio=true"
```

**Python Client:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/translate",
    json={"text": "Hello world", "target_lang": "ht"}
)

print(response.json())
```

---

## 🐋 Docker

### Build

```bash
docker build -t kreyol-ai:latest .
```

### Run

```bash
# Single container
docker run -p 8000:8000 -p 8501:8501 kreyol-ai

# With docker-compose (recommended)
docker-compose up -d
```

### Manage

```bash
# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart

# Scale API
docker-compose up -d --scale api=3
```

---

## 📊 Database

### Task Management

```python
from src.database import DatabaseManager

db = DatabaseManager()

# Create task
task = db.create_task("task123", "translation")

# Update
db.update_task("task123", status="completed")

# Get
task = db.get_task("task123")

# List
tasks = db.list_tasks(limit=50)

# Statistics
stats = db.get_statistics()
```

---

## 📈 Monitoring

### Metrics

```python
from src.monitoring import get_monitor

monitor = get_monitor()

# Record metrics
monitor.record_translation(...)
monitor.record_audio_generation(...)

# Get summary
summary = monitor.get_summary()
# {
#   "total_requests": 1250,
#   "avg_translation_duration": 2.1,
#   "cache_hit_rate": 67.3,
#   "total_errors": 3
# }
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```bash
# Directories
DATA_DIR=data
OUTPUT_DIR=output
CACHE_DIR=cache
LOG_DIR=logs

# Translation
TRANSLATION_MODEL=facebook/m2m100_418M
TARGET_LANGUAGE=ht
MAX_CHUNK_SIZE=1000
TRANSLATION_MAX_WORKERS=3

# TTS
TTS_LANGUAGE=ht
TTS_SLOW_SPEED=false

# Limits
MAX_PDF_PAGES=500
MAX_PDF_SIZE_MB=50
```

---

## 🚢 Deployment

### Production Checklist

- [ ] Configure environment variables
- [ ] Set up reverse proxy (Nginx)
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Test health endpoints
- [ ] Load testing

### Cloud Providers

**Heroku:**
```bash
heroku create kreyol-ai
heroku container:push web
heroku container:release web
```

**AWS:**
```bash
# Use ECS or EC2 with Docker
aws ecr create-repository --repository-name kreyol-ai
docker tag kreyol-ai:latest <aws-account>.dkr.ecr.<region>.amazonaws.com/kreyol-ai
docker push <aws-account>.dkr.ecr.<region>.amazonaws.com/kreyol-ai
```

**DigitalOcean:**
```bash
# Use App Platform or Droplet with Docker
doctl apps create --spec app.yaml
```

---

## 🔬 Testing

### Run Tests

```bash
# All tests
pytest tests/

# With coverage
pytest tests/ --cov=src --cov-report=html

# API tests
pytest tests/test_api.py -v
```

### CI/CD

GitHub Actions automatically:
- ✅ Run tests on each push
- ✅ Build Docker image
- ✅ Security scanning
- ✅ Deploy to production (main branch)

---

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (Swagger)
- **API Docs**: http://localhost:8000/redoc (ReDoc)
- **Complete Guide**: PHASE4_COMPLETE.md
- **Changelog**: CHANGELOG.md

---

## 🎯 Features Phase 4

- ✅ RESTful API (FastAPI)
- ✅ SQLite Database
- ✅ Docker Containerization
- ✅ Automated Deployment
- ✅ CI/CD Pipeline
- ✅ Performance Monitoring
- ✅ Task Tracking
- ✅ Health Checks
- ✅ API Documentation
- ✅ Production Ready

---

## 🔮 Roadmap

### Phase 5 (Optional)
- Kubernetes
- Redis cache
- PostgreSQL
- Message queue
- Load balancer

### Phase 6 (Optional)
- Multi-tenancy
- OAuth2
- RBAC
- Audit logs
- Encryption

---

## 🆘 Support

- **Issues**: GitHub Issues
- **Docs**: /docs endpoint
- **Health**: /health endpoint

---

## 📄 License

MIT License

---

**Fèt ak ❤️ pou kominote Kreyòl Ayisyen** 🇭🇹

**Version**: 5.0  
**Status**: Production Ready  
**Date**: 12 octobre 2025


