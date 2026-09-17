from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    done: bool


app = FastAPI(title="Task API", description="A simple task management API", version="1.0.0")
tasks = [{"id": 1, "title": "Clg Studies", "done": True}, {"id": 2, "title": "Workout", "done": True}, {"id": 3, "title": "Grocery Shopping", "done": False}]


@app.get("/", summary="Get API information")
async def root():
    return {"name": "Task API", "version": "1.0.0", "endpoints":["/tasks"]}

@app.get("/health", summary="Check the API is running")
async def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="Get all tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}", summary="Get a task by ID", responses={404: {"description": "Task not found"}})
async def get_task(id: int):
    for task in tasks:
       if task["id"] == id:
          return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", status_code=201, summary="Create a new task", responses={400: {"description": "Task title is required"}})
async def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Task title is required")
    new_task = {"id": len(tasks) + 1, "title": task.title, "done": False}
    tasks.append(new_task)
    return new_task

@app.delete("/tasks/{id}", status_code=204, summary="Delete a task", responses={404: {"description": "Task not found"}})
async def delete_task(id: int):
    for task in tasks :
        if task["id"] == id:
            tasks.remove(task)
            return 
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{id}", summary="Update a task", responses={400: {"description": "Task title is required"}, 404: {"description": "Task not found"}})
async def update_task(id: int, task_update: TaskUpdate):
    if not task_update.title.strip():
        raise HTTPException(status_code=400, detail="Task title is required")
    for task in tasks:
        if task["id"] == id:
            task["title"] = task_update.title
            task["done"] = task_update.done
            return task
    raise HTTPException(status_code=404, detail="Task not found")
