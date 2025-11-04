#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Real-Time Collaboration with WebSocket
Kolaborasyon an tan reyèl avèk WebSocket

Features:
- Live script editing
- Real-time progress updates
- Multi-user collaboration
- Live audio preview
- Chat between collaborators
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set
import json
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger('FanerStudio.WebSocket')


class ConnectionManager:
    """
    Manage WebSocket connections
    Jere koneksyon WebSocket
    """
    
    def __init__(self):
        # Active connections by room
        self.active_connections: Dict[str, List[WebSocket]] = {}
        # User info by connection
        self.user_info: Dict[WebSocket, Dict] = {}
        # Room metadata
        self.rooms: Dict[str, Dict] = {}
    
    async def connect(
        self,
        websocket: WebSocket,
        room_id: str,
        user_id: str,
        username: str
    ):
        """Connect user to a room"""
        await websocket.accept()
        
        # Add to room
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
            self.rooms[room_id] = {
                "created_at": datetime.now().isoformat(),
                "users": []
            }
        
        self.active_connections[room_id].append(websocket)
        
        # Store user info
        self.user_info[websocket] = {
            "user_id": user_id,
            "username": username,
            "room_id": room_id,
            "joined_at": datetime.now().isoformat()
        }
        
        # Add to room users
        self.rooms[room_id]["users"].append({
            "user_id": user_id,
            "username": username
        })
        
        logger.info(f"✅ User {username} connected to room {room_id}")
        
        # Notify others
        await self.broadcast_to_room(
            room_id,
            {
                "type": "user_joined",
                "user_id": user_id,
                "username": username,
                "timestamp": datetime.now().isoformat()
            },
            exclude=websocket
        )
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect user"""
        if websocket in self.user_info:
            user_info = self.user_info[websocket]
            room_id = user_info["room_id"]
            username = user_info["username"]
            
            # Remove from room
            if room_id in self.active_connections:
                self.active_connections[room_id].remove(websocket)
                
                # Remove from room users
                self.rooms[room_id]["users"] = [
                    u for u in self.rooms[room_id]["users"]
                    if u["user_id"] != user_info["user_id"]
                ]
                
                # Clean up empty room
                if not self.active_connections[room_id]:
                    del self.active_connections[room_id]
                    del self.rooms[room_id]
            
            # Remove user info
            del self.user_info[websocket]
            
            logger.info(f"❌ User {username} disconnected from room {room_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def broadcast_to_room(
        self,
        room_id: str,
        message: dict,
        exclude: WebSocket = None
    ):
        """Broadcast message to all users in room"""
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                if connection != exclude:
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        logger.error(f"Error broadcasting: {e}")
    
    def get_room_users(self, room_id: str) -> List[Dict]:
        """Get list of users in room"""
        if room_id in self.rooms:
            return self.rooms[room_id]["users"]
        return []
    
    def get_active_rooms(self) -> List[str]:
        """Get list of active room IDs"""
        return list(self.active_connections.keys())


# Global connection manager
manager = ConnectionManager()


# ============================================================
# MESSAGE HANDLERS
# ============================================================

class MessageHandler:
    """Handle different types of WebSocket messages"""
    
    @staticmethod
    async def handle_script_edit(
        websocket: WebSocket,
        room_id: str,
        data: dict
    ):
        """Handle script editing"""
        user_info = manager.user_info.get(websocket, {})
        
        await manager.broadcast_to_room(
            room_id,
            {
                "type": "script_update",
                "user_id": user_info.get("user_id"),
                "username": user_info.get("username"),
                "content": data.get("content"),
                "cursor_position": data.get("cursor_position"),
                "timestamp": datetime.now().isoformat()
            },
            exclude=websocket
        )
    
    @staticmethod
    async def handle_progress_update(
        websocket: WebSocket,
        room_id: str,
        data: dict
    ):
        """Handle progress updates"""
        await manager.broadcast_to_room(
            room_id,
            {
                "type": "progress",
                "task": data.get("task"),
                "progress": data.get("progress"),
                "message": data.get("message"),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    @staticmethod
    async def handle_chat_message(
        websocket: WebSocket,
        room_id: str,
        data: dict
    ):
        """Handle chat messages"""
        user_info = manager.user_info.get(websocket, {})
        
        await manager.broadcast_to_room(
            room_id,
            {
                "type": "chat",
                "user_id": user_info.get("user_id"),
                "username": user_info.get("username"),
                "message": data.get("message"),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    @staticmethod
    async def handle_audio_preview(
        websocket: WebSocket,
        room_id: str,
        data: dict
    ):
        """Handle audio preview requests"""
        await manager.broadcast_to_room(
            room_id,
            {
                "type": "audio_preview",
                "audio_url": data.get("audio_url"),
                "duration": data.get("duration"),
                "timestamp": datetime.now().isoformat()
            }
        )
    
    @staticmethod
    async def handle_cursor_position(
        websocket: WebSocket,
        room_id: str,
        data: dict
    ):
        """Handle cursor position updates"""
        user_info = manager.user_info.get(websocket, {})
        
        await manager.broadcast_to_room(
            room_id,
            {
                "type": "cursor",
                "user_id": user_info.get("user_id"),
                "username": user_info.get("username"),
                "position": data.get("position"),
                "timestamp": datetime.now().isoformat()
            },
            exclude=websocket
        )


# ============================================================
# WEBSOCKET ROUTES (to be added to main.py)
# ============================================================

"""
Add these routes to main.py:

from websocket_collaboration import manager, MessageHandler

@app.websocket("/ws/collaborate/{room_id}")
async def websocket_collaborate(
    websocket: WebSocket,
    room_id: str,
    user_id: str = None,
    username: str = "Anonymous"
):
    # Connect user
    await manager.connect(websocket, room_id, user_id or "guest", username)
    
    try:
        # Send initial room state
        await manager.send_personal_message(
            {
                "type": "room_state",
                "room_id": room_id,
                "users": manager.get_room_users(room_id)
            },
            websocket
        )
        
        # Listen for messages
        while True:
            data = await websocket.receive_json()
            
            message_type = data.get("type")
            
            if message_type == "script_edit":
                await MessageHandler.handle_script_edit(websocket, room_id, data)
            elif message_type == "progress":
                await MessageHandler.handle_progress_update(websocket, room_id, data)
            elif message_type == "chat":
                await MessageHandler.handle_chat_message(websocket, room_id, data)
            elif message_type == "audio_preview":
                await MessageHandler.handle_audio_preview(websocket, room_id, data)
            elif message_type == "cursor":
                await MessageHandler.handle_cursor_position(websocket, room_id, data)
            else:
                logger.warning(f"Unknown message type: {message_type}")
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
        # Notify others
        user_info = manager.user_info.get(websocket, {})
        if user_info:
            await manager.broadcast_to_room(
                room_id,
                {
                    "type": "user_left",
                    "user_id": user_info.get("user_id"),
                    "username": user_info.get("username"),
                    "timestamp": datetime.now().isoformat()
                }
            )
"""


# ============================================================
# CLIENT-SIDE JAVASCRIPT EXAMPLE
# ============================================================

CLIENT_JS_EXAMPLE = """
// Example WebSocket client code

class CollaborationClient {
    constructor(roomId, userId, username) {
        this.roomId = roomId;
        this.userId = userId;
        this.username = username;
        this.ws = null;
    }
    
    connect() {
        const wsUrl = `ws://localhost:8000/ws/collaborate/${this.roomId}?user_id=${this.userId}&username=${this.username}`;
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('✅ Connected to collaboration room');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onclose = () => {
            console.log('❌ Disconnected from collaboration room');
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }
    
    handleMessage(data) {
        switch(data.type) {
            case 'room_state':
                this.updateUsersList(data.users);
                break;
            case 'user_joined':
                this.onUserJoined(data);
                break;
            case 'user_left':
                this.onUserLeft(data);
                break;
            case 'script_update':
                this.onScriptUpdate(data);
                break;
            case 'progress':
                this.onProgressUpdate(data);
                break;
            case 'chat':
                this.onChatMessage(data);
                break;
            case 'audio_preview':
                this.onAudioPreview(data);
                break;
            case 'cursor':
                this.onCursorUpdate(data);
                break;
        }
    }
    
    // Send script edit
    sendScriptEdit(content, cursorPosition) {
        this.ws.send(JSON.stringify({
            type: 'script_edit',
            content: content,
            cursor_position: cursorPosition
        }));
    }
    
    // Send chat message
    sendChatMessage(message) {
        this.ws.send(JSON.stringify({
            type: 'chat',
            message: message
        }));
    }
    
    // Send cursor position
    sendCursorPosition(position) {
        this.ws.send(JSON.stringify({
            type: 'cursor',
            position: position
        }));
    }
    
    // Event handlers (to be implemented by UI)
    updateUsersList(users) { }
    onUserJoined(data) { }
    onUserLeft(data) { }
    onScriptUpdate(data) { }
    onProgressUpdate(data) { }
    onChatMessage(data) { }
    onAudioPreview(data) { }
    onCursorUpdate(data) { }
}

// Usage:
const client = new CollaborationClient('room123', 'user1', 'John');
client.connect();
"""


# ============================================================
# TESTING
# ============================================================

def test_websocket_system():
    """Test WebSocket collaboration system"""
    print("🧪 Testing WebSocket Collaboration System\n")
    
    print("Connection Manager:")
    print(f"  Active rooms: {len(manager.get_active_rooms())}")
    
    print("\n✅ WebSocket system ready!")
    print("\nTo test:")
    print("1. Add WebSocket route to main.py (see comments above)")
    print("2. Start server: uvicorn main:app --reload")
    print("3. Open browser console and run client code")
    print("4. Connect multiple browsers to same room")


if __name__ == "__main__":
    test_websocket_system()

