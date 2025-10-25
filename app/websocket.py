#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔌 WebSocket Support
Real-time progress updates pou long-running tasks
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, List
import json
import asyncio
from datetime import datetime


class ConnectionManager:
    """
    Manage WebSocket connections pou real-time updates
    
    Features:
    - Multiple clients can watch same task
    - Broadcast updates to all watchers
    - Automatic cleanup on disconnect
    - Message queuing for offline clients
    """
    
    def __init__(self):
        """Initialize connection manager"""
        # Task ID -> Set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        
        # Message history for reconnections
        self.message_history: Dict[str, List[dict]] = {}
        self.max_history = 50  # Keep last 50 messages per task
        
        print("✅ WebSocket ConnectionManager initialized")
    
    async def connect(self, websocket: WebSocket, task_id: str):
        """
        Connect a new WebSocket client for a task
        
        Args:
            websocket: WebSocket connection
            task_id: Task ID to watch
        """
        await websocket.accept()
        
        # Add to active connections
        if task_id not in self.active_connections:
            self.active_connections[task_id] = set()
        
        self.active_connections[task_id].add(websocket)
        
        print(f"🔌 WebSocket connected for task: {task_id}")
        print(f"   Active connections for this task: {len(self.active_connections[task_id])}")
        
        # Send message history if available
        if task_id in self.message_history:
            for msg in self.message_history[task_id]:
                try:
                    await websocket.send_json(msg)
                except:
                    pass
    
    def disconnect(self, websocket: WebSocket, task_id: str):
        """
        Disconnect a WebSocket client
        
        Args:
            websocket: WebSocket connection
            task_id: Task ID being watched
        """
        if task_id in self.active_connections:
            self.active_connections[task_id].discard(websocket)
            
            # Cleanup empty task groups
            if not self.active_connections[task_id]:
                del self.active_connections[task_id]
                print(f"🔌 No more connections for task: {task_id}")
    
    async def send_progress(
        self,
        task_id: str,
        data: dict,
        save_to_history: bool = True
    ):
        """
        Send progress update to all clients watching a task
        
        Args:
            task_id: Task ID
            data: Progress data to send
            save_to_history: Whether to save message for reconnections
        """
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        # Save to history
        if save_to_history:
            if task_id not in self.message_history:
                self.message_history[task_id] = []
            
            self.message_history[task_id].append(data)
            
            # Keep only last N messages
            if len(self.message_history[task_id]) > self.max_history:
                self.message_history[task_id] = self.message_history[task_id][-self.max_history:]
        
        # Send to all connected clients
        if task_id in self.active_connections:
            disconnected = []
            
            for connection in self.active_connections[task_id]:
                try:
                    await connection.send_json(data)
                except Exception as e:
                    print(f"⚠️  Failed to send to connection: {e}")
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for conn in disconnected:
                self.disconnect(conn, task_id)
    
    async def broadcast(self, data: dict):
        """
        Broadcast message to ALL connected clients
        
        Args:
            data: Data to broadcast
        """
        for task_id, connections in self.active_connections.items():
            await self.send_progress(task_id, data, save_to_history=False)
    
    def get_connection_count(self, task_id: str = None) -> int:
        """
        Get number of active connections
        
        Args:
            task_id: Specific task ID, or None for total
        
        Returns:
            Number of active connections
        """
        if task_id:
            return len(self.active_connections.get(task_id, set()))
        else:
            return sum(len(conns) for conns in self.active_connections.values())
    
    def cleanup_task(self, task_id: str):
        """
        Cleanup all data for a completed task
        
        Args:
            task_id: Task ID to cleanup
        """
        # Remove from active connections
        if task_id in self.active_connections:
            del self.active_connections[task_id]
        
        # Remove message history
        if task_id in self.message_history:
            del self.message_history[task_id]
        
        print(f"🧹 Cleaned up WebSocket data for task: {task_id}")
    
    def get_stats(self) -> dict:
        """
        Get statistics about WebSocket connections
        
        Returns:
            Dictionary with stats
        """
        return {
            "total_connections": self.get_connection_count(),
            "active_tasks": len(self.active_connections),
            "tasks_in_history": len(self.message_history),
            "tasks": {
                task_id: {
                    "connections": len(conns),
                    "messages_in_history": len(self.message_history.get(task_id, []))
                }
                for task_id, conns in self.active_connections.items()
            }
        }


# Global connection manager instance
manager = ConnectionManager()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

async def notify_task_progress(
    task_id: str,
    progress: int,
    status: str,
    stage: str = None,
    **extra_data
):
    """
    Helper function to send task progress via WebSocket
    
    Args:
        task_id: Task ID
        progress: Progress percentage (0-100)
        status: Status message
        stage: Current stage name
        **extra_data: Additional data to include
    """
    data = {
        "progress": progress,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    
    if stage:
        data["stage"] = stage
    
    # Add extra data
    data.update(extra_data)
    
    await manager.send_progress(task_id, data)


async def notify_task_complete(
    task_id: str,
    result: dict
):
    """
    Notify that a task is complete
    
    Args:
        task_id: Task ID
        result: Task result
    """
    await manager.send_progress(task_id, {
        "progress": 100,
        "status": "Konple!",
        "stage": "completed",
        "result": result
    })
    
    # Cleanup after a delay
    await asyncio.sleep(5)
    manager.cleanup_task(task_id)


async def notify_task_error(
    task_id: str,
    error: str
):
    """
    Notify that a task failed
    
    Args:
        task_id: Task ID
        error: Error message
    """
    await manager.send_progress(task_id, {
        "progress": 0,
        "status": "Erè",
        "stage": "failed",
        "error": error
    })


if __name__ == "__main__":
    print("🔌 WebSocket ConnectionManager")
    print("=" * 60)
    print("Features:")
    print("  • Real-time progress updates")
    print("  • Multiple clients per task")
    print("  • Message history for reconnections")
    print("  • Automatic cleanup")
    print("=" * 60)

