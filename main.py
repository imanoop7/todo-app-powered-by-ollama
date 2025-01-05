from database.db_manager import DatabaseManager
from services.auth_service import AuthService
from services.task_service import TaskService
from services.ollama_service import LlamaService
from ui.todo_app import TodoApp

def main():
    # Initialize services
    db_manager = DatabaseManager()
    auth_service = AuthService(db_manager)
    llama_service = LlamaService()
    task_service = TaskService(db_manager, llama_service)
    
    # Create and run the UI
    app = TodoApp(task_service, auth_service)
    app.run()

if __name__ == "__main__":
    main()