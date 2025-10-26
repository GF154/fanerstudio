#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Module
SQLite database for task management
"""

import sqlite3
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


logger = logging.getLogger('KreyolAI.Database')


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """Task model"""
    task_id: str
    task_type: str
    status: str
    created_at: str
    updated_at: str
    input_data: Optional[Dict[str, Any]] = None
    result_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class DatabaseManager:
    """
    Database manager for task tracking
    """
    
    def __init__(self, db_path: str = "kreyol_ai.db"):
        """
        Initialize database manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.connection = None
        self._initialize_database()
        logger.info(f"Database initialized: {self.db_path}")
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id TEXT PRIMARY KEY,
                task_type TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                input_data TEXT,
                result_data TEXT,
                error_message TEXT
            )
        """)
        
        # Create indices
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_status 
            ON tasks(status)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_created_at 
            ON tasks(created_at DESC)
        """)
        
        # Usage statistics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                UNIQUE(date, endpoint)
            )
        """)
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT,
                hashed_password TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT,
                disabled INTEGER DEFAULT 0
            )
        """)
        
        # API keys table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                name TEXT NOT NULL,
                hashed_key TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_api_keys_username
            ON api_keys(username)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_api_keys_hashed_key
            ON api_keys(hashed_key)
        """)
        
        conn.commit()
        logger.info("Database tables initialized")
    
    def create_task(
        self,
        task_id: str,
        task_type: str,
        input_data: Optional[Dict[str, Any]] = None
    ) -> Task:
        """
        Create a new task
        
        Args:
            task_id: Unique task identifier
            task_type: Type of task
            input_data: Input data dictionary
        
        Returns:
            Created task object
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute("""
            INSERT INTO tasks (
                task_id, task_type, status, created_at, updated_at, input_data
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            task_id,
            task_type,
            TaskStatus.PENDING,
            now,
            now,
            json.dumps(input_data) if input_data else None
        ))
        
        conn.commit()
        
        logger.info(f"Task created: {task_id} ({task_type})")
        
        return Task(
            task_id=task_id,
            task_type=task_type,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
            input_data=input_data
        )
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get task by ID
        
        Args:
            task_id: Task identifier
        
        Returns:
            Task object or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM tasks WHERE task_id = ?
        """, (task_id,))
        
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return Task(
            task_id=row['task_id'],
            task_type=row['task_type'],
            status=row['status'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            input_data=json.loads(row['input_data']) if row['input_data'] else None,
            result_data=json.loads(row['result_data']) if row['result_data'] else None,
            error_message=row['error_message']
        )
    
    def update_task(
        self,
        task_id: str,
        status: Optional[str] = None,
        result_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Update task status and results
        
        Args:
            task_id: Task identifier
            status: New status
            result_data: Result data dictionary
            error_message: Error message if failed
        
        Returns:
            True if updated successfully
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        updates = ["updated_at = ?"]
        params = [datetime.now().isoformat()]
        
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        
        if result_data is not None:
            updates.append("result_data = ?")
            params.append(json.dumps(result_data))
        
        if error_message is not None:
            updates.append("error_message = ?")
            params.append(error_message)
        
        params.append(task_id)
        
        cursor.execute(f"""
            UPDATE tasks
            SET {', '.join(updates)}
            WHERE task_id = ?
        """, params)
        
        conn.commit()
        
        logger.info(f"Task updated: {task_id} (status={status})")
        
        return cursor.rowcount > 0
    
    def list_tasks(
        self,
        limit: int = 50,
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[Task]:
        """
        List tasks with pagination
        
        Args:
            limit: Maximum number of tasks
            offset: Number of tasks to skip
            status: Filter by status (optional)
        
        Returns:
            List of tasks
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM tasks"
        params = []
        
        if status:
            query += " WHERE status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        
        return [
            Task(
                task_id=row['task_id'],
                task_type=row['task_type'],
                status=row['status'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
                input_data=json.loads(row['input_data']) if row['input_data'] else None,
                result_data=json.loads(row['result_data']) if row['result_data'] else None,
                error_message=row['error_message']
            )
            for row in rows
        ]
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task
        
        Args:
            task_id: Task identifier
        
        Returns:
            True if deleted successfully
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM tasks WHERE task_id = ?
        """, (task_id,))
        
        conn.commit()
        
        logger.info(f"Task deleted: {task_id}")
        
        return cursor.rowcount > 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get usage statistics
        
        Returns:
            Dictionary with statistics
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Total tasks
        cursor.execute("SELECT COUNT(*) as total FROM tasks")
        total_tasks = cursor.fetchone()['total']
        
        # Tasks by status
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM tasks
            GROUP BY status
        """)
        status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
        
        # Tasks by type
        cursor.execute("""
            SELECT task_type, COUNT(*) as count
            FROM tasks
            GROUP BY task_type
        """)
        type_counts = {row['task_type']: row['count'] for row in cursor.fetchall()}
        
        # Recent tasks
        cursor.execute("""
            SELECT DATE(created_at) as date, COUNT(*) as count
            FROM tasks
            WHERE created_at >= date('now', '-7 days')
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        """)
        recent_activity = [
            {"date": row['date'], "count": row['count']}
            for row in cursor.fetchall()
        ]
        
        return {
            "total_tasks": total_tasks,
            "by_status": status_counts,
            "by_type": type_counts,
            "recent_activity": recent_activity
        }
    
    def cleanup_old_tasks(self, days: int = 30) -> int:
        """
        Delete tasks older than specified days
        
        Args:
            days: Number of days to keep
        
        Returns:
            Number of tasks deleted
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM tasks
            WHERE created_at < datetime('now', '-' || ? || ' days')
        """, (days,))
        
        conn.commit()
        
        deleted_count = cursor.rowcount
        logger.info(f"Cleaned up {deleted_count} old tasks")
        
        return deleted_count
    
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """
        Create a new user
        
        Args:
            user_data: User data dictionary
        
        Returns:
            True if created successfully
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (
                username, email, full_name, hashed_password,
                created_at, disabled
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_data["username"],
            user_data["email"],
            user_data.get("full_name"),
            user_data["hashed_password"],
            user_data["created_at"],
            1 if user_data.get("disabled", False) else 0
        ))
        
        conn.commit()
        logger.info(f"User created in database: {user_data['username']}")
        
        return cursor.rowcount > 0
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get user by username
        
        Args:
            username: Username
        
        Returns:
            User data dictionary or None
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM users WHERE username = ?
        """, (username,))
        
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return {
            "username": row["username"],
            "email": row["email"],
            "full_name": row["full_name"],
            "hashed_password": row["hashed_password"],
            "created_at": row["created_at"],
            "last_login": row["last_login"],
            "disabled": bool(row["disabled"])
        }
    
    def update_user(self, username: str, updates: Dict[str, Any]) -> bool:
        """
        Update user data
        
        Args:
            username: Username
            updates: Dictionary of fields to update
        
        Returns:
            True if updated successfully
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        set_clauses = []
        params = []
        
        for key, value in updates.items():
            if key in ["email", "full_name", "hashed_password", "last_login", "disabled"]:
                set_clauses.append(f"{key} = ?")
                if key == "disabled":
                    params.append(1 if value else 0)
                else:
                    params.append(value)
        
        if not set_clauses:
            return False
        
        params.append(username)
        
        cursor.execute(f"""
            UPDATE users
            SET {', '.join(set_clauses)}
            WHERE username = ?
        """, params)
        
        conn.commit()
        
        logger.info(f"User updated: {username}")
        
        return cursor.rowcount > 0
    
    def create_api_key(self, key_data: Dict[str, Any]) -> bool:
        """
        Create API key
        
        Args:
            key_data: API key data dictionary
        
        Returns:
            True if created successfully
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO api_keys (
                username, name, hashed_key, created_at, expires_at, is_active
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            key_data["username"],
            key_data["name"],
            key_data["hashed_key"],
            key_data["created_at"],
            key_data["expires_at"],
            1 if key_data.get("is_active", True) else 0
        ))
        
        conn.commit()
        logger.info(f"API key created for user: {key_data['username']}")
        
        return cursor.rowcount > 0
    
    def get_api_key_by_hash(self, hashed_key: str) -> Optional[Dict[str, Any]]:
        """
        Get API key by hash
        
        Args:
            hashed_key: Hashed API key
        
        Returns:
            API key data or None
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM api_keys WHERE hashed_key = ?
        """, (hashed_key,))
        
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return {
            "id": row["id"],
            "username": row["username"],
            "name": row["name"],
            "hashed_key": row["hashed_key"],
            "created_at": row["created_at"],
            "expires_at": row["expires_at"],
            "is_active": bool(row["is_active"])
        }
    
    def list_user_api_keys(self, username: str) -> List[Dict[str, Any]]:
        """
        List all API keys for a user
        
        Args:
            username: Username
        
        Returns:
            List of API key data
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, name, created_at, expires_at, is_active
            FROM api_keys
            WHERE username = ?
            ORDER BY created_at DESC
        """, (username,))
        
        rows = cursor.fetchall()
        
        return [
            {
                "id": row["id"],
                "username": row["username"],
                "name": row["name"],
                "created_at": row["created_at"],
                "expires_at": row["expires_at"],
                "is_active": bool(row["is_active"])
            }
            for row in rows
        ]
    
    def revoke_api_key(self, key_id: int) -> bool:
        """
        Revoke an API key
        
        Args:
            key_id: API key ID
        
        Returns:
            True if revoked successfully
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE api_keys
            SET is_active = 0
            WHERE id = ?
        """, (key_id,))
        
        conn.commit()
        
        logger.info(f"API key revoked: {key_id}")
        
        return cursor.rowcount > 0
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Database connection closed")

