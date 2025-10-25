# 🚀 Production-Ready Guide - Kreyòl IA V2

## 📋 Overview

Platfòm Kreyòl IA la te amelyore ak features pwofesyonèl pou deployment nan production. Vèsyon V2 la gen sekirite, monitoring, ak robustness amelyore.

---

## ✨ Nouvo Features V2

### 1. 🔒 **Sekirite Amelyore**

#### Configuration Sentrialize (`src/app_config.py`)
- ✅ Environment variable sipò
- ✅ Validation pou production
- ✅ Secret key management
- ✅ CORS konfigirasyon sekirize

#### File Upload Validation (`src/file_validator.py`)
- ✅ Extension validation (bloke fichye danjere)
- ✅ MIME type verification
- ✅ File size limits
- ✅ Content scanning pou exploit
- ✅ Path traversal protection
- ✅ SHA256 hashing pou tracking

#### Security Features:
```python
# Pa gen plis wildcard CORS!
allow_origins=["http://localhost:3000", "https://yourdomain.com"]

# Secret key nan environment
JWT_SECRET_KEY=your-secret-key-from-env

# File validation robus
- Block .exe, .bat, .sh, ak lòt fichye danjere
- Verifye MIME type
- Scan pou suspicious content
```

### 2. 📊 **Monitoring & Observability**

#### Prometheus Metrics (`src/metrics.py`)
- ✅ HTTP request metrics (count, duration, in-progress)
- ✅ Translation metrics (count, duration, characters)
- ✅ Audio generation metrics
- ✅ File processing metrics
- ✅ Cache hit/miss rates
- ✅ Error tracking
- ✅ Custom application metrics

#### Health Checks (`src/health.py`)
- ✅ Comprehensive health checks
- ✅ Kubernetes-style probes (liveness, readiness, startup)
- ✅ Component-level monitoring (database, translator, storage, cache)
- ✅ Disk space monitoring
- ✅ Response time tracking

### 3. 🎯 **Request Tracking**

- ✅ Unique request IDs (UUID)
- ✅ Request ID nan response headers
- ✅ Structured logging ak request context
- ✅ Error messages ak request ID pou debugging

### 4. 🛡️ **Error Handling Amelyore**

- ✅ Granular exception handling
- ✅ Professional error responses
- ✅ Request ID tracking nan errors
- ✅ Detailed logging
- ✅ Proper HTTP status codes

---

## 📁 Nouvo Files

### Configuration
- **`config.example.env`** - Template pou environment variables
- **`src/app_config.py`** - Centralized configuration management

### Security
- **`src/file_validator.py`** - Secure file upload validation

### Monitoring
- **`src/metrics.py`** - Prometheus metrics
- **`src/health.py`** - Health check system

### API
- **`api_final_v2.py`** - Production-ready API ak tout nouvo features

### Documentation
- **`PRODUCTION_READY_GUIDE.md`** - Dokiman sa a
- **`SECURITY_GUIDE.md`** - Security best practices (upcoming)

---

## 🔧 Setup & Configuration

### 1. Environment Variables

Kopye `config.example.env` a `.env`:

```bash
cp config.example.env .env
```

Edit `.env` pou konfigire:

```env
# KRITIK: Change sa yo pou production!
JWT_SECRET_KEY=generate-with-python-secrets-token-hex-32
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Optional: Redis pou caching
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_ENABLED=true

# Optional: Sentry pou error tracking
SENTRY_DSN=https://your-sentry-dsn
```

### 2. Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Mete rezilta a nan `.env`:
```env
JWT_SECRET_KEY=your-generated-secret-key-here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

# Pou file validation (MIME type detection)
pip install python-magic-bin  # Windows
# ou
pip install python-magic  # Linux/Mac

# Pou metrics
pip install prometheus-client

# Optional: Redis pou caching
pip install redis
```

### 4. Validate Configuration

```bash
# Test configuration loading
python src/app_config.py

# Should display configuration summary
```

### 5. Run API V2

```bash
# Development
python api_final_v2.py

# Production (with Gunicorn)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api_final_v2:app
```

---

## 🏥 Health Checks

### Endpoints

#### GET `/health`
Full health check ak tout kompozan yo:

```bash
curl http://localhost:8000/health?detailed=true
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-21T12:00:00",
  "uptime_seconds": 3600.5,
  "version": "2.0.0",
  "environment": "production",
  "components": {
    "database": {
      "status": "healthy",
      "message": "Database is operational",
      "response_time_ms": 5.2
    },
    "translator": {
      "status": "healthy",
      "message": "Translator is operational"
    },
    "storage": {
      "status": "healthy",
      "message": "Storage is operational",
      "details": {
        "used_percent": 45.2,
        "free_gb": 50.5
      }
    }
  }
}
```

#### GET `/health/live`
Kubernetes liveness probe:

```bash
curl http://localhost:8000/health/live
```

#### GET `/health/ready`
Kubernetes readiness probe:

```bash
curl http://localhost:8000/health/ready
```

---

## 📊 Metrics

### Prometheus Endpoint

GET `/metrics` - Prometheus-formatted metrics:

```bash
curl http://localhost:8000/metrics
```

### Available Metrics

#### HTTP Metrics:
- `http_requests_total` - Total requests (by method, endpoint, status)
- `http_request_duration_seconds` - Request latency histogram
- `http_requests_in_progress` - Current active requests

#### Translation Metrics:
- `translations_total` - Total translations
- `translation_duration_seconds` - Translation time
- `translation_characters` - Characters translated

#### Audio Metrics:
- `audio_generations_total` - Total audio generations
- `audio_generation_duration_seconds` - Generation time
- `audio_output_duration_seconds` - Audio duration

#### File Metrics:
- `file_upload_size_bytes` - Upload size distribution
- `file_processing_duration_seconds` - Processing time
- `pdf_pages_processed` - PDF page count

#### Cache Metrics:
- `cache_hits_total` - Cache hits
- `cache_misses_total` - Cache misses

#### Error Metrics:
- `errors_total` - Total errors (by type, endpoint)

### Grafana Dashboard

Import metrics nan Grafana pou visualization. Example queries:

```promql
# Request rate
rate(http_requests_total[5m])

# Average response time
rate(http_request_duration_seconds_sum[5m]) 
/ rate(http_request_duration_seconds_count[5m])

# Error rate
rate(errors_total[5m])

# Cache hit rate
rate(cache_hits_total[5m]) 
/ (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))
```

---

## 🔒 Security Best Practices

### 1. Environment Variables

❌ **BAD:**
```python
SECRET_KEY = "my-secret-key"  # Hard-coded!
```

✅ **GOOD:**
```python
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY must be set")
```

### 2. CORS Configuration

❌ **BAD:**
```python
allow_origins=["*"]  # Tou lemonn ka access!
```

✅ **GOOD:**
```python
allow_origins=[
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]
```

### 3. File Upload Validation

✅ **ALWAYS:**
- Validate file extension
- Check MIME type
- Limit file size
- Scan content
- Use unique filenames
- Store outside web root

Example:
```python
from src.file_validator import PDFValidator

validator = PDFValidator(max_size_mb=10, max_pages=500)
content, file_hash, pages = await validator.validate_pdf(file)
```

### 4. Error Messages

❌ **BAD:**
```python
# Expose stack traces
raise HTTPException(500, str(e))
```

✅ **GOOD:**
```python
logger.exception("Error details here")
raise HTTPException(500, {
    "error": "Operation failed",
    "request_id": request_id
})
```

---

## 🚀 Deployment

### Docker

Create `Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "api_final_v2.py"]
```

Build & Run:
```bash
docker build -f Dockerfile.prod -t kreyol-ia:v2 .
docker run -p 8000:8000 --env-file .env kreyol-ia:v2
```

### Kubernetes

Create `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kreyol-ia
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kreyol-ia
  template:
    metadata:
      labels:
        app: kreyol-ia
    spec:
      containers:
      - name: api
        image: kreyol-ia:v2
        ports:
        - containerPort: 8000
        env:
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: kreyol-ia-secrets
              key: jwt-secret
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Render.com

Update `render.yaml`:

```yaml
services:
  - type: web
    name: kreyol-ia-v2
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python api_final_v2.py
    envVars:
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: APP_ENV
        value: production
      - key: ALLOWED_ORIGINS
        value: https://kreyol-ia.onrender.com
```

---

## 📈 Performance Tips

### 1. Enable Redis Caching

```env
REDIS_CACHE_ENABLED=true
REDIS_URL=redis://localhost:6379/0
```

### 2. Use Gunicorn with Multiple Workers

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  api_final_v2:app
```

### 3. PostgreSQL for Production

```env
DATABASE_URL=postgresql://user:pass@localhost/kreyol_ia
```

### 4. CDN for Static Files

Use CloudFront, Cloudflare, ou lòt CDN pou output files.

---

## 🧪 Testing

### Test Health Checks

```bash
# Liveness
curl http://localhost:8000/health/live

# Readiness
curl http://localhost:8000/health/ready

# Full health
curl http://localhost:8000/health?detailed=true
```

### Test Metrics

```bash
curl http://localhost:8000/metrics
```

### Test File Upload Security

```bash
# Should be blocked
curl -X POST http://localhost:8000/api/audiobook \
  -F "file=@malware.exe"

# Should work
curl -X POST http://localhost:8000/api/audiobook \
  -F "file=@document.pdf"
```

### Load Testing

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:8000/health

# Using wrk
wrk -t4 -c100 -d30s http://localhost:8000/health
```

---

## 🔍 Troubleshooting

### Configuration Errors

```bash
# Check configuration
python src/app_config.py

# Validate production config
python -c "from src.app_config import validate_production_config; validate_production_config()"
```

### Health Check Failures

```bash
# Check detailed health
curl http://localhost:8000/health?detailed=true | jq .

# Check specific component
# Database, translator, storage, etc.
```

### Metrics Not Working

```bash
# Check if Prometheus enabled
curl http://localhost:8000/metrics

# Should return metrics or 404 if disabled
```

---

## 📚 Additional Resources

### Documentation
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **NLLB Guide**: `NLLB_GUIDE.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`

### Monitoring Tools
- **Prometheus**: https://prometheus.io/
- **Grafana**: https://grafana.com/
- **Sentry**: https://sentry.io/

### Security Tools
- **OWASP ZAP**: Security testing
- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability scanner

---

## ✅ Production Checklist

Anvan deployment nan production:

- [ ] Generate ak set JWT_SECRET_KEY
- [ ] Configure CORS origins properly
- [ ] Set APP_ENV=production
- [ ] Disable DEBUG mode
- [ ] Configure proper DATABASE_URL
- [ ] Set up Redis (optional)
- [ ] Configure Sentry (optional)
- [ ] Test health checks
- [ ] Test metrics endpoint
- [ ] Load test application
- [ ] Security scan
- [ ] Backup strategy
- [ ] Monitoring alerts
- [ ] Log aggregation
- [ ] SSL/TLS certificates

---

## 🎊 Summary

Kreyòl IA V2 kounye a production-ready ak:

✅ **Sekirite**
- Environment-based configuration
- Secure file upload validation
- Proper CORS setup
- No hard-coded secrets

✅ **Monitoring**
- Prometheus metrics
- Health checks (live/ready/startup)
- Request tracking
- Performance metrics

✅ **Robustness**
- Professional error handling
- Request ID tracking
- Comprehensive logging
- Component health monitoring

✅ **Production Features**
- Docker support
- Kubernetes-ready
- Scalable architecture
- Best practices

**Bon deployment!** 🚀🇭🇹

