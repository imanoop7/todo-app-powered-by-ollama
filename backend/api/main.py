from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
import uvicorn

from models.task import Task, TaskCreate
from models.user import User, UserCreate
from services.auth import AuthService
from services.task import TaskService
from database.db_manager import DatabaseManager

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db_manager = DatabaseManager()
auth_service = AuthService(db_manager)
task_service = TaskService(db_manager)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user_id = auth_service.verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user_id

@app.post("/api/register")
async def register(user_data: UserCreate):
    # Implementation for user registration
    pass

@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Implementation for user login
    pass

@app.get("/api/tasks", response_model=List[Task])
async def get_tasks(current_user: str = Depends(get_current_user)):
    return task_service.get_user_tasks(current_user)

@app.post("/api/tasks", response_model=Task)
async def create_task(task: TaskCreate, current_user: str = Depends(get_current_user)):
    return task_service.create_task(current_user, task)

@app.put("/api/tasks/{task_id}/complete")
async def complete_task(task_id: str, current_user: str = Depends(get_current_user)):
    success = task_service.complete_task(task_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success"}

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str, current_user: str = Depends(get_current_user)):
    success = task_service.delete_task(task_id, current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)