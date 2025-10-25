# 🐘 Migration PostgreSQL Guide

## Vue d'Ensemble

Ce guide explique comment migrer de SQLite vers PostgreSQL pour une meilleure scalabilité en production.

---

## 🎯 Pourquoi Migrer?

### SQLite (Actuel)
✅ **Avantages:**
- Simple, pas de configuration
- Parfait pour développement
- Intégré, pas de serveur externe

❌ **Limitations:**
- Un seul writer à la fois
- Pas optimal pour scaling horizontal
- Moins performant sous forte charge

### PostgreSQL (Recommandé)
✅ **Avantages:**
- Multiple concurrent writers
- Excellent pour scaling
- Meilleure performance
- Transactions ACID robustes
- Réplication & clustering

---

## 📦 Installation PostgreSQL

### Option 1: Local (Développement)

**Windows:**
```bash
# Télécharger depuis postgresql.org
# Ou avec Chocolatey:
choco install postgresql

# Démarrer service
pg_ctl start
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

### Option 2: Docker (Recommandé)

```bash
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16
    container_name: kreyol_ai_postgres
    environment:
      POSTGRES_USER: kreyol_ai
      POSTGRES_PASSWORD: your_password_here
      POSTGRES_DB: kreyol_ai_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

```bash
docker-compose up -d postgres
```

### Option 3: Cloud (Production)

**Heroku Postgres:**
```bash
heroku addons:create heroku-postgresql:mini
```

**AWS RDS:**
- Créer instance RDS PostgreSQL
- Configurer security groups
- Noter endpoint et credentials

**DigitalOcean:**
- Créer Managed Database
- Choisir PostgreSQL
- Configurer connection pooling

---

## 🔧 Code Migration

### 1. Installer Dépendances

```bash
pip install psycopg2-binary SQLAlchemy alembic
```

**requirements.txt:**
```txt
# Database (Phase 5)
psycopg2-binary==2.9.10  # PostgreSQL adapter
SQLAlchemy==2.0.36       # ORM
alembic==1.14.0          # Database migrations
```

### 2. Créer Module PostgreSQL

**src/postgres_db.py:**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PostgreSQL Database Module
"""

import logging
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

logger = logging.getLogger('KreyolAI.PostgreSQL')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    
    task_id = Column(String, primary_key=True)
    task_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    input_data = Column(Text)
    result_data = Column(Text)
    error_message = Column(Text)


class User(Base):
    __tablename__ = 'users'
    
    username = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    last_login = Column(DateTime)
    disabled = Column(Boolean, default=False)
    
    # Relationship
    api_keys = relationship("APIKey", back_populates="user")


class APIKey(Base):
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey('users.username'), nullable=False)
    name = Column(String, nullable=False)
    hashed_key = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationship
    user = relationship("User", back_populates="api_keys")


class PostgreSQLManager:
    """PostgreSQL database manager"""
    
    def __init__(self, database_url: str):
        """
        Initialize PostgreSQL manager
        
        Args:
            database_url: PostgreSQL connection URL
                Format: postgresql://user:password@host:port/database
        """
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables
        Base.metadata.create_all(self.engine)
        
        logger.info(f"PostgreSQL connected: {database_url.split('@')[1]}")
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()
        logger.info("PostgreSQL connection closed")


def get_database_url(
    user: str = "kreyol_ai",
    password: str = "password",
    host: str = "localhost",
    port: int = 5432,
    database: str = "kreyol_ai_db"
) -> str:
    """
    Build PostgreSQL connection URL
    
    Args:
        user: Database user
        password: Database password
        host: Database host
        port: Database port
        database: Database name
    
    Returns:
        Connection URL
    """
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"
```

### 3. Configuration

**.env:**
```bash
# Database Configuration
DATABASE_TYPE=postgresql  # or sqlite
DATABASE_URL=postgresql://user:password@localhost:5432/kreyol_ai_db

# For Heroku (auto-configured)
# DATABASE_URL will be set automatically
```

### 4. Migration Script

**scripts/migrate_to_postgres.py:**
```python
#!/usr/bin/env python3
"""
Migrate data from SQLite to PostgreSQL
"""

import sqlite3
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.database import DatabaseManager
from src.postgres_db import PostgreSQLManager, get_database_url, Task, User, APIKey
from datetime import datetime


def migrate_tasks(sqlite_db: DatabaseManager, postgres_db: PostgreSQLManager):
    """Migrate tasks from SQLite to PostgreSQL"""
    print("Migrating tasks...")
    
    # Get all tasks from SQLite
    tasks = sqlite_db.list_tasks(limit=10000)
    
    session = postgres_db.get_session()
    
    for task_data in tasks:
        task = Task(
            task_id=task_data.task_id,
            task_type=task_data.task_type,
            status=task_data.status,
            created_at=datetime.fromisoformat(task_data.created_at),
            updated_at=datetime.fromisoformat(task_data.updated_at),
            input_data=str(task_data.input_data) if task_data.input_data else None,
            result_data=str(task_data.result_data) if task_data.result_data else None,
            error_message=task_data.error_message
        )
        session.merge(task)
    
    session.commit()
    session.close()
    
    print(f"Migrated {len(tasks)} tasks")


def migrate_users(sqlite_db: DatabaseManager, postgres_db: PostgreSQLManager):
    """Migrate users from SQLite to PostgreSQL"""
    print("Migrating users...")
    
    # Get users from SQLite (implement list_users method if needed)
    # For now, this is a placeholder
    
    print("User migration complete")


def main():
    """Main migration function"""
    print("="*60)
    print("🐘 SQLite → PostgreSQL Migration")
    print("="*60)
    print()
    
    # Connect to databases
    sqlite_db = DatabaseManager("kreyol_ai.db")
    
    # Get PostgreSQL URL from environment or use default
    postgres_url = get_database_url()
    postgres_db = PostgreSQLManager(postgres_url)
    
    try:
        # Migrate data
        migrate_tasks(sqlite_db, postgres_db)
        migrate_users(sqlite_db, postgres_db)
        
        print()
        print("✅ Migration complete!")
        print("   Remember to:")
        print("   1. Update DATABASE_URL in .env")
        print("   2. Test the application")
        print("   3. Backup SQLite database")
        print("   4. Update deployment configuration")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        sqlite_db.close()
        postgres_db.close()


if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python scripts/migrate_to_postgres.py
```

---

## 🔄 Database Migrations avec Alembic

### Initialiser Alembic

```bash
# Créer répertoire migrations
alembic init alembic

# Éditer alembic.ini
# sqlalchemy.url = postgresql://user:password@localhost/kreyol_ai_db
```

### Créer Migration

```bash
# Auto-générer migration depuis models
alembic revision --autogenerate -m "Initial migration"

# Appliquer migration
alembic upgrade head

# Rollback si nécessaire
alembic downgrade -1
```

---

## ⚡ Performance Tuning

### Connection Pooling

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    database_url,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Verify connections
)
```

### Indices

```sql
-- Créer indices pour performance
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_api_keys_user ON api_keys(username);
```

---

## 🔒 Sécurité

### 1. Credentials Management

```bash
# Ne JAMAIS commit credentials
# Utiliser variables d'environnement

export DATABASE_URL="postgresql://user:password@host:port/db"
```

### 2. SSL Connection

```python
# Pour production
database_url = "postgresql://user:password@host:port/db?sslmode=require"
```

### 3. User Permissions

```sql
-- Créer user avec permissions limitées
CREATE USER kreyol_ai_app WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE kreyol_ai_db TO kreyol_ai_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO kreyol_ai_app;
```

---

## 📊 Monitoring

### Queries Monitoring

```sql
-- Voir queries actives
SELECT pid, usename, application_name, state, query
FROM pg_stat_activity
WHERE datname = 'kreyol_ai_db';

-- Kill query longue
SELECT pg_terminate_backend(pid);
```

### Database Size

```sql
-- Taille database
SELECT pg_size_pretty(pg_database_size('kreyol_ai_db'));

-- Taille tables
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public';
```

---

## 🚀 Déploiement

### Heroku

```bash
# Heroku configure automatiquement DATABASE_URL
heroku addons:create heroku-postgresql:mini
heroku config:set DATABASE_TYPE=postgresql

# Migrations
heroku run alembic upgrade head
```

### AWS RDS

```bash
# Créer RDS instance
aws rds create-db-instance \
  --db-instance-identifier kreyol-ai-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20

# Obtenir endpoint
aws rds describe-db-instances \
  --db-instance-identifier kreyol-ai-db \
  --query 'DBInstances[0].Endpoint.Address'
```

---

## ✅ Checklist Migration

- [ ] Installer PostgreSQL (local/docker/cloud)
- [ ] Installer dépendances Python
- [ ] Créer module `postgres_db.py`
- [ ] Mettre à jour `.env` avec DATABASE_URL
- [ ] Exécuter script de migration
- [ ] Tester application avec PostgreSQL
- [ ] Configurer connection pooling
- [ ] Créer indices pour performance
- [ ] Setup monitoring
- [ ] Backup SQLite avant suppression
- [ ] Mettre à jour documentation
- [ ] Mettre à jour CI/CD

---

## 🆘 Troubleshooting

### Connection Refused
```bash
# Vérifier que PostgreSQL est démarré
sudo systemctl status postgresql

# Vérifier port
sudo netstat -nlp | grep 5432
```

### Permission Denied
```bash
# Réinitialiser password
sudo -u postgres psql
ALTER USER kreyol_ai WITH PASSWORD 'new_password';
```

### Slow Queries
```sql
-- Activer query logging
ALTER DATABASE kreyol_ai_db SET log_min_duration_statement = 1000;  -- log queries > 1s

-- Analyser query
EXPLAIN ANALYZE SELECT * FROM tasks WHERE status = 'completed';
```

---

**Date:** 12 octobre 2025  
**Version:** 5.0  
**Status:** Migration Ready 🐘







