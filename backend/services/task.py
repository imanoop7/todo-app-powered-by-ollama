from typing import List, Optional
from models.task import Task, TaskCreate
from database.db_manager import DatabaseManager

class TaskService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_task(self, user_id: str, task_data: TaskCreate) -> Task:
        task = Task(**task_data.dict(), user_id=user_id)
        self.db_manager.add_task(task)
        return task

    def get_user_tasks(self, user_id: str) -> List[Task]:
        return self.db_manager.get_tasks(user_id)

    def complete_task(self, task_id: str, user_id: str) -> bool:
        return self.db_manager.mark_completed(task_id, user_id)

    def delete_task(self, task_id: str, user_id: str) -> bool:
        return self.db_manager.delete_task(task_id, user_id)