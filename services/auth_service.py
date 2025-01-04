import hashlib
import uuid
from typing import Optional
import sqlite3
from database.db_manager import DatabaseManager

class AuthService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username: str, password: str) -> str:
        user_id = str(uuid.uuid4())
        password_hash = self.hash_password(password)
        
        with sqlite3.connect(self.db_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (id, username, password_hash) VALUES (?, ?, ?)",
                (user_id, username, password_hash)
            )
        return user_id

    def authenticate(self, username: str, password: str) -> Optional[str]:
        password_hash = self.hash_password(password)
        
        with sqlite3.connect(self.db_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            result = cursor.fetchone()
            return result[0] if result else None