import sqlite3
from typing import List, Optional
from models.task import Task
import json

class DatabaseManager:
    def __init__(self, db_path: str = "todo.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    priority TEXT NOT NULL,
                    due_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tags TEXT,
                    category TEXT,
                    completed BOOLEAN DEFAULT FALSE,
                    user_id TEXT NOT NULL,
                    recurrence TEXT,
                    parent_task_id TEXT,
                    points INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (parent_task_id) REFERENCES tasks(id)
                )
            """)
            
            conn.commit()

    def add_task(self, task: Task) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (
                    id, title, description, priority, due_date, tags,
                    category, completed, user_id, recurrence, parent_task_id, points
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.id, task.title, task.description, task.priority.value,
                task.due_date, json.dumps(task.tags), task.category,
                task.completed, task.user_id, task.recurrence.value,
                task.parent_task_id, task.points
            ))
            return True

    def get_tasks(self, user_id: str) -> List[Task]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def _row_to_task(self, row) -> Task:
        # Convert database row to Task object
        return Task(
            id=row[0],
            title=row[1],
            description=row[2],
            priority=Priority(row[3]),
            due_date=row[4],
            created_at=row[5],
            tags=json.loads(row[6]),
            category=row[7],
            completed=bool(row[8]),
            user_id=row[9],
            recurrence=RecurrenceType(row[10]),
            parent_task_id=row[11],
            points=row[12],
            subtasks=[]
        )