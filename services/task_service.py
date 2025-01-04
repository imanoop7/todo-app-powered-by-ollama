from typing import List, Optional
from datetime import datetime
import uuid
from models.task import Task, Priority, RecurrenceType
from database.db_manager import DatabaseManager
from services.ollama_service import LlamaService
import sqlite3

class TaskService:
    def __init__(self, db_manager: DatabaseManager, llama_service: LlamaService):
        self.db_manager = db_manager
        self.llama_service = llama_service

    def create_task(self, user_id: str, title: str, description: Optional[str] = None,
                   priority: Priority = Priority.MEDIUM, due_date: Optional[datetime] = None,
                   tags: List[str] = None, category: Optional[str] = None,
                   recurrence: RecurrenceType = RecurrenceType.NONE,
                   parent_task_id: Optional[str] = None) -> Task:
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            created_at=datetime.now(),
            tags=tags or [],
            category=category,
            completed=False,
            user_id=user_id,
            recurrence=recurrence,
            parent_task_id=parent_task_id,
            subtasks=[],
            points=self._calculate_points(priority)
        )
        self.db_manager.add_task(task)
        return task

    def create_task_from_natural_language(self, user_id: str, text: str) -> Task:
        # Use Llama service to parse natural language input
        task_info = self.llama_service.parse_task(text)
        return self.create_task(user_id=user_id, **task_info)

    def _calculate_points(self, priority: str) -> int:
        points_map = {
            'high': 10,
            'medium': 5,  
            'low': 2
        }
        return points_map.get(priority.lower(), 2)

    def get_user_tasks(self, user_id: str) -> List[Task]:
        return self.db_manager.get_tasks(user_id)

    def mark_completed(self, task_id: str, user_id: str) -> bool:
        with sqlite3.connect(self.db_manager.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks 
                SET completed = TRUE 
                WHERE id = ? AND user_id = ?
            """, (task_id, user_id))
            return cursor.rowcount > 0

def update_task(self, task_id: str, user_id: str, **updates) -> Optional[Task]:
    allowed_fields = {'title', 'description', 'priority', 'due_date', 
                     'tags', 'category', 'recurrence', 'points'}
    
    # Filter out invalid fields
    valid_updates = {k: v for k, v in updates.items() if k in allowed_fields}
    
    if not valid_updates:
        return None
    
    # Build the update query
    set_clause = ', '.join(f"{k} = ?" for k in valid_updates.keys())
    values = list(valid_updates.values())
    values.extend([task_id, user_id])  # Add WHERE clause parameters
    
    with sqlite3.connect(self.db_manager.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE tasks 
            SET {set_clause}
            WHERE id = ? AND user_id = ?
            RETURNING *
        """, values)
        
        row = cursor.fetchone()
        return self.db_manager._row_to_task(row) if row else None

def delete_task(self, task_id: str, user_id: str) -> bool:
    with sqlite3.connect(self.db_manager.db_path) as conn:
        cursor = conn.cursor()
        # First delete any subtasks
        cursor.execute("""
            DELETE FROM tasks 
            WHERE parent_task_id = ? AND user_id = ?
        """, (task_id, user_id))
        
        # Then delete the main task
        cursor.execute("""
            DELETE FROM tasks 
            WHERE id = ? AND user_id = ?
        """, (task_id, user_id))
        return cursor.rowcount > 0