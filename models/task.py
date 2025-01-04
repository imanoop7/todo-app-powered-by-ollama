from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RecurrenceType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    NONE = "none"

@dataclass
class Task:
    id: str
    title: str
    description: Optional[str]
    priority: Priority
    due_date: Optional[datetime]
    created_at: datetime
    tags: List[str]
    category: Optional[str]
    completed: bool
    user_id: str
    recurrence: RecurrenceType
    parent_task_id: Optional[str]
    subtasks: List['Task']
    points: int = 0